from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from users.request import create_new_user, get_user_by_email


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:

            param = resource.split("?")[1]
            resource = resource.split("?")[0]
            pair = param.split("=")
            key = pair[0]
            value = pair[1]

            return (resource, key, value)

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass
            except ValueError:
                pass

            return (resource, id)

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
        self._set_headers(200) # STATUS OKAY
        response = {}
        parsed = self.parse_url(self.path)

        if len(parsed) <= 2:
            # no query params
            pass
            # (resource, id) = parsed
        else:
            # we got query params!
            (resource, key, value) = parsed
            if resource.lower() == "users" and key.lower() == "email":
                response = get_user_by_email(value)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        self._set_headers(201) # STATUS CREATED
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        # Co
        post_body = json.loads(post_body)

        parsed = self.parse_url(self.path)
        resource = parsed[0]
        new_thing = None
        if resource.lower() == "users":
            new_thing = create_new_user(post_body)
        
        self.wfile.write(json.dumps(new_thing).encode())

    def do_PUT(self):
        # TODO
        pass

    def do_DELETE(self):
        # TODO
        pass


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
