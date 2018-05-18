from panda3d.core import (QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, 
NetAddress, NetDatagram, PointerToConnection, UniqueIdAllocator)
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from lib.logging.Logger import Logger


class ServerBase(QueuedConnectionManager):
    logger = Logger("server_base")

    def __init__(self, host, listen_port, interface, backlog=10000):
        self.__host = host
        self.__listen_port = listen_port  # port we want to listen on
        self.__backlog = backlog

        self.__listen_socket = None
        self.__active_connections = []

        self.__interface = interface
        self.__active_interface = None
        self.__interface_objects = {}

        self.__allocated_channels = []

        self.__listen_task = None
        self.__read_task = None

        QueuedConnectionManager.__init__(self)
        self.__cListener = QueuedConnectionListener(self, 0)
        self.__cReader = QueuedConnectionReader(self, 0)
        self.__cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.__listen_socket:
            return
        
        self.__listen_socket = self.openTCPServerRendezvous(self.__host, self.__listen_port, self.__backlog)
        if self.__listen_socket is None:
            raise Exception("unable to open socket at %s:%s" % (self.__host, str(self.__listen_port)))

        self.__cListener.addConnection(self.__listen_socket)  # keep track of listening sockets

        # poll for any incoming suggestions or data
        self.__listen_task = taskMgr.add(self.__poll_incoming_suggestions, "listen-task")
        self.__read_task = taskMgr.add(self.__poll_incoming_data, "read-task")

    def __poll_incoming_suggestions(self, task):
        if self.__cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            net_addr = NetAddress()
            new_conn = PointerToConnection()

            if self.__cListener.getNewConnection(rendezvous, net_addr, new_conn):
                new_conn = new_conn.p()
                self.__handle_suggestion(rendezvous, net_addr, new_conn)
        
        return task.cont

    def __poll_incoming_data(self, task):
        if self.__cReader.dataAvailable():
            dg = NetDatagram()

            # make sure the dg actually contains data
            if self.__cReader.getData(dg):
                self.__handle_data(dg)
        
        return task.cont

    def __handle_data(self, datagram):
        # to be overridden by inheritors
        pass

    def __handle_suggestion(self, rendezvous, net_addr, new_conn):
        self.__active_interface = self.__interface(self, rendezvous, net_addr, new_conn)  # instantiate a new interface
        if self.__active_interface.__connection not in self.__interface_objects:
            self.__interface_objects[self.__active_interface.__connection] = self.__active_interface
            self.__cReader.addConnection(self.__active_interface.__connection)

    def __allocate_channel(self):
        channel = UniqueIdAllocator(1100, 1500).allocate()
        if channel > 1000000000:
            raise ValueError("unable to allocate new channels (exceeded max)")
        self.__allocated_channels.append(channel)
        return channel

    def __shutdown(self):
        if self.__listen_task or self.__read_task:
            # first, let's terminate all the current connections to the listener
            for client in self.__active_connections:
                self.__cReader.removeConnection(client)
            self.__active_connections = []  # reset the connection list

            # end current running tasks
            taskMgr.remove(self.__listen_task)
            taskMgr.remove(self.__read_task)
            self.__listen_task = None
            self.__read_task = None

            self.closeConnection(self.__listen_socket)  # close our listener
            self.__socket = None
