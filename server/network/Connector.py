from panda3d.core import QueuedConnectionManager, QueuedConnectionReader, ConnectionWriter, NetDatagram
from direct.task.Task import Task

from lib.logging.Logger import Logger


class Connector(QueuedConnectionManager):
    logger = Logger("network_connector")

    def __init__(self, host_addr, port, timeout=5000):
        self.host_addr = host_addr
        self.__port = port
        self.timeout = timeout

        self.client_sock = None
        
        self.read_task = None

        QueuedConnectionManager.__init__(self)
        self.qcr = QueuedConnectionReader(self, 0)
        self.cw = ConnectionWriter(self, 0)

    def configure(self):
        if self.client_sock is None:
            try:
                self.client_sock = self.openTCPClientConnection(self.host_addr, self.__port, self.timeout)
                self.qcr.addConnection(self.client_sock)
            except:
                raise Exception("unable to connect to %s:%s" % (self.host_addr, str(self.port)))
            
        self.read_task = taskMgr.add(self.poll_incoming_data, "poll-data")

    def poll_incoming_data(self, task):
        if self.qcr.dataAvailable():
            dg = NetDatagram()
            if self.qcr.getData(dg):
                self.handle_data(dg)

        return Task.cont

    def handle_data(self, dg):
        # TODO - handle data
        pass
