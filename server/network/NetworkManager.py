from panda3d.core import QueuedConnectionManager
from lib.logging.Logger import Logger


class NetworkManager(QueuedConnectionManager):
    logger = Logger("NetworkManager")

    def __init__(self):
        QueuedConnectionManager.__init__(self)

    def get_uid(self, name):
        return "%s-%d" % (name, id(self))
