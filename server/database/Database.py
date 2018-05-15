from lib.datagram.DatagramIterator import DatagramIterator
from lib.logging.Logger import Logger
from collections import defaultdict


class Database:
    notify = Logger('Database')

    # TODO - possibly use a more secure, stable, and faster db system, such as mongo or mysql
    def __init__(self, db=None):
        self.db = db if db is not None else defaultdict(list)

    def load_database(self, db_file):
        # TODO - dynamically load database files from config
        pass

    def add_user(self, dg):
        # TODO - check if a user with desired username already exists in db
        dgi = DatagramIterator(dg)
        uname = dgi.get_string()
        pword = dgi.get_string()

        uid = len(self.db) + 1
        self.db[uid].append(uname)
        self.db[uid].append(pword)
