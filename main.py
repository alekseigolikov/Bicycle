# !/usr/bin/python

import string
import argparse
from http.server import *
from modules.node_module import *
from modules.logs_module import *
from modules.conf_module import *
from modules.vote_module import *
from modules.stats_module import *
from modules.state_module import *
from modules.container_module import *
from modules.image_module import *
from modules.service_module import *
from configuration_class import *
import os
import http
import uuid


class ServerClass(HTTPServer):
    """
        Server class inherits from httpserver class,
        overloading constructor in order to store some specific info
        intended to be used for server instance creation
    """

    def __init__(self, *args, **kwargs):
        """
            :param keep_going: Boolean value defining should server continue to run or stop
            :param root_path: root path if server / address of another hop if proxy
            :param data_source: data access type defining protocol of accessing data local or remote
        """
        print("initiing server")
        (config, handlerObj) = args
        HTTPServer.__init__(self, (config['address'], int(config['port'])), handlerObj)
        print("initiing server {}:{}".format(config['address'], int(config['port'])))
        self.keep_going = config['keep_going']
        self.root_path = config['root_path']
        self.magic_string = config['magic_string']
        self.config = config
        print("Init Server class")



class RequestsHandlerClass(BaseHTTPRequestHandler):
    """
        Handler class for http server holding scenarios for answers generation
    """
    def __init__(self, *args, **kwargs):
        print("Init request handler")
        self.__handler = handler_factory()
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)


    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _parse_uri(self):
        path_pieces = self.path.split('/')
        return (path_pieces)

    def _get_handler(self, request):
        output = self.__handler['default']
        if request in self.__handler:
            print("REQUEST MATCHED {}".format(request))
            output = self.__handler[request]
        print("REQUEST DID NOT MATCH {}".format(request))
        return output

    def _get_uri_data(self):
        uri = self.path
        body_data = None
        if self.headers['Content-Length'] is not None:
            content_length = int(self.headers['Content-Length'])
            if content_length > 0:
                body_data = self.rfile.read(content_length)
        return (uri, body_data)


    def do_ADD(self):
        uri = self._parse_uri()
        (full_uri, body_data) = self._get_uri_data()
        handler = self._get_handler(uri[1])
        (status_code, status_text) = handler.do_ADD(full_uri, body_data)
        self.send_response(status_code)
        if status_code == 302:
            print("REDIRECTING TO {}".format(status_text) )
            self.send_header("Location", "http://" + format(status_text) + "/ADD/")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(status_text.encode())

    def do_DELETE(self):
        uri = self._parse_uri()
        (full_uri, body_data) = self._get_uri_data()
        handler = self._get_handler(uri[1])
        (status_code, status_text) = handler.do_DELETE(full_uri, body_data)
        self.send_response(status_code)
        if status_code == 302:
            print("REDIRECTING TO {}".format(status_text))
            self.send_header("Location", "http://" + format(status_text) + "/ADD/")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(status_text.encode())

    def do_PUT(self):
        pass

    def do_GET(self):
        uri = self._parse_uri()
        (full_uri, body_data) = self._get_uri_data()
        handler = self._get_handler(uri[1])
        (status_code, status_text) = handler.do_GET(full_uri, body_data)
        if status_code == 404 or status_text is None:
            status_code = 404
            status_text = 'Requested object is not found'
        self.send_response(status_code)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(status_text.encode())

    def do_UPDATE(self):
        uri = self._parse_uri()
        (full_uri, body_data) = self._get_uri_data()
        handler = self._get_handler(uri[1])
        (status_code, status_text) = handler.do_UPDATE(full_uri, body_data)
        self.send_response(status_code)
        if status_code == 302:
            print("REDIRECTING TO {}".format(status_text))
            self.send_header("Location", "http://" + format(status_text) + "/ADD/")
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(status_text.encode())

    def do_POST(self):
        pass


def handler_factory():
    print("Init factory")
    return {"node": NodeRequestHandler(),
            "service": ServiceRequestHandler(),
            "conf": ConfRequestHandler(),
            "image": ImageRequestHandler(),
            "container": ContainerRequestHandler(),
            "stats": StatsRequestHandler(),
            "logs": LogsRequestHandler(),
            "vote": VoteRequestHandler(),
            "default": NodeRequestHandler(),
            "state":StateRequestHandler()
            }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(usage='Usage: %(prog)s -M <mode> -p <port> -h <host> [options] -r <root_path>')
    parser.add_argument('-M', dest='mode', action='store', help='Mode to run, possible values: ''server'',''cli'',''proxy'',''test''', default='server')
    parser.add_argument('-H', dest='address', action='store', help='Host to listen/interact to', default='localhost')
    parser.add_argument('-p', dest='port', action='store', help='Port to listen/interact to', default='9979')
    parser.add_argument('-k', dest='ssh_key', action='store', help='Ssh key for bootstraping', default='')
    parser.add_argument('-N', dest='name', action='store', help='name assigned in nodelist', default=uuid.uuid4().hex[:32].upper())
    parser.add_argument('-c', dest='config_filename', action='store', help='cofniguration file name', default='config.json' )
    parser.add_argument('-D', dest='database_file', action='store', help='Database file', default='database.db')
    parser.add_argument('-r', dest='root_path', action='store', help='Path where documents are stored, in proxy mode it holds url of main server', default=os.path.abspath(os.getcwd()))
    parser.add_argument('-q', dest='query', action='store', help='query string example:''retrieve 123''', default='list')
    parser.add_argument('-m', dest='magic_string', action='store',  help='Magic string sent as query will lead to stop server', default='StopServerNow')
    opts = parser.parse_args()

    config_object = configurationClass(opts.config_filename, opts.root_path)
    config = config_object.get_config()
    configurationClass.config = config

    if opts.mode in ('server', 'proxy'):
        server_object = ServerClass(config, RequestsHandlerClass)
        print('Starting Up serverr')
        while (server_object.keep_going):
            print("Going")
            server_object.handle_request()
        print('Stoping serverr')
        server_object.server_close()

    if opts.mode == 'cli':
        cli_object = CLIClass({'address': opts.address, 'port': opts.port, 'path': opts.root_path, 'query': opts.query,
                               'magic_string': opts.magic_string})
        output =  cli_object.do_action()
        print(output)



