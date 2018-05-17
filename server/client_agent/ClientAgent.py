from lib.logging.Logger import Logger
from server.network.ConnectionListener import ConnectionListener
from server.network.NetworkConnector import NetworkConnector


class ClientAgent(ConnectionListener, NetworkConnector):
    logger = Logger("ClientAgent")

    def __init__(self, host_addr, md_port, ca_port):
        ConnectionListener.__init__(self, host_addr, ca_port)  # listen on a new socket
        NetworkConnector.__init__(self, host_addr, md_port)  # connect to message director socket

    def setup_server(self):
        ConnectionListener.setup_socket(self)
        NetworkConnector.connect(self)
        self.logger.info("socket online")
