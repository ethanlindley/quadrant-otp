from panda3d.core import NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.core.InterfaceObject import InterfaceObject
from lib.logging.Logger import Logger


class MDInterface(InterfaceObject):
    logger = Logger("md_interface")

    def __init__(self, parent, rendezvous, net_addr, conn, our_channel=None):
        InterfaceObject.__init__(self, parent, rendezvous, net_addr, conn, our_channel)

    def setup(self):
        if self.channel is None:
            self.channel = self.parent.channel_allocator.allocate()

    def handle_datagram(self, dg):
        dgi = PyDatagramIterator(dg)

        # make sure the datagram contains data
        if dgi.getRemainingSize() is None:
            return
        msg = dgi.getUint8()
        self.logger.debug("received new message - %s" % str(msg))
