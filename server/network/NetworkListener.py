from panda3d.core import QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter
from lib.logging.Logger import Logger
from .NetworkManager import NetworkManager


class NetworkListener(NetworkManager):
    notify = Logger('NetworkListener')

    def __init__(self, host_addr, port, backlog):
        self.host_addr = host_addr
        self.port = port
        self.backlog = backlog

        self.socket = None
        self.listen_task = None
        self.read_task = None
        
        NetworkManager.__init__(self)
        self.qcl = QueuedConnectionListener.__init__(self, 0)
        self.qcr = QueuedConnectionReader.__init__(self, 0)
        self.cw = ConnectionWriter.__init__(self, 0)

    def setup_server(self):
        if self.socket is None:
            try:
                self.socket = self.openTCPSeverRendezvous(self.host_addr, self.port, self.backlog)
            except:
                raise Exception("unable to open socket on port %s" % (str(self.port)))
                
            self.qcl.add_connection(self.socket)
            notify.info("socket now listenening on %s" % (str(self.port)))

    def listen_incoming(self, task):
        # TODO - poll for incoming suggestions 
        pass

    def read_incoming(self, task):
        # TODO - poll for incoming data
        pass
