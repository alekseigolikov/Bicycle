from . import RestAPIInterface
from configuration_class import *
from database_class import *

class ContainerRequestHandler(RestAPIInterface):
    def __init__(self,  *params):
        self.__config = configurationClass().config
        self.__database = containerDatabase(self.__config)

    def check_connection(self):
        pass

    def add_container(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_add(data_dict['container'], data_dict['image'], data_dict['command'], data_dict['ports'], data_dict['names'])

    def delete_container(self, json_data):
        data_dict = json.loads(json_data)
        if self.container_exists(json_data):
            return self.__database.do_delete(data_dict['container'])
        return None

    def update_container(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_update(data_dict['container'], data_dict['image'], data_dict['command'], data_dict['status'], data_dict['ports'], data_dict['names'])

    def get_container(self, json_data):
        container_name = None
        if json_data is not None:
            data_dict = json.loads(json_data)
            container_name = data_dict['container']
        return self.__database.do_get(container_name)

    def container_exists(self, json_data):
        list = self.get_container(json_data)
        if len(list) == 0:
            return False
        return True

    def who_am_i(self):
        """"Find instance hosntname"""
        return self.__config['name']

    def who_is_master(self):
        """"Find master container"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[0]

    def get_master_address(self):
        """"Find master container address"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[1]

    def i_am_master(self):
        """"Check is this instance a master"""
        my_name = self.who_am_i()
        master_name = self.who_is_master()
        return my_name == master_name

    def containerlist_to_json(self, container_list):
        if container_list is None or container_list==[]:
            return None
        output = '{'
        container_dict = {}
        for container in container_list:
            container_dict['container'] = container[0]
            container_dict['image'] = container[1]
            container_dict['command'] = container[2]
            container_dict['status'] = container[3]
            container_dict['ports'] = container[4]
            container_dict['names'] = container[5]
            container_dict['deployment'] = container[6]
            output += json.dumps(container_dict, indent = 4)
            output += ','
            container_dict = {}
        output = output[:-1]
        output += '}'
        return output

    def do_ADD(self, full_uri, body_data):
        """"Add container"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return(302, master_address)

        self.add_container(body_data)
        return (201, "Object added")

    def do_GET(self, full_uri, body_data):
        """"List containers"""
        container_list = self.get_container(body_data)
        container_json = self.containerlist_to_json(container_list)
        if container_json is not None:
            return (201, container_json)
        return (404, None)

    def do_POST(self, full_uri, body_data):
        """"Alternative update container"""
        return

    def do_PUT(self, full_uri, body_data):
        """"Alternative add container"""
        return

    def do_DELETE(self, full_uri, body_data):
        """"Delete container"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        output = self.delete_container(body_data)
        if output is not None:
            return (201, "Object deleted")
        return(500, "Object deletition failed")

    def do_UPDATE(self, full_uri, body_data):
        """"Update container"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        self.update_container(body_data)
        return (201, "Object updated")

class containerDatabase(databaseClass):
    def do_init(self):
        cursor = self.connection.cursor()
        print("Starting DATABASE Initialization")
        cursor.execute('''CREATE TABLE IF NOT EXISTS containers (container text, image text, command text, status text, ports text, names text, deployment text)''')
        self.connection.commit()


    def get_master(self):
        cursor = self.connection.cursor()
        sql = '''select * from nodes order by votes desc limit 1'''
        cursor.execute(sql)
        return_rows = cursor.fetchone()
        return return_rows

    def do_add(self, container, image, command, ports, names):
        cursor = self.connection.cursor()
        sql = '''INSERT INTO containers (container , image , command , status , ports , names , deployment) values (?,?,?,?,?,?,?)'''
        cursor.execute(sql,[container, image, command, '', ports, names, 'ADD'])
        self.connection.commit()
        return 1

    def do_delete(self, container):
        cursor = self.connection.cursor()
        sql = "UPDATE containers set deployment='DELETE' where container = '{}'".format(container)
        cursor.execute(sql)
        self.connection.commit()
        return 1

    def do_list_deployment(self, deployment = None):
        cursor = self.connection.cursor()
        if deployment is not None:
            sql = '''SELECT * FROM containers where deployment = ?'''
            cursor.execute(sql, deployment)
        else:
            sql = '''SELECT * FROM containers'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows

    def do_get(self, container = None):
        cursor = self.connection.cursor()
        if container is not None:
            print("GETTING INAGE {}".format(container))
            sql = "SELECT * FROM containers where container = '{}'".format(container)
            print("GETTING container {}".format(sql))
            cursor.execute(sql)
        else:
            sql = '''SELECT * FROM containers'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows

    def do_update(self, container, image, command, status, ports, names):
        cursor = self.connection.cursor()
        sql = '''UPDATE containers SET image = ?,  command = ?, status = ?, ports = ?, names = ?,  deployment = ? WHERE container = ?'''
        cursor.execute(sql, [image, command, status, ports, names, 'UPDATE', container])
        self.connection.commit()
        return 1


    def do_backup(self):
        pass

    def do_restore(self):
        pass