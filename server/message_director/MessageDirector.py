from panda3d.core import NetDatagram
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.core.ServerBase import ServerBase
from lib.logging.Logger import Logger


class MessageDirector(ServerBase):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port)

    def setup(self):
        ServerBase.configure(self)
        self.logger.info("server started")

    def handle_data(self, dg, connection):
        dgi = PyDatagramIterator(dg)
        # make sure the datagram contains data
        if dgi.getRemainingSize() is None:
            return
        msg = dgi.getUint8()
        self.logger.debug(msg)
