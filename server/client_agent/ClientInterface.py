from panda3d.core import NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import ChannelTypes as channel_types
from server.core.InterfaceObject import InterfaceObject
from lib.logging.Logger import Logger


class ClientInterface(InterfaceObject):
    logger = Logger("client_interface")

    def __init__(self, parent, rendezvous, net_addr, conn, our_channel=None):
        InterfaceObject.__init__(self, parent, rendezvous, net_addr, conn, our_channel)

    def setup(self):
        InterfaceObject.setup(self)

        if self.channel is None:
            self.channel = self.parent.allocate_channel()
            self.__register_for_channel(self.channel)
        
        self.logger.info("interface started")

    def handle_datagram(self, datagram):
        # NOTE - incomplete method
        dgi = PyDatagramIterator(datagram)
        msg = dgi.getUint16()

        # make sure the datagram contains data
        if dgi.getRemainingSize() is None:
            return
        
        self.logger.debug("received new message - %s" % str(msg))
