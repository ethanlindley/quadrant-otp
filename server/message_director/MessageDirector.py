from panda3d.core import NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from .MDInterface import MDInterface
from server.core.ServerBase import ServerBase
from lib.logging.Logger import Logger


class MessageDirector(ServerBase):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port, MDInterface)

    def setup(self):
        ServerBase.configure(self)
        self.logger.info("server started")

    def handle_data(self, dg, connection):
        dg = self.interface.handle_datagram()
        self.cWriter.send(dg, connection)
