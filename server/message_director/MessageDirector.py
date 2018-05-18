from .MDHandler import MDHandler
from server.handlers.ServerHandler import ServerHandler
from lib.logging.Logger import Logger


class MessageDirector(ServerHandler):
    logger = Logger("message_director")

    def __init__(self, host, port):
        ServerHandler.__init__(self, host, port)
    
    def configure(self):
        ServerHandler.configure(self)
        self.logger.info("server online")
        self.handler = MDHandler()  # instantiate our handler

    def handle_data(self, dg):
        self.handler.handle_packet(dg)
