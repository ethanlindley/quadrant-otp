from panda3d.core import NetAddress, PointerToConnection

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
        self.handler = MDHandler(self.host, self.port)  # instantiate our handler

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
        return task.cont

    def handle_data(self, dg):
        self.handler.handle_packet(dg)
