from panda3d.core import NetDatagram, DatagramIterator

from server.core.ServerBase import ServerBase
from lib.logging.Logger import Logger


class MessageDirector(ServerBase):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port)

    def setup(self):
        ServerBase.configure(self)
        self.logger.info("server started")

    def handle_data(self, dg):
        # TODO - handle any incoming data
        dgi = DatagramIterator(dg)
        if dgi.getRemainingSize() is None:
            return
