import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from post_reactions.request import get_all_post_reactions
from categories.request import create_category, get_all_categories
from users.request import create_new_user, get_single_user, get_user_by_email
from posts.request import get_posts_by_user


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
            elif resource == "postreactions":
                response = get_all_post_reactions() 
            elif resource == "users":
                if id is not None:
                    response = get_single_user(id)

        else:
            # we got query params!
            (resource, key, value) = parsed
            if resource.lower() == "users" and key.lower() == "email":
                response = get_user_by_email(value)
            elif resource.lower() == "posts" and key.lower() == "user_id":
                response = get_posts_by_user(value)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):

        """Handles POST requests to the server
        """
        self._set_headers(201) # STATUS CREATED
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        # Co
        post_body = json.loads(post_body)

        parsed = self.parse_url(self.path)
        resource = parsed[0].lower()
        new_thing = None
        new_category = None
        if resource == "users":
            new_thing = create_new_user(post_body)
            self.wfile.write(json.dumps(new_thing).encode())
        elif resource == "categories":
            new_category = create_category(post_body)
            self.wfile.write(json.dumps(new_category).encode())

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
