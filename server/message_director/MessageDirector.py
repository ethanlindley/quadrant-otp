from lib.logging.Logger import Logger
from server.network.ConnectionListener import ConnectionListener


class MessageDirector(ConnectionListener):
    logger = Logger("MessageDirector")

    def __init__(self, host_addr, md_port):
        ConnectionListener.__init__(host_addr, md_port)

    def setup_server(self):
        ConnectionListener.setup(self)
