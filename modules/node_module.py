from . import RestAPIInterface
from configuration_class import *
from database_class import *

class NodeRequestHandler(RestAPIInterface):
    def __init__(self,  *params):
        self.__config = configurationClass().config
        self.__database = nodeDatabase(self.__config)

    def check_connection(self):
        pass

    def add_node(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_add(data_dict['name'], data_dict['address'], data_dict['ssh_key'])

    def delete_node(self, json_data):
        data_dict = json.loads(json_data)
        if self.__config['name']==data_dict['name']:
            return None
        return self.__database.do_delete(data_dict['name'])

    def update_node(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_update(data_dict['name'], data_dict['address'], data_dict['ssh_key'])

    def get_node(self, json_data):
        node_name = None
        if json_data is not None:
            data_dict = json.loads(json_data)
            node_name = data_dict['name']
        return self.__database.do_get(node_name)

    def who_am_i(self):
        """"Find instance hosntname"""
        return self.__config['name']

    def who_is_master(self):
        """"Find master node"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[0]

    def get_master_address(self):
        """"Find master node address"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[1]

    def i_am_master(self):
        """"Check is this instance a master"""
        my_name = self.who_am_i()
        master_name = self.who_is_master()
        return my_name == master_name

    def nodelist_to_json(self, node_list):
        if node_list is None or node_list==[]:
            return None
        output = '{'
        node_dict = {}
        for node in node_list:
            node_dict['name'] = node[0]
            node_dict['address'] = node[1]
            node_dict['votes'] = node[2]
            node_dict['timestamp'] = node[3]
            node_dict['deployment'] = node[4]
            node_dict['ssh_key'] = node[5]
            output += json.dumps(node_dict, indent = 4)
            output += ','
            node_dict = {}
        output = output[:-1]
        output += '}'
        return output

    def do_ADD(self, full_uri, body_data):
        """"Add node"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return(302, master_address)

        self.add_node(body_data)
        return (201, "Object added")

    def do_GET(self, full_uri, body_data):
        """"List nodes"""
        node_list = self.get_node(body_data)
        node_json = self.nodelist_to_json(node_list)
        if node_json is not None:
            return (201, node_json)
        return (404, None)

    def do_POST(self, full_uri, body_data):
        """"Alternative method for update node"""
        return

    def do_PUT(self, full_uri, body_data):
        """"Alternative method for add node"""
        return

    def do_DELETE(self, full_uri, body_data):
        """"Delete node"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        output = self.delete_node(body_data)
        if output is not None:
            return (201, "Object deleted")
        return(500, "Object deletition failed")

    def do_UPDATE(self, full_uri, body_data):
        """"Update node"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        self.update_node(body_data)
        return (201, "Object updated")

class nodeDatabase(databaseClass):
    def do_init(self):
        cursor = self.connection.cursor()
        print("Starting DATABASE Initialization")
        cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (name text, address text, votes real, timestamp integer, deployment text, ssh_key text)''')
        self.connection.commit()
        self.do_data_init()

    def do_data_init(self):
        cursor = self.connection.cursor()
        nodes_list = self.do_list_deployment()
        my_config = configurationClass().config
        now_time = int(time.time())
        if nodes_list == []:
            print("Starting MY DATA Initialization")
            sql = '''INSERT INTO nodes (name , address, votes , timestamp , deployment , ssh_key ) values (?,?,?,?,?,?)'''
            cursor.execute(sql, [my_config['name'],my_config['address'], 0, now_time, 'RUNNING', my_config['ssh_key']])
            self.connection.commit()


    def get_master(self):
        cursor = self.connection.cursor()
        sql = '''select * from nodes order by votes desc limit 1'''
        cursor.execute(sql)
        return_rows = cursor.fetchone()
        return return_rows

    def do_add(self, node_name, address, ssh_key):
        cursor = self.connection.cursor()
        now_time = int(time.time())
        sql = '''INSERT INTO nodes (name ,address, votes , timestamp , deployment , ssh_key ) values (?,?,?,?,?,?)'''
        cursor.execute(sql,[node_name, address, 0, now_time, 'ADD', ssh_key])
        self.connection.commit()
        return 1

    def do_delete(self, node_name):
        cursor = self.connection.cursor()
        now_time = int(time.time())
        sql = "UPDATE nodes set deployment='DELETE' where name = '{}'".format(node_name)
        cursor.execute(sql)
        self.connection.commit()
        return 1

    def do_list_deployment(self, deployment = None):
        cursor = self.connection.cursor()
        if deployment is not None:
            sql = '''SELECT * FROM nodes where deployment = ?'''
            cursor.execute(sql, node_name)
        else:
            sql = '''SELECT * FROM nodes'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows

    def do_get(self, node_name = None):
        cursor = self.connection.cursor()
        if node_name is not None:
            print("GETTING NODENAME {}".format(node_name))
            sql = "SELECT * FROM nodes where name = '{}'".format(node_name)
            print("GETTING NODENAME {}".format(sql))
            cursor.execute(sql)
        else:
            sql = '''SELECT * FROM nodes'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows


    def do_update(self, name, address, ssh_key):
        cursor = self.connection.cursor()
        sql = '''UPDATE nodes SET address = ?,  deployment = ?, ssh_key = ? WHERE name = ?'''
        cursor.execute(sql, [address, votes, 'UPDATE', ssh_key ])
        self.connection.commit()
        return 1

    def do_backup(self):
        pass

    def do_restore(self):
        pass