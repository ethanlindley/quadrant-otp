from panda3d.core import (QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, 
NetAddress, PointerToConnection, NetDatagram)

from lib.logging.Logger import Logger


class ServerHandler(QueuedConnectionManager):
    logger = Logger("server_handler")

    def __init__(self, host, port, backlog=10000):
        self.host = host
        self.port = port
        self.backlog = backlog

        self.socket = None
        self.active_connections = []

        self.handler = None

        QueuedConnectionManager.__init__(self)
        self.cListener = QueuedConnectionListener(self, 0)
        self.cReader = QueuedConnectionReader(self, 0)
        self.cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.socket is None:
            self.socket = self.openTCPServerRendezvous(self.host, self.port, self.backlog)
            if self.socket is None:
                raise Exception("unable to open new socket at %s:%d" % (self.host, self.port))
            self.cListener.addConnection(self.socket)

            taskMgr.add(self.listen_suggestions, "listen-task")
            taskMgr.add(self.__read_data, "read-task")
    
    def listen_suggestions(self, task):
        # to be overridden by inheritors
        pass

    def __read_data(self, task):
        if self.cReader.dataAvailable():
            dg = NetDatagram()

            if self.cReader.getData(dg):
                self.handle_data(dg)
        return task.cont

    def handle_data(self, dg):
        # to be overridden by inheritors
        pass
