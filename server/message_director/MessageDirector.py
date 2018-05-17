from panda3d.core import NetDatagram, UniqueIdAllocator
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from .MDInterface import MDInterface
from server.core.ServerBase import ServerBase
from lib.logging.Logger import Logger


class MessageDirector(ServerBase):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port, MDInterface)

        self.channel_allocator = UniqueIdAllocator(1000000000, 1009999999)

    def setup(self):
        ServerBase.configure(self)
        self.logger.info("server started")

    def register_channel(self, channel):
        # TODO - handle any requests to register a new channel to the MD
        pass

    def unregister_channel(self, channel):
        # TODO - handle any requests to unregister a channel from the MD
        pass

    def handle_data(self, dg, connection):
        dgi = PyDatagramIterator(dg)
        interface = self.get_interface_from_datagram(dgi.getUint64())
        dg = interface.handle_datagram()
        self.cWriter.send(dg, connection)
