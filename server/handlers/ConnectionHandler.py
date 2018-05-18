from panda3d.core import QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, NetDatagram

from lib.logging.Logger import Logger


class ConnectionHandler(QueuedConnectionManager):
    logger = Logger("connection_handler")

    def __init__(self, md_host, md_port, timeout=5000):
        self.md_host = md_host
        self.md_port = md_port
        self.timeout = timeout

        self.client_socket = None

        QueuedConnectionManager.__init__(self)
        self.__cReader = QueuedConnectionReader(self, 0)
        self.cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.client_socket is None:
            self.client_socket = self.openTCPClientConnection(self.md_host, self.md_port, self.timeout)
            if self.client_socket is None:
                raise Exception("unable to connect to socket at %s:%d" % (self.md_host, self.md_port))
            self.__cReader.addConnection(self.client_socket)

            taskMgr.add(self.__read_data, "read-task")

    def __read_data(self, task):
        if self.__cReader.dataAvailable():
            dg = NetDatagram()

            if self.__cReader.getData(dg):
                self.__handle_data(dg)
        return task.cont

    def handle_data(self, dg):
        # to be overridden by inheritors
        pass
