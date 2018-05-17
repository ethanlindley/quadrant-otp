from panda3d.core import loadPrcFile, ConfigVariableString
ConfigVariableString("window-type","none").setValue("none")
from direct.showbase.ShowBase import ShowBase

from server.message_director.MessageDirector import MessageDirector
from server.client_agent.ClientAgent import ClientAgent
from lib.logging.Logger import Logger

class ServerStart(ShowBase):
    logger = Logger("ServerStart")

    def __init__(self):
        ShowBase.__init__(self)
        self.start_protocols()

    def start_protocols(self):
        # TODO - receive server params from config?
        # let's instantiate our server protocols and set them up accordingly
        md = MessageDirector("127.0.0.1", 7000)
        ca = ClientAgent("127.0.0.1", 7000, 7001)

        md.setup_server()
        ca.setup_server()


start = ServerStart()
start.run()
