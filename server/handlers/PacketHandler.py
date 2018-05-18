from panda3d.core import UniqueIdAllocator

from lib.logging.Logger import Logger


class PacketHandler:
    logger = Logger("packet_handler")

    def __init__(self, our_channel=None):
        self.our_channel = our_channel

    def configure(self):
        # to be overridden by inheritors
        pass

    def allocate_channel(self):
        channel = UniqueIdAllocator(1000000, 1999999).allocate()
        if channel > 1999999:
            return ValueError("trying to allocate more channels than allowed")
        return channel

    def handle_packet(self, dg):
        # to be overridden by inheritors
        pass
