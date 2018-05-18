from direct.distributed.PyDatagram import PyDatagram

from server.types import MessageTypes as msg_types
from lib.logging.Logger import Logger


class InterfaceObject:
    logger = Logger("interface_object")

    def __init__(self, parent, rendezvous, net_addr, connection, channel=None):
        self.parent = parent
        self.rendezvous = rendezvous
        self.net_addr = net_addr
        self.connection = connection
        self.channel = channel

    def setup(self):
        self.parent.__add_interface(self.rendezvous, self.net_addr, self.connection)

    def __handle_datagram(self, datagram):
        # to be overridden by inheritors
        pass

    def __register_for_channel(self, channel):
        dg = PyDatagram()
        dg.addUint16(msg_types.CONTROL_SET_CHANNEL)
        dg.addUint16(channel)
        self.parent.__cWriter.send(dg, self.parent.__socket)  # make sure we're sending the datagram to the MD

    def __unregister_for_channel(self, channel):
        dg = PyDatagram()
        dg.addUint16(msg_types.CONTROL_REMOVE_CHANNEL)
        dg.addUint16(channel)
        self.parent.__cWriter.send(dg, self.parent.__socket)  # make sure we're sending the datagram to the MD
