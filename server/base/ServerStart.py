from panda3d.core import ConfigVariableString
ConfigVariableString("window-type","none").setValue("none")
from direct.showbase.ShowBase import ShowBase

from server.client_agent.ClientAgent import ClientAgent
from server.message_director.MessageDirector import MessageDirector
from lib.logging.Logger import Logger


class ServerStart(ShowBase):
    logger = Logger("server_start")

    def __init__(self):
        ShowBase.__init__(self)
        self.start()

    def start(self):
        md = MessageDirector("127.0.0.1", 6667)
        ca = ClientAgent("127.0.0.1", 6667, 6668)

        md.setup()
        ca.setup()


start = ServerStart()
start.run()
