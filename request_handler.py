from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        # TODO
        pass

    def _set_headers(self, status):
        """_set_headers is an internal method that sends the proper headers for a given status code

            Args:
                status (int): status code number (e.g. 200 for okay, 500 for server error)
            """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """do_OPTIONS responds to an OPTIONS request from the client
            """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        # TODO
        pass

    def do_POST(self):
        # TODO
        pass

    def do_PUT(self):
        # TODO
        pass

    def do_DELETE(self):
        # TODO
        pass


def main():
    host = ''
    port = 8088
    HTTPServer((host,port), HandleRequests).serve_forever()

if __name__ == "__main__":
    main()