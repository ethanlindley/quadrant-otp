from panda3d.core import (QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, 
NetAddress, PointerToConnection, NetDatagram)

from lib.logging.Logger import Logger


class SocketHandler:
    logger = Logger("socket_handler")

    def __init__(self, port=None, host=None, ip_addr="127.0.0.1", backlog=10000, timeout=5000):
        self.port = port  # our port
        self.host = host  # host port
        self.ip_addr = ip_addr
        self.backlog = backlog
        self.timeout = timeout

        self.socket = None
        self.connection = None
        self.active_connections = []

        self.handler = None

        self.cManager = QueuedConnectionManager()
        self.cListener = QueuedConnectionListener(self.cManager, 0)
        self.cReader = QueuedConnectionReader(self.cManager, 0)
        self.cWriter = ConnectionWriter(self.cManager, 0)

    def setup_socket(self):
        self.socket = self.cManager.openTCPServerRendezvous(self.ip_addr, self.port, self.backlog)
        if self.socket is None:
            raise Exception("unable to open new socket at %s:%d" % (self.ip_addr, self.port))
        self.cListener.addConnection(self.socket)

        taskMgr.add(self.listen_suggestions, "poll the suggestion listener")
        taskMgr.add(self.read_data, "poll the connection reader")

    def connect_socket(self):
        if self.connection is None:
            self.connection = self.cManager.openTCPClientConnection(self.ip_addr, self.host, self.timeout)
            if self.connection is None:
                raise Exception("unable to connect to socket at %s:%d" % (self.ip_addr, self.host))
            self.cReader.addConnection(self.connection)

            taskMgr.add(self.read_data, "poll the socket reader")
    
    def listen_suggestions(self, task):
        # to be overridden by inheritors
        pass

    def read_data(self, task):
        if self.cReader.dataAvailable():
            dg = NetDatagram()

            if self.cReader.getData(dg):
                self.handle_data(dg)
        return task.cont

    def handle_data(self, dg):
        # to be overridden by inheritors
        pass
