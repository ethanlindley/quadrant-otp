from panda3d.core import QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, PointerToConnection, NetAddress, NetDatagram
from direct.task.Task import Task

from lib.logging.Logger import Logger
from .NetworkManager import NetworkManager


class ConnectionListener(NetworkManager):
    notify = Logger("ConnectionListener")

    def __init__(self, host_addr, port, backlog=10000):
        self.host_addr = host_addr
        self.port = port
        self.backlog = backlog  # if the backlog exceeds supplied value, something is wrong

        self.socket = None
        self.active_connections = []

        self.listen_task = None
        self.read_task = None
        
        NetworkManager.__init__(self)
        self.qcl = QueuedConnectionListener(self, 0)
        self.qcr = QueuedConnectionReader(self, 0)
        self.cw = ConnectionWriter(self, 0)

    def setup_socket(self):
        # make sure a socket isn't already opened
        if self.socket is None:
            try:
                self.socket = self.openTCPServerRendezvous(self.host_addr, self.port, self.backlog)
                self.qcl.addConnection(self.socket)

                self.listen_task = taskMgr.add(self.listen_incoming, self.get_uid("listen-incoming"))
                self.listen_task = taskMgr.add(self.read_incoming, self.get_uid("read-incoming"))
            except:
                raise StandardError("unable to open port on socket %s:%s -- is the port open?" % (self.host_addr, str(self.port)))

    def listen_incoming(self, task):
        # poll for any incoming connections to the server
        if self.qcl.newConnectionAvailable():
            rendezvous = PointerToConnection()
            net_addr = NetAddress()
            new_conn = PointerToConnection()

            if self.qcl.getNewConnection(rendezvous, net_addr, new_conn):
                new_conn = new_conn.p()
                self.active_connections.append(new_conn)  # remember and store the new connection
                self.qcr.addConnection(new_conn)  # begin reading the connection

        return task.cont

    def read_incoming(self, task):
        # poll for incoming data to the server
        if self.qcr.dataAvailable():
            dg = NetDatagram()  # catch the incoming data

            # check the return value; if we were threaded, 
            # someone could've snagged the data before we did
            if self.qcr.getData(dg):
                # TODO - handle incoming packets
                pass

        return task.cont

    def shutdown_socket(self):
        # make sure that the tasks are running already
        if self.read_task is not None and self.listen_task is not None:
            taskMgr.remove(self.read_task)
            taskMgr.remove(self.listen_task)

            # terminate connection to all clients
            for client in self.active_connections:
                self.qcr.removeConnection(client)
            self.active_connections = []  # reset the list of connections

            self.closeConnection(socket)  # finally, let's close down the listener socket
