from panda3d.core import NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from .MDInterface import MDInterface
from server.core.ServerBase import ServerBase
from lib.logging.Logger import Logger


class MessageDirector(ServerBase):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port, MDInterface)

    def setup(self):
        ServerBase.configure(self)
        self.logger.info("server started")

    def is_registered_interface(self, channel, connection):
        # check and see if the current connection is a registered interface or not
        if channel in self.__registered_interfaces:
            if self.__registered_interfaces[channel] == connection:
                if connection in self.__potential_interfaces:
                    del self.__potential_interaces[connection]
                    return True
        else:
            return False

    def register_channel(self, channel, connection):
        if self.is_interface(channel, connection) is False:
            if self.__registered_clients[channel] is None:
                self.__registered_clients[channel] = connection
                self.logger.debug("registered new channel - %d" % channel)

    def unregister_channel(self, channel):
        if self.is_interface(channel, connection):
            if self.__registered_clients[channel]:
                del self.__registered_clients[channel]
                self.logger.debug("unregistered channel - %d" % channel)

    def __handle_data(self, datagram):
        self.logger.debug("received data")
