from panda3d.core import loadPrcFile, ConfigVariableString
ConfigVariableString("window-type","none").setValue("none")
from direct.showbase.ShowBase import ShowBase

from server.network.NetworkListener import NetworkListener
from lib.logging.Logger import Logger

class ServerStart(ShowBase):
    logger = Logger("ServerStart")

    def __init__(self):
        ShowBase.__init__(self)
        self.start_server()

    def start_server(self):
        # TODO - receive server params from config?
        server = NetworkListener("127.0.0.1", 6667)
        server.setup_socket()


start = ServerStart()
start.run()
