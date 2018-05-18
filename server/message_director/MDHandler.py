from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.handlers.PacketHandler import PacketHandler
from lib.logging.Logger import Logger


class MDHandler(PacketHandler):
    logger = Logger("md_handler")

    def __init__(self):
        PacketHandler.__init__(self)
        self.configure()

    def configure(self):
        if self.our_channel is None:
            self.our_channel = self.allocate_channel()
            # TODO - register channels within MD
        
        self.logger.info("handler online")

    def handle_packet(self, dg):
        dgi = PyDatagramIterator(dg)
        msg = dgi.getUint16()
        self.logger.debug("received message - %d" % msg)