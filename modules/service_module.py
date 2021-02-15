from . import RestAPIInterface
from configuration_class import *
from database_class import *

class ServiceRequestHandler(RestAPIInterface):
    def __init__(self,  *params):
        self.__config = configurationClass().config
        self.__database = serviceDatabase(self.__config)

    def check_connection(self):
        pass

    def add_service(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_add(data_dict['service'], data_dict['replicas'], data_dict['min_replicas'], data_dict['status'])

    def delete_service(self, json_data):
        data_dict = json.loads(json_data)
        if self.service_exists(json_data):
            return self.__database.do_delete(data_dict['service'])
        return None

    def update_service(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_update(data_dict['service'], data_dict['replicas'], data_dict['min_replicas'], data_dict['status'])

    def get_service(self, json_data):
        service_name = None
        if json_data is not None:
            data_dict = json.loads(json_data)
            service_name = data_dict['service']
        return self.__database.do_get(service_name)

    def service_exists(self, json_data):
        list = self.get_service(json_data)
        if len(list) == 0:
            return False
        return True

    def who_am_i(self):
        """"Find instance hosntname"""
        return self.__config['name']

    def who_is_master(self):
        """"Find master service"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[0]

    def get_master_address(self):
        """"Find master service address"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[1]

    def i_am_master(self):
        """"Check is this instance a master"""
        my_name = self.who_am_i()
        master_name = self.who_is_master()
        return my_name == master_name

    def servicelist_to_json(self, service_list):
        if service_list is None or service_list==[]:
            return None
        output = '{'
        service_dict = {}
        for service in service_list:
            service_dict['service'] = service[0]
            service_dict['replicas'] = service[1]
            service_dict['min_replicas'] = service[2]
            service_dict['status'] = service[3]
            service_dict['deployment'] = service[4]
            output += json.dumps(service_dict, indent = 4)
            output += ','
            service_dict = {}
        output = output[:-1]
        output += '}'
        return output

    def do_ADD(self, full_uri, body_data):
        """"Add service"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return(302, master_address)

        self.add_service(body_data)
        return (201, "Object added")

    def do_GET(self, full_uri, body_data):
        """"List services"""
        service_list = self.get_service(body_data)
        service_json = self.servicelist_to_json(service_list)
        if service_json is not None:
            return (201, service_json)
        return (404, None)

    def do_POST(self, full_uri, body_data):
        """"Alternative update service"""
        return

    def do_PUT(self, full_uri, body_data):
        """"Alternative add service"""
        return

    def do_DELETE(self, full_uri, body_data):
        """"Delete service"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        output = self.delete_service(body_data)
        if output is not None:
            return (201, "Object deleted")
        return(500, "Object deletition failed")

    def do_UPDATE(self, full_uri, body_data):
        """"Update service"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        self.update_service(body_data)
        return (201, "Object updated")

class serviceDatabase(databaseClass):
    def do_init(self):
        cursor = self.connection.cursor()
        print("Starting DATABASE Initialization")
        cursor.execute('''CREATE TABLE IF NOT EXISTS services (service text, replicas integer, min_replicas integer, status text, deployment text)''')
        self.connection.commit()


    def get_master(self):
        cursor = self.connection.cursor()
        sql = '''select * from nodes order by votes desc limit 1'''
        cursor.execute(sql)
        return_rows = cursor.fetchone()
        return return_rows

    def do_add(self, service, replicas, min_replicas, status):
        cursor = self.connection.cursor()
        sql = '''INSERT INTO services (service , replicas , min_replicas , status ,deployment) values (?,?,?,?,?)'''
        cursor.execute(sql,[service, replicas, min_replicas, status, 'ADD'])
        self.connection.commit()
        return 1

    def do_delete(self, service):
        cursor = self.connection.cursor()
        sql = "UPDATE services set deployment='DELETE' where service = '{}'".format(service)
        cursor.execute(sql)
        self.connection.commit()
        return 1

    def do_list_deployment(self, deployment = None):
        cursor = self.connection.cursor()
        if deployment is not None:
            sql = '''SELECT * FROM services where deployment = ?'''
            cursor.execute(sql, deployment)
        else:
            sql = '''SELECT * FROM services'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows

    def do_get(self, service = None):
        cursor = self.connection.cursor()
        if service is not None:
            print("GETTING INAGE {}".format(service))
            sql = "SELECT * FROM services where service = '{}'".format(service)
            print("GETTING service {}".format(sql))
            cursor.execute(sql)
        else:
            sql = '''SELECT * FROM services'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows

    def do_update(self, service, replicas, min_replicas, status):
        cursor = self.connection.cursor()
        sql = '''UPDATE services SET replicas = ?,  min_replicas = ?, status = ? deployment = ? WHERE service = ?'''
        cursor.execute(sql, [replicas, min_replicas, status, 'UPDATE', service])
        self.connection.commit()
        return 1


    def do_backup(self):
        pass

    def do_restore(self):
        pass