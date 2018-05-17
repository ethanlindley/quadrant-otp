from panda3d.core import NetDatagram
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

    def setup(self):
        ServerBase.configure(self)
        SocketConnector.configure(self)
        self.logger.info("server started")

    def handle_data(self, dg, connection):
        dg = self.interface.handle_datagram()
        self.cWriter.send(dg, connection)
