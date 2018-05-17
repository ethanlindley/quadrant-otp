from panda3d.core import (QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, 
NetAddress, NetDatagram, PointerToConnection)
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from lib.logging.Logger import Logger


class ServerBase(QueuedConnectionManager):
    logger = Logger("server_base")

    def __init__(self, host, listen_port, interface, backlog=10000):
        self.host = host
        self.listen_port = listen_port  # port we want to listen on
        self.backlog = backlog

        self.socket = None
        self.active_connections = []

        self.interface = interface
        self.interface_objects = {}

        self.listen_task = None
        self.read_task = None

        QueuedConnectionManager.__init__(self)
        self.cListener = QueuedConnectionListener(self, 0)
        self.cReader = QueuedConnectionReader(self, 0)
        self.cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.socket:
            return
        
        self.socket = self.openTCPServerRendezvous(self.host, self.listen_port, self.backlog)
        if self.socket is None:
            raise Exception("unable to open socket at %s:%s" % (self.host, str(self.listen_port)))

        self.cListener.addConnection(self.socket)  # keep track of listening sockets

        # poll for any incoming suggestions or data
        self.listen_task = taskMgr.add(self.poll_incoming_suggestions, "listen-task")
        self.read_task = taskMgr.add(self.poll_incoming_data, "read-task")

    def poll_incoming_suggestions(self, task):
        if self.cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            net_addr = NetAddress()
            new_conn = PointerToConnection()

            if self.cListener.getNewConnection(rendezvous, net_addr, new_conn):
                new_conn = new_conn.p()
                self.handle_suggestion(rendezvous, net_addr, new_conn)
        
        return task.cont

    def poll_incoming_data(self, task):
        if self.cReader.dataAvailable():
            dg = NetDatagram()

            # make sure the dg actually contains data
            if self.cReader.getData(dg):
                conn = dg.getConnection()
                self.handle_data(dg, conn)
        
        return task.cont

    def handle_data(self, dg, connection):
        # to be overridden by inheritors
        pass

    def handle_suggestion(self, rendezvous, net_addr, new_conn):
        interface = self.interface(self, rendezvous, net_addr, new_conn)  # instantiate a new interface
        if interface.connection not in self.interface_objects:
            self.interface_objects[interface.connection] = interface
            self.cReader.addConnection(interface.connection)

    def get_interface_from_datagram(self, interface_channel):
        for interface in self.interface_objects:
            if interface.channel == interface_channel:
                return interface
        return None

    def shutdown(self):
        if self.listen_task or self.read_task:
            # first, let's terminate all the current connections to the listener
            for client in self.active_connections:
                self.cReader.removeConnection(client)
            self.active_connections = []  # reset the connection list

            # end current running tasks
            taskMgr.remove(self.listen_task)
            taskMgr.remove(self.read_task)
            self.listen_task = None
            self.read_task = None

            self.closeConnection(self.socket)  # close our listener
            self.socket = None
