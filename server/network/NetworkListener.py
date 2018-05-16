from panda3d.core import QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, PointerToConnection, NetAddress
from direct.task import Task

from lib.datagram.Datagram import Datagram
from lib.logging.Logger import Logger
from .NetworkManager import NetworkManager


class NetworkListener(NetworkManager):
    notify = Logger('NetworkListener')

    def __init__(self, host_addr, port, backlog=10000):
        self.host_addr = host_addr
        self.port = port
        self.backlog = backlog  # if the backlog exceeds supplied value, something is wrong

        self.socket = None
        self.active_connections = []
        
        NetworkManager.__init__(self)
        self.qcl = QueuedConnectionListener(self, 0)
        self.qcr = QueuedConnectionReader(self, 0)
        self.cw = ConnectionWriter(self, 0)

    def setup_socket(self):
        if self.socket is None:
            try:
                self.socket = self.openTCPServerRendezvous(self.host_addr, self.port, self.backlog)
                self.qcl.addConnection(self.socket)
                self.logger.info("socket now listening on %s" % (str(self.port)))

                taskMgr.add(self.listen_incoming, self.get_uid("listen-incoming"))
                taskMgr.add(self.read_incoming, self.get_uid("read-incoming"))
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
        # TODO - poll for incoming data
        if self.qcr.dataAvailable():
            dg = Datagram()  # catch the incoming data
            if self.qcr.getData(dg):
                # check the return value; if we were threaded, 
                # someone could've snagged the data before we did
                # TODO - handle incoming packets
                pass

        return task.cont
