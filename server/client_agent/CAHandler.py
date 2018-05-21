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

        PacketHandler.__init__(self)
        SocketHandler.__init__(self, port, host)
        self.configure()

    def configure(self):
        SocketHandler.connect_socket(self)
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
        elif msg == msg_types.CLIENT_LOGIN_3:
            self.handle_client_login(dgi, connection)
        elif msg == msg_types.CLIENT_SET_AVTYPE:
            self.handle_client_set_avtype(dgi, connection)
        elif msg == msg_types.CLIENT_ADD_INTEREST:
            self.handle_add_interest(dgi, connection)
        elif msg == msg_types.CLIENT_DISCONNECT:
            self.handle_client_disconnect(dgi, connection)
        else:
            self.logger.warn("received unimplemented message - %d" % msg)

    def handle_client_heartbeat(self, dgi):
        # TODO - handle and keep track of client heartbeats
        self.logger.debug("received client heartbeat")

    def handle_client_login(self, dgi, connection):
        token = dgi.getString()

        dg = PyDatagram()
        dg.addUint16(msg_types.CLIENT_LOGIN_3_RESP)
        dg.addUint8(0)  # returnCode
        dg.addString("")  # errorString

        # account details 
        dg.addString(token)  # username
        dg.addUint8(1)  # canChat
        dg.addUint32(00000)  # sec
        dg.addUint32(00000)  # usec 
        dg.addUint8(1)  # isPaid                
        dg.addInt32(00000)  # minutesRemaining
        dg.addString('dev')
        dg.addString('YES')
        dg.addInt32(00000)  # LastLogin

        self.cWriter.send(dg, connection)

    def handle_client_set_avtype(self, dgi, connection):
        # TODO - setup avatar types dynamically
        avId = dgi.getUint32()
        self.logger.debug("received SET_AVTYPE for avId %d" % avId)

    def handle_add_interest(self, dgi, connection):
        # TODO - setup interests
        handle = dgi.getUint16()  # interest ID
        contextId = dgi.getUint32()
        parentId = dgi.getUint32()  # related object
        zoneList = [dgi.getUint32()]  # zone to create object in
        self.logger.debug("received ADD_INTEREST - (%d, %d, %d, %s)" % (handle, contextId, parentId, zoneList))

    def handle_client_disconnect(self, dgi, connection):
        self.logger.warn("client from %s has disconnected" % str(connection))
        for client in self.active_clients:
            if self.active_clients[client] == connection:
                self.unregister_channel(client)
                del self.active_clients[client]
