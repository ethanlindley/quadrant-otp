from panda3d.core import NetAddress, PointerToConnection

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

    def listen_suggestions(self, task):
        if self.cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            net_addr = NetAddress()
            new_conn = PointerToConnection()

            if self.cListener.getNewConnection(rendezvous, net_addr, new_conn):
                new_conn = new_conn.p()

                self.logger.warn("new connection from %s" % str(net_addr))
                self.active_connections.append(new_conn)
                self.handler.setup_new_connection(new_conn)
                self.cReader.addConnection(new_conn)
        return task.cont

    def handle_data(self, dg):
        self.handler.handle_packet(dg)
