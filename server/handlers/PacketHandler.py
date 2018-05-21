from panda3d.core import UniqueIdAllocator

from lib.logging.Logger import Logger


class PacketHandler:
    logger = Logger("packet_handler")

    def __init__(self, our_channel=None):
        self.our_channel = our_channel
        self.allocate_channel = UniqueIdAllocator(1000000, 1999999)

    def configure(self):
        # to be overridden by inheritors
        pass

    def handle_packet(self, dg):
        # to be overridden by inheritors
        pass
