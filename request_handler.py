from http.server import BaseHTTPRequestHandler, HTTPServer
from categories import create_category, get_all_categories
from comments import create_comment
from users import register_new_user, get_user_by_email


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
            ( resource, id ) = parsed
            if resource.lower() == "categories":
                response = get_all_categories()

        else:
            # we got query params!
            (resource, key, value) = parsed
            if resource.lower() == "users" and key.lower() == "email":
                response = get_user_by_email(value)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        parsed = self.parse_url(self.path)
        resource = parsed[0].lower()

        if resource == "register":
            # if the user specified by the email in the post body does exist:
            if get_user_by_email(post_body['email']) is None:
                self._set_headers(201) # STATUS CREATED
                new_user = register_new_user(post_body)
                self.wfile.write(json.dumps(new_user).encode())
            else:
                self._set_headers(409) # STATUS CONFLICT (used here to indicate it already exists)
                self.wfile.write(json.dumps("User already exists.").encode())

        if resource == "categories":
            self._set_headers(201) # STATUS CREATED
            new_category = create_category(post_body)
            self.wfile.write(json.dumps(new_category).encode())
        elif resource == "comments":
            self._set_headers(201) # STATUS CREATED
            new_comment = create_comment(post_body)
            self.wfile.write(json.dumps(new_comment).encode())


    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "categories":
            success = True
        
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
        
        self.wfile.write("".encode())

    def do_DELETE(self):
        # TODO
        pass


def main():
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
