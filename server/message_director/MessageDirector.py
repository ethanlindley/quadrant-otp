from panda3d.core import NetDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from .MDInterface import MDInterface
from server.core.ServerBase import ServerBase
from lib.logging.Logger import Logger


class MessageDirector(ServerBase):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerBase.__init__(self, host, port, MDInterface)

        self.registered_clients = {}

    def setup(self):
        ServerBase.configure(self)
        self.logger.info("server started")

    def register_channel(self, channel, connection):
        if self.registered_clients[channel] is None:
            self.registered_clients[channel] = connection
            self.logger.debug("registered new channel - %d" % channel)

    def unregister_channel(self, channel):
        if self.registered_clients[channel]:
            del self.registered_clients[channel]
            self.logger.debug("unregistered channel - %d" % channel)

    def handle_data(self, datagram):
        connection = datagram.getConnection()
        self.__active_interface.__handle_datagram(datagram)
