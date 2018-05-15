from direct.directnotify.DirectNotifyGlobal import directNotify


class Logger:
    def __init__(self, name):
        self.name = name
        self.logger = directNotify.newCategory(self.name)

    def debug(self, msg):
        print("%s [debug] :: %s" % (self.name, msg))

    def info(self, msg):
        print("%s [info] :: %s" % (self.name, msg))

    def warn(self, msg):
        print("%s [warn] :: %s" % (self.name, msg))
