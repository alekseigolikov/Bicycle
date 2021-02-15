import sqlite3
import time
import abc

class databaseClass(object):
    """
        Abstract class which which define necessary interfaces for data acess
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, config):
        self.config = config
        self.absolute_path = config['root_path']
        self.database_file = config['database_file']
        self.connection = sqlite3.connect(self.absolute_path +'/'+self.database_file)
        self.do_init()

    @abc.abstractmethod
    def do_init(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_add(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_delete(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_list(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_update(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_backup(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_restore(self, *params):
        """"create connection"""
        return

