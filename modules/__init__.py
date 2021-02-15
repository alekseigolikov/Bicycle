import abc
class RestAPIInterface(object):
    """
        Abstract class which which define necessary interfaces for data acess
    """
    __metaclass__ = abc.ABCMeta

    def __init(self):
        pass

    @abc.abstractmethod
    def check_connection(self):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_ADD(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_GET(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_POST(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_DELETE(self, *params):
        """"create connection"""
        return

    @abc.abstractmethod
    def do_UPDATE(self, *params):
        """"create connection"""
        return