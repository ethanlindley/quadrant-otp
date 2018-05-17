from lib.logging.Logger import Logger


class InterfaceObject:
    logger = Logger("interface_object")

    def __init__(self, parent, rendezvous, net_addr, connection, channel=None):
        self.parent = parent
        self.rendezvous = rendezvous
        self.net_addr = net_addr
        self.connection = connection
        self.channel = channel

    def handle_datagram(self, dg):
        # to be overridden by inheritors
        pass
