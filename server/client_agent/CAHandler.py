from direct.distributed.PyDatagram import PyDatagram
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from server.types import MessageTypes as msg_types
from server.handlers.ConnectionHandler import ConnectionHandler
from server.handlers.PacketHandler import PacketHandler
from lib.logging.Logger import Logger


class CAHandler(PacketHandler, ConnectionHandler):
    logger = Logger("ca_handler")

    def __init__(self, host, port):
        PacketHandler.__init__(self)
        ConnectionHandler.__init__(self, host, port)
        self.configure()

    def configure(self):
        ConnectionHandler.configure(self)
        self.logger.info("handler online")

        if self.our_channel is None:
            self.our_channel = self.allocate_channel()

            dg = PyDatagram()
            dg.addUint16(msg_types.CONTROL_SET_CHANNEL)
            dg.addUint64(self.our_channel)
            self.cWriter.send(dg, self.client_socket)

    def handle_packet(self, dg):
        dgi = PyDatagramIterator(dg)
        msg = dgi.getUint16()

        self.logger.debug("received new message - %d" % msg)
