import thread

from panda3d.core import ConfigVariableString
ConfigVariableString("window-type", "none").setValue("none")
from direct.showbase.ShowBase import ShowBase

from server.message_director.MessageDirector import MessageDirector
from lib.logging.Logger import Logger


class ServerStart(ShowBase):
    logger = Logger("server_start")

    def __init__(self):
        ShowBase.__init__(self)
        self.start_threads()
    
    def start_threads(self):
        thread.start_new_thread(self.start_md, ("127.0.0.1", 6667))

    def start_md(self, host, port):
        md = MessageDirector(host, port)
        md.configure()


server = ServerStart()
server.run()
