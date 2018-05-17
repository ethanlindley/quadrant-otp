from server.network.Connector import Connector
from server.network.Listener import Listener
from lib.logging.Logger import Logger


class ClientAgent(Connector, Listener):
    logger = Logger("client_agent")

    def __init__(self, host_addr, md_port, ca_port):
        Listener.__init__(self, host_addr, ca_port)
        Connector.__init__(self, host_addr, md_port)

    def setup(self):
        Listener.configure(self)
        Connector.configure(self)
        self.logger.info("protocol online")
