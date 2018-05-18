from panda3d.core import NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import MessageTypes as msg_types
from server.core.InterfaceObject import InterfaceObject
from lib.logging.Logger import Logger


class MDInterface(InterfaceObject):
    logger = Logger("md_interface")

    def __init__(self, parent, rendezvous, net_addr, conn, our_channel=None):
        InterfaceObject.__init__(self, parent, rendezvous, net_addr, conn, our_channel)

    def handle_datagram(self, datagram):
        dgi = PyDatagramIterator(datagram)
        msg = dgi.getUint16()
        connection = datagram.getConnection()

        # make sure the datagram contains data
        if dgi.getRemainingSize() is None:
            return
        
        if msg == msg_types.CONTROL_SET_CHANNEL:
            channel = dgi.getUint64()
            self.__parent.register_channel(channel, connection)
        elif msg == msg_types.CONTROL_REMOVE_CHANNEL:
            self.parent.unregister_channel(channel)
        else:
            self.logger.debug("received unimplemented message type - %s" % str(msg))
