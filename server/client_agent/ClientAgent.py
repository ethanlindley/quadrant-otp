from panda3d.core import NetDatagram, DatagramIterator

from server.core.ServerBase import ServerBase
from server.core.SocketConnector import SocketConnector
from lib.logging.Logger import Logger


class ClientAgent(ServerBase, SocketConnector):
    logger = Logger("client_agent")

    def __init__(self, host, md_port, ca_port):
        ServerBase.__init__(self, host, ca_port)
        SocketConnector.__init__(self, host, md_port)

    def setup(self):
        ServerBase.configure(self)  # open a new socket for the ClientAgent
        SocketConnector.configure(self)  # once the socket is opened, open another socket and connect to the MD
        self.logger.info("server started")

    def handle_data(self, dg, connection):
        dgi = PyDatagramIterator(dg)
        # make sure the datagram contains data
        if dgi.getRemainingSize() is None:
            return
        msg = dgi.getUint8()
        self.logger.debug(msg)
