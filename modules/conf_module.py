from . import RestAPIInterface
class ConfRequestHandler(RestAPIInterface):
    def __init__(self,  *params):
        pass

    def check_connection(self):
        """"create connection"""
        return

    def do_ADD(self, *params):
        """"create connection"""
        print("YAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA CONFFFFFFFFFFFF")
        #conn = sqlite3.connect('example.db')
        #c = conn.cursor()
        # Create table
        #c.execute('''CREATE TABLE stocks
        #             (date text, trans text, symbol text, qty real, price real)''')

        # Insert a row of data
        #c.execute("INSERT INTO stocks VALUES ('2006-01-05','BUY','RHAT',100,35.14)")

        # Save (commit) the changes
        #conn.commit()

        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        #conn.close()
        return 1

    def do_GET(self, *params):
        """"create connection"""
        return

    def do_POST(self, *params):
        """"create connection"""
        return

    def do_DELETE(self, *params):
        """"create connection"""
        return

    def do_UPDATE(self, *params):
        """"create connection"""
        return
