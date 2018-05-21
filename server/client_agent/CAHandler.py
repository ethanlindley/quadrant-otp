from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import MessageTypes as msg_types
from server.handlers.ConnectionHandler import ConnectionHandler
from server.handlers.PacketHandler import PacketHandler
from lib.logging.Logger import Logger


class CAHandler(PacketHandler, ConnectionHandler):
    logger = Logger("ca_handler")

    def __init__(self, host, port):
        self.active_clients = {}

        PacketHandler.__init__(self)
        ConnectionHandler.__init__(self, host, port)
        self.configure()

    def configure(self):
        ConnectionHandler.configure(self)
        self.logger.info("handler online")

        if self.our_channel is None:
            self.our_channel = self.allocate_channel.allocate()

            self.register_channel(self.our_channel)

    def setup_new_connection(self, connection):
        channel = self.allocate_channel.allocate()
        self.active_clients[channel] = connection
        self.register_channel(channel)

    def register_channel(self, channel):
        dg = PyDatagram()
        dg.addUint16(msg_types.CONTROL_SET_CHANNEL)
        dg.addUint64(channel)
        self.cWriter.send(dg, self.client_socket)

    def handle_packet(self, dg):
        dgi = PyDatagramIterator(dg)
        msg = dgi.getUint16()
        self.logger.debug("received new message - %d" % msg)

        # begin handling messages here
        if msg == msg_types.CLIENT_HEARTBEAT:
            self.handle_client_heartbeat(dgi)
        elif msg == msg_types.CLIENT_LOGIN_3:
            self.handle_client_login(dgi)

    def handle_client_heartbeat(self, dgi):
        # TODO - handle and keep track of client heartbeats
        pass

    def handle_client_login(self, dgi):
        # TODO - handle client login requests
        pass
