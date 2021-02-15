from . import RestAPIInterface
from configuration_class import *
from database_class import *

class ImageRequestHandler(RestAPIInterface):
    def __init__(self,  *params):
        self.__config = configurationClass().config
        self.__database = imageDatabase(self.__config)

    def check_connection(self):
        pass

    def add_image(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_add(data_dict['repository'], data_dict['tag'], data_dict['image'])

    def delete_image(self, json_data):
        data_dict = json.loads(json_data)
        if self.image_exists(json_data):
            return self.__database.do_delete(data_dict['image'])
        return None

    def update_image(self, json_data):
        data_dict = json.loads(json_data)
        return self.__database.do_update(data_dict['repository'], data_dict['tag'], data_dict['image'])

    def get_image(self, json_data):
        image_name = None
        if json_data is not None:
            data_dict = json.loads(json_data)
            image_name = data_dict['image']
        return self.__database.do_get(image_name)

    def image_exists(self, json_data):
        list = self.get_image(json_data)
        if len(list) == 0:
            return False
        return True

    def who_am_i(self):
        """"Find instance hosntname"""
        return self.__config['name']

    def who_is_master(self):
        """"Find master image"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[0]

    def get_master_address(self):
        """"Find master image address"""
        master_data = self.__database.get_master()
        print("DATA {}".format(master_data))
        return master_data[1]

    def i_am_master(self):
        """"Check is this instance a master"""
        my_name = self.who_am_i()
        master_name = self.who_is_master()
        return my_name == master_name

    def imagelist_to_json(self, image_list):
        if image_list is None or image_list==[]:
            return None
        output = '{'
        image_dict = {}
        for image in image_list:
            image_dict['repository'] = image[0]
            image_dict['tag'] = image[1]
            image_dict['image'] = image[2]
            image_dict['deployment'] = image[3]
            output += json.dumps(image_dict, indent = 4)
            output += ','
            image_dict = {}
        output = output[:-1]
        output += '}'
        return output

    def do_ADD(self, full_uri, body_data):
        """"Add image"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return(302, master_address)

        self.add_image(body_data)
        return (201, "Object added")

    def do_GET(self, full_uri, body_data):
        """"List images"""
        image_list = self.get_image(body_data)
        image_json = self.imagelist_to_json(image_list)
        if image_json is not None:
            return (201, image_json)
        return (404, None)

    def do_POST(self, full_uri, body_data):
        """"Alternative update image"""
        return

    def do_PUT(self, full_uri, body_data):
        """"Alternative add image"""
        return

    def do_DELETE(self, full_uri, body_data):
        """"Delete image"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        output = self.delete_image(body_data)
        if output is not None:
            return (201, "Object deleted")
        return(500, "Object deletition failed")

    def do_UPDATE(self, full_uri, body_data):
        """"Update image"""
        if not self.i_am_master():
            master_address = self.get_master_address()
            return (302, master_address)

        self.update_image(body_data)
        return (201, "Object updated")

class imageDatabase(databaseClass):
    def do_init(self):
        cursor = self.connection.cursor()
        print("Starting DATABASE Initialization")
        cursor.execute('''CREATE TABLE IF NOT EXISTS images (repository text, tag text, image text, deployment text)''')
        self.connection.commit()


    def get_master(self):
        cursor = self.connection.cursor()
        sql = '''select * from nodes order by votes desc limit 1'''
        cursor.execute(sql)
        return_rows = cursor.fetchone()
        return return_rows

    def do_add(self, repository, tag, image):
        cursor = self.connection.cursor()
        sql = '''INSERT INTO images (repository , tag , image , deployment ) values (?,?,?,?)'''
        cursor.execute(sql,[repository, tag, image, 'ADD'])
        self.connection.commit()
        return 1

    def do_delete(self, image):
        cursor = self.connection.cursor()
        sql = "UPDATE images set deployment='DELETE' where image = '{}'".format(image)
        cursor.execute(sql)
        self.connection.commit()
        return 1

    def do_list_deployment(self, deployment = None):
        cursor = self.connection.cursor()
        if deployment is not None:
            sql = '''SELECT * FROM images where deployment = ?'''
            cursor.execute(sql, deployment)
        else:
            sql = '''SELECT * FROM images'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows

    def do_get(self, image = None):
        cursor = self.connection.cursor()
        if image is not None:
            print("GETTING INAGE {}".format(image))
            sql = "SELECT * FROM images where image = '{}'".format(image)
            print("GETTING IMAGE {}".format(sql))
            cursor.execute(sql)
        else:
            sql = '''SELECT * FROM images'''
            cursor.execute(sql)
        return_rows = cursor.fetchall()
        return return_rows


    def do_update(self, repository, tag, image):
        cursor = self.connection.cursor()
        sql = '''UPDATE images SET repository = ?,  tag = ?, image = ? deployment = ? WHERE image = ?'''
        cursor.execute(sql, [repository, tag, image, 'UPDATE', image])
        self.connection.commit()
        return 1


    def do_backup(self):
        pass

    def do_restore(self):
        pass