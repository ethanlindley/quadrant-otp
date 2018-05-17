from panda3d.core import QueuedConnectionReader, ConnectionWriter, NetDatagram, DatagramIterator
from direct.task.Task import Task

from lib.logging.Logger import Logger
from .NetworkManager import NetworkManager

class NetworkConnector(NetworkManager):
    logger = Logger("NetworkConnector")

    def __init__(self, host_addr, port, timeout=5000):
        self.host_addr = host_addr
        self.port = port
        self.timeout = timeout

        self.socket = None
        self.read_task = None

        NetworkManager.__init__(self)
        self.qcr = QueuedConnectionReader(self, 0)
        self.cw = ConnectionWriter(self, 0)

    def connect(self):
        if self.socket is None:
            try:
                self.socket = self.openTCPClientConnection(self.host_addr, self.port, self.timeout)
                self.qcr.addConnection(self.socket)
            except:
                raise Exception("unable to connect to %s:%s" % (self.host_addr, str(self.port)))
        
        self.read_task = taskMgr.add(self.read_incoming, self.get_uid("read-incoming"))

    def read_incoming(self, task):
        # poll for incoming data to the server
        if self.qcr.dataAvailable():
            dg = NetDatagram()  # catch the incoming data

            # check the return value; if we were threaded, 
            # someone could've snagged the data before we did
            if self.qcr.getData(dg):
                self.handle_data(dg)

        return task.cont

    def handle_data(self, dg):
        # make sure the received packet actually contains data
        if dg.get_length() is None:
            return
        
        di = DatagramIterator(dg)

        # TODO - get data from datagram?

    def handle_datagram(self, sender, msg_type, dg):
        # properly handle any incoming packets to the server
        # NOTE: to be overridden by inheritors
        pass

    def shutdown(self):
        if self.read_task:
            taskMgr.remove(self.read_task)
        
        self.qcr.removeConnection(self.socket)
