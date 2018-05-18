from panda3d.core import QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, NetDatagram

from lib.logging.Logger import Logger


class SocketConnector(QueuedConnectionManager):
    logger = Logger("socket_connector")

    def __init__(self, host, connect_port, timeout=5000):
        self.__host = host
        self.__connect_port = connect_port
        self.__timeout = timeout

        self.__socket = None

        self.__read_task = None

        QueuedConnectionManager.__init__(self)
        self.__cReader = QueuedConnectionReader(self, 0)
        self.__cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.__socket:
            return

        self.__socket = self.openTCPClientConnection(self.__host, self.__connect_port, self.__timeout)
        if self.__socket is None:
            raise Exception("unable to connect to socket at %s:%s" % (self.host, str(self.port)))
        
        self.__cReader.addConnection(self.__socket)  # keep track of connected sockets to their respective listener(s)
        
        # poll for incoming data
        self.__read_task = taskMgr.add(self.__poll_incoming_data, "read-task")

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

    def shutdown(self):
        if self.__read_task:
            taskMgr.remove(self.__read_task)
            self.__read_task = None
            
            self.__closeConnection(self.__socket)  # close the reading socket
            self.__socket = None
