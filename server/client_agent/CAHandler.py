from panda3d.core import UniqueIdAllocator
from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import MessageTypes as msg_types
from server.handlers.SocketHandler import SocketHandler
from server.handlers.PacketHandler import PacketHandler
from lib.logging.Logger import Logger


class CAHandler(PacketHandler, SocketHandler):
    logger = Logger("ca_handler")

    def __init__(self, port=None, host=6660):
        self.active_clients = {}
        self.allocate_channel = UniqueIdAllocator(1000000, 1999999)

        PacketHandler.__init__(self)
        SocketHandler.__init__(self, port, host)
        self.configure()

    def configure(self):
        SocketHandler.connect_socket(self)
        self.logger.info("handler online")

    def setup_new_connection(self, connection):
        channel = self.allocate_channel.allocate()
        self.active_clients[channel] = connection
        self.register_channel(channel)

    def register_channel(self, channel):
        dg = PyDatagram()
        dg.addUint16(msg_types.CONTROL_SET_CHANNEL)
        dg.addUint64(channel)
        self.cWriter.send(dg, self.connection)

    def unregister_channel(self, channel):
        dg = PyDatagram()
        dg.addUint16(msg_types.CONTROL_REMOVE_CHANNEL)
        dg.addUint64(channel)
        self.cWriter.send(dg, self.connection)

    def handle_packet(self, dg):
        connection = dg.getConnection()
        dgi = PyDatagramIterator(dg)
        msg = dgi.getUint16()

        # begin handling messages here
        if msg == msg_types.CLIENT_HEARTBEAT:
            self.handle_client_heartbeat(dgi)
        elif msg == msg_types.CLIENT_LOGIN_2:
            self.handle_client_login(dgi, connection)
        elif msg == msg_types.CLIENT_DISCONNECT:
            self.handle_client_disconnect(dgi, connection)
        else:
            self.logger.warn("received unimplemented message type - %d" % msg)

    def handle_client_heartbeat(self, dgi):
        # TODO - handle and keep track of client heartbeats
        self.logger.debug("received client heartbeat")

    def handle_client_login(self, dgi, connection):
        # TODO - dynamically set user info from the DBServer
        token = dgi.getString()
        self.logger.debug("logging in user %s" % token)

        # TODO - sanity checks
        serverVersion = dgi.getString()
        hashVal = dgi.getInt32()
        
        dg = PyDatagram()
        dg.addUint16(msg_types.CLIENT_LOGIN_2_RESP)
        dg.addUint8(0)  # returnCode
        dg.addString("")  # errorString

        # begin account details
        dg.addString(token)  # username
        dg.addUint8(0)  # secretChatAllowed
        dg.addUint32(0)  # sec
        dg.addUint32(0)  # usec
        dg.addUint8(1)  # isPaid

        self.cWriter.send(dg, connection)

    def handle_client_disconnect(self, dgi, connection):
        # TODO - unregister channels
        self.logger.warn("client from %s has disconnected" % str(connection))
