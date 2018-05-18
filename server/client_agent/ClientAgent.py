from panda3d.core import NetDatagram, UniqueIdAllocator
from direct.distributed.PyDatagramIterator import PyDatagramIterator

from .ClientInterface import ClientInterface
from server.core.ServerBase import ServerBase
from server.core.SocketConnector import SocketConnector
from lib.logging.Logger import Logger


class ClientAgent(ServerBase, SocketConnector):
    logger = Logger("client_agent")

    def __init__(self, host, md_port, ca_port):
        ServerBase.__init__(self, host, ca_port, ClientInterface)
        SocketConnector.__init__(self, host, md_port)

        self.channel_allocator = UniqueIdAllocator(1000000000, 1009999999)

    def setup(self):
        ServerBase.configure(self)
        SocketConnector.configure(self)
        self.logger.info("server started")

    def handle_data(self, dg, connection):
        dgi = PyDatagramIterator(dg)
        interface = self.get_interface_from_datagram(dgi.getUint64())
        dg = interface.handle_datagram(dg)
        self.cWriter.send(dg, connection)
