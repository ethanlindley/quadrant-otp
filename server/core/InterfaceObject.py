from direct.distributed.PyDatagram import PyDatagram

from server.types import MessageTypes as msg_types
from lib.logging.Logger import Logger


class InterfaceObject:
    logger = Logger("interface_object")

    def __init__(self, parent, rendezvous, net_addr, connection, channel=None):
        self.__parent = parent
        self.__rendezvous = rendezvous
        self.__net_addr = net_addr
        self.__connection = connection
        self.__channel = channel

    def __handle_datagram(self, datagram):
        # to be overridden by inheritors
        pass

    def __register_for_channel(self, channel):
        dg = PyDatagram()
        dg.addServerHeader(channel, channel, msg_types.CONTROL_SET_CHANNEL)
        self.__parent.__cWriter.send(dg, self.__parent.__socket)  # make sure we're sending the datagram to the MD

    def __unregister_for_channel(self, channel):
        dg = PyDatagram()
        dg.addServerHeader(channel, channel, msg_types.CONTROL_REMOVE_CHANNEL)
        self.__parent.__cWriter.send(dg, self.__parent.__socket)  # make sure we're sending the datagram to the MD
