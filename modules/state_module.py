from . import RestAPIInterface
from configuration_class import *
from database_class import *
from .image_module import *
from .container_module import *
from .node_module import *
from .service_module import *


class StateRequestHandler(RestAPIInterface):
    def __init__(self,  *params):
        self.__config = configurationClass().config
        self.__database = stateDatabase(self.__config)
        self.__node = NodeRequestHandler()
        self.__container = ContainerRequestHandler()
        self.__image = ImageRequestHandler()
        self.__service = ServiceRequestHandler()

    def check_connection(self):
        pass

    def get_node_list(self, full_uri, body_data):
        (return_status, return_body) = self.__node.do_GET(full_uri, body_data)
        return return_body

    def get_service_list(self, full_uri, body_data):
        (return_status, return_body) = self.__service.do_GET(full_uri, body_data)
        return return_body

    def get_image_list(self, full_uri, body_data):
        (return_status, return_body) = self.__image.do_GET(full_uri, body_data)
        return return_body

    def get_container_list(self, full_uri, body_data):
        (return_status, return_body) = self.__container.do_GET(full_uri, body_data)
        return return_body

    def get_state_list(self, full_uri, body_data):
        node_list = self.get_node_list(full_uri, body_data)
        service_list = self.get_service_list(full_uri, body_data)
        image_list = self.get_image_list(full_uri, body_data)
        container_list = self.get_container_list(full_uri, body_data)
        output_json = '{'
        output_json += '"nodes":' + format(node_list) + ","
        output_json += '"images":' + format(image_list) + ","
        output_json += '"containers":' + format(container_list) + ","
        output_json += '"services":' + format(service_list) + ","
        output_json += '}'
        return output_json

    def who_am_i(self):
        """"Find instance hosntname"""
        return self.__config['name']


    def do_ADD(self, full_uri, body_data):
        """"Add node"""
        return(500, "Method is not supported")

    def do_GET(self, full_uri, body_data):
        """"List nodes"""
        state_output = self.get_state_list(full_uri, body_data)
        return (201, state_output)

    def do_POST(self, full_uri, body_data):
        """"Alternative method for update node"""
        return(500, "Method is not supported")

    def do_PUT(self, full_uri, body_data):
        """"Alternative method for add node"""
        return(500, "Method is not supported")

    def do_DELETE(self, full_uri, body_data):
        """"Delete node"""

        return(500, "Method is not supported")

    def do_UPDATE(self, full_uri, body_data):
        """"Update node"""
        return(500, "Method is not supported")

class stateDatabase(databaseClass):
    def do_init(self):
        cursor = self.connection.cursor()
        print("Starting DATABASE Initialization")
        cursor.execute('''CREATE TABLE IF NOT EXISTS nodes (name text, address text, votes real, timestamp integer, deployment text, ssh_key text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS services (service text, replicas integer, min_replicas integer, status text, deployment text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS images (repository text, tag text, image text, deployment text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS containers (container text, image text, command text, status text, ports text, names text, deployment text)''')
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
