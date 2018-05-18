from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import MessageTypes as msg_types
from server.handlers.PacketHandler import PacketHandler
from lib.logging.Logger import Logger


class MDHandler(PacketHandler):
    logger = Logger("md_handler")

    def __init__(self):
        PacketHandler.__init__(self)

        self.registered_handlers = {}

        self.configure()

    def configure(self):
        if self.our_channel is None:
            self.our_channel = self.allocate_channel()
            # TODO - register channels within MD
        
        self.logger.info("handler online")

    def handle_packet(self, dg):
        dgi = PyDatagramIterator(dg)
        msg = dgi.getUint16()
        self.logger.debug("received message - %d" % msg)
        
        # begin handling messages here
        if msg == msg_types.CONTROL_SET_CHANNEL:
            channel = dgi.getUint16()
            connection = dg.getConnection()
            self.register_channel(channel, connection)
        elif msg == msg_types.CONTROL_REMOVE_CHANNEL:
            channel = dgi.getUint16()
            self.unregister_channel(channel)
        

    def register_channel(self, channel, connection):
        if self.registered_handlers[channel] is None:
            self.registered_handlers[channel] = connection
            self.logger.debug("registered new channel - %d" % channel)
        
    def unregister_channel(self, channel):
        if self.registered_handlers[channel]:
            del self.registered_handlers[channel]
            self.logger.debug("unregistered channel - %d" % channel)
