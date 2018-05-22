from lib.logging.Logger import Logger


class PacketHandler:
    logger = Logger("packet_handler")

    def __init__(self):
        pass

    def configure(self):
        # to be overridden by inheritors
        pass

    def handle_packet(self, dg):
        # to be overridden by inheritors
        pass
