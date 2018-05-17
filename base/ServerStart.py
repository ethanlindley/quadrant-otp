from panda3d.core import ConfigVariableString
ConfigVariableString("window-type","none").setValue("none")
from direct.showbase.ShowBase import ShowBase

from lib.logging.Logger import Logger


class ServerStart(ShowBase):
    logger = Logger("server_start")

    def __init__(self):
        ShowBase.__init__(self)
        self.start()

    def start(self):
        # TODO - instantiate protocols
        pass


start = ServerStart()
start.run()
