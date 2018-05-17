from server.network.Listener import Listener
from lib.logging.Logger import Logger


class MessageDirector(Listener):
    logger = Logger("message_director")

    def __init__(self, host_addr, port, backlog=10000):
        Listener.__init__(self, host_addr, port, backlog)

    def setup(self):
        Listener.configure(self)
        self.logger.info("protocol online")
