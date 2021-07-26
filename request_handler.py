from http.server import BaseHTTPRequestHandler, HTTPServer
import json


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

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
        self._set_headers(200)
        response = {}
        parsed = self.parse_url(self.path)

        if len(parsed) <= 2:
            # no query params
            pass
            # (resource, id) = parsed
        else:
            # we got query params!
            (resource, key, value) = parsed
            if resource.lower() == "users" AND key.lower() == "email":
                response = get_user_by_email(value)

        self.wfile.write(json.dumps(response).encode())




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