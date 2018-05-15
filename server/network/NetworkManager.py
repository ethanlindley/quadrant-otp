from panda3d.core import QueuedConnectionManager
from lib.logging.Logger import Logger


class NetworkManager(QueuedConnectionManager):
    notify = Logger('NetworkManager')

    def __init__(self):
        QueuedConnectionManager.__init__(self)
