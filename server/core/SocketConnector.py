from panda3d.core import QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, NetDatagram

from lib.logging.Logger import Logger


class SocketConnector(QueuedConnectionManager):
    logger = Logger("socket_connector")

    def __init__(self, host, connect_port, timeout=5000):
        self.host = host
        self.connect_port = connect_port
        self.timeout = timeout

        self.socket = None

        self.read_task = None

        QueuedConnectionManager.__init__(self)
        self.cReader = QueuedConnectionReader(self, 0)
        self.cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.socket:
            return

        self.socket = self.openTCPClientConnection(self.host, self.connect_port, self.timeout)
        if self.socket is None:
            raise Exception("unable to connect to socket at %s:%s" % (self.host, str(self.port)))
        
        self.cReader.addConnection(self.socket)  # keep track of connected sockets to their respective listener(s)
        
        # poll for incoming data
        self.read_task = taskMgr.add(self.poll_incoming_data, "read-task")

    def poll_incoming_data(self, task):
        if self.cReader.getData():
            dg = NetDatagram()

            # make sure the dg actually contains data
            if self.cReader.dataAvailable(dg):
                self.handle_data(dg)
        
        return task.cont

    def handle_data(self, dg):
        # inheritors will handle the data specifically to their needs
        pass
