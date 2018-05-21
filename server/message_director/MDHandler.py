from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import MessageTypes as msg_types
from server.handlers.SocketHandler import SocketHandler
from server.handlers.PacketHandler import PacketHandler
from lib.logging.Logger import Logger


class MDHandler(PacketHandler, SocketHandler):
    logger = Logger("md_handler")

    def __init__(self, port=None, host=6660):
        self.registered_channels = {}

        PacketHandler.__init__(self)
        SocketHandler.__init__(self, port, host)
        self.configure()

    def configure(self):
        SocketHandler.connect_socket(self)
        self.logger.info("handler online")

    def handle_packet(self, dg):
        dgi = PyDatagramIterator(dg)
        msg = dgi.getUint16()
        self.logger.debug("received message - %d" % msg)
        
        # begin handling messages here
        if msg == msg_types.CONTROL_SET_CHANNEL:
            channel = dgi.getUint64()
            connection = dg.getConnection()
            self.register_channel(channel, connection)
        elif msg == msg_types.CONTROL_REMOVE_CHANNEL:
            channel = dgi.getUint16()
            self.unregister_channel(channel)

    def register_channel(self, channel, connection):
        if channel not in self.registered_channels:
            self.registered_channels[channel] = connection
            self.logger.debug("registered new channel - %d" % channel)
        
    def unregister_channel(self, channel):
        if self.registered_channels[channel]:
            del self.registered_channels[channel]
            self.logger.debug("unregistered channel - %d" % channel)
