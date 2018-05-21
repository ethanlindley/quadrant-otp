import thread

from panda3d.core import ConfigVariableString
ConfigVariableString("window-type", "none").setValue("none")
from direct.showbase.ShowBase import ShowBase

from server.client_agent.ClientAgent import ClientAgent
from server.message_director.MessageDirector import MessageDirector
from lib.logging.Logger import Logger


class ServerStart(ShowBase):
    logger = Logger("server_start")

    def __init__(self):
        ShowBase.__init__(self)
        self.start_servers()

    def start_servers(self):
        host = "127.0.0.1"
        md_port = 6660
        ca_port = 6667

        md = MessageDirector(md_port)
        md.configure()
        
        ca = ClientAgent(ca_port, md_port)
        ca.configure()


server = ServerStart()
server.run()
