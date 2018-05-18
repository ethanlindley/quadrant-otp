from .CAHandler import CAHandler
from server.handlers.ConnectionHandler import ConnectionHandler
from server.handlers.ServerHandler import ServerHandler
from lib.logging.Logger import Logger


class ClientAgent(ServerHandler, ConnectionHandler):
    logger = Logger("client_agent")

    def __init__(self, host, port, ca_port):
        ServerHandler.__init__(self, host, ca_port)
        ConnectionHandler.__init__(self, host, port)

    def configure(self):
        ServerHandler.configure(self)
        ConnectionHandler.configure(self)
        self.logger.info("server online")
        self.handler = CAHandler(self.md_host, self.md_port)  # instantiate our handler

    def handle_data(self, dg):
        self.handler.handle_packet(dg)
