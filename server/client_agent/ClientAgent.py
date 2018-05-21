from panda3d.core import NetAddress, PointerToConnection

from .CAHandler import CAHandler
from server.handlers.SocketHandler import SocketHandler
from lib.logging.Logger import Logger


class ClientAgent(SocketHandler):
    logger = Logger("client_agent")

    def __init__(self, port=6667, host=6660):
        SocketHandler.__init__(self, port, host)

    def configure(self):
        SocketHandler.setup_socket(self)
        SocketHandler.connect_socket(self)
        self.logger.info("server online")
        self.handler = CAHandler(self.host)  # instantiate our handler

    def listen_suggestions(self, task):
        if self.cListener.newConnectionAvailable():
            rendezvous = PointerToConnection()
            net_addr = NetAddress()
            new_conn = PointerToConnection()

            if self.cListener.getNewConnection(rendezvous, net_addr, new_conn):
                new_conn = new_conn.p()

                self.logger.warn("new connection from %s" % str(net_addr))
                self.active_connections.append(new_conn)
                self.cReader.addConnection(new_conn)

                try:
                    self.handler.setup_new_connection(new_conn)
                except:
                    pass
        return task.cont

    def handle_data(self, dg):
        self.handler.handle_packet(dg)
