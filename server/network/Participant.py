from panda3d.core import NetDatagram, DatagramIterator

from lib.logging.Logger import Logger


class Participant:
    logger = Logger("network_participant")

    def __init__(self, parent, rendezvous, addr, connection, channel=None):
        self.parent = parent
        self.rendezvous = rendezvous
        self.addr = addr
        self.connection = connection
        self.channel = channel

        self.data = []

        self.update_task = None

    def configure(self):
        if self.update_task is None:
            self.update_task = taskMgr.add(self.update_data, "update-handler")

    def register_channel(self, channel):
        # TODO - register channels with the MessageDirector
        pass

    def unregister_channel(self, channel):
        # TODO - unregister channels from the MessageDirector

    def add_data(self, dg):
        if dg not in self.data or dg.getLength() is not None:
            self.data.append(dg)

    def update_data(self, task):
        if len(self.data) is not None:
            dg = self.data.pop()  # get the most recent datagram from the list
            dgi = DatagramIterator(dg)

            if dgi.getRemainingSize() is None:
                return task.cont
            
            self.handle_datagram(dgi, dg)

            return task.cont
        
    def handle_datagram(self, dgi, dg):
        # should be overridden by inheritors
        pass
