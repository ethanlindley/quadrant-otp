from panda3d.core import (QueuedConnectionListener, QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, 
PointerToConnection, NetAddress)
from lib.datagram.Datagram import Datagram
from direct.task import Task
from lib.logging.Logger import Logger
from .NetworkManager import NetworkManager


class NetworkListener:
    notify = Logger('NetworkListener')

    def __init__(self, host_addr, port, backlog):
        self.host_addr = host_addr
        self.port = port
        self.backlog = backlog

        self.socket = None
        self.active_connections = []
        
        self.nwm = QueuedConnectionManager()
        self.qcl = QueuedConnectionListener.__init__(self.nwm, 0)
        self.qcr = QueuedConnectionReader.__init__(self.nwm, 0)
        self.cw = ConnectionWriter.__init__(self.nwm, 0)

    def setup_server(self):
        if self.socket is None:
            try:
                self.socket = self.nwm.openTCPSeverRendezvous(self.host_addr, self.port, self.backlog)
                self.qcl.addConnection(self.socket)
                notify.info("socket now listenening on %s" % (str(self.port)))

                taskMgr.add(self.listen_incoming, self.get_uid("listen-incoming"))
                taskMgr.add(self.read_incoming, self.get_uid("read-incoming"))
            except:
                raise Exception("unable to open socket on port %s" % (str(self.port)))

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

    def get_uid(self, name):
        return "%s-%d" % (name, id(self))
