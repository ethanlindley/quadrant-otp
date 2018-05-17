from panda3d.core import QueuedConnectionManager, QueuedConnectionListener, QueuedConnectionReader, ConnectionWriter, NetAddress, NetDatagram, PointerToAddress

from lib.logging.Logger import Logger


class ServerBase(QueuedConnectionManager):
    logger = Logger("server_base")

    def __init__(self, host, listen_port, backlog=10000):
        self.host = host
        self.listen_port = listen_port  # port we want to listen on
        self.backlog = backlog

        self.socket = None
        self.active_connections = []

        self.listen_task = None
        self.read_task = None

        QueuedConnectionManager.__init__(self)
        self.cListener = QueuedConnectionListener(self, 0)
        self.cReader = QueuedConnectionReader(self, 0)
        self.cWriter = ConnectionWriter(self, 0)

    def configure(self):
        if self.socket:
            return
        
        self.socket = self.openTCPServerRendezvous(self.host, self.listen_port, self.backlog)
        if self.socket is None:
            raise Exception("unable to open socket at %s:%s" % (self.host, str(self.listen_port)))

        self.cListener.addConnection(self.socket)  # keep track of listening sockets

        # poll for any incoming suggestions or data
        self.listen_task = taskMgr.add(self.poll_incoming_suggestions, "listen-task")
        self.read_task = taskMgr.add(self.poll_incoming_data, "read-task")

    def poll_incoming_suggestions(self, task):
        pass

    def poll_incoming_data(self, task):
        pass
