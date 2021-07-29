from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from posts.request import get_subbed_posts_for_user
from reactions.request import create_reaction
from users.request import login_user
from users import register_new_user, get_user_by_email, get_single_user
from post_reactions import (
    get_all_post_reactions,
    get_post_reactions_by_post_id,
    create_post_reaction
)
from categories import create_category, get_all_categories, update_category
from posts import get_posts_by_user
from comments import (
    create_comment,
    get_all_comments,
    view_comments_by_post,
    delete_comment,
    edit_comment
)


class HandleRequests(BaseHTTPRequestHandler):
    def parse_url(self, path):  # pylint: disable=missing-docstring
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

    def do_GET(self):  # pylint: disable=missing-docstring
        self._set_headers(200)  # STATUS OKAY
        response = {}
        parsed = self.parse_url(self.path)

        if len(parsed) <= 2:
            (resource, id) = parsed
            if resource.lower() == "categories":
                response = get_all_categories()
            elif resource == "post_reactions":
                response = get_all_post_reactions()
            elif resource == "comments":
                response = get_all_comments()
            elif resource == "users":
                if id is not None:
                    response = get_single_user(id)

        else:
            # we got query params!
            (resource, key, value) = parsed
            if resource.lower() == "users" and key.lower() == "email":
                response = get_user_by_email(value)
            elif resource.lower() == "post_reactions" and key.lower() == "post_id":
                response = get_post_reactions_by_post_id(value)
            elif resource.lower() == "posts" and key.lower() == "user_id":
                response = get_posts_by_user(value)
            elif resource.lower() == "subs" and key.lower() == "follower_id":
                response = get_subbed_posts_for_user(value)
            elif resource.lower() == "comments" and key.lower() == "post_id":
                response = view_comments_by_post(value)

        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):  # pylint: disable=missing-docstring
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        parsed = self.parse_url(self.path)
        resource = parsed[0].lower()

        if resource == "register":
            # if the user specified by the email in the post body does exist:
            if get_user_by_email(post_body['email']) is None:
                self._set_headers(201)  # STATUS CREATED
                new_user = register_new_user(post_body)
                self.wfile.write(json.dumps(new_user).encode())
            else:
                # STATUS OKAY (used here to indicate it the request went through okay)
                self._set_headers(200)
                self.wfile.write(json.dumps("User already exists.").encode())
        elif resource == "login":
            # send 200 OKAY to indicate that the request went through
            self._set_headers(200)
            user_id = login_user(post_body['email'], post_body['password'])
            if user_id is None:
                self.wfile.write(json.dumps(
                    "Email and password do not match.").encode())
            else:
                self.wfile.write(json.dumps({"id": user_id}).encode())
        elif resource == "categories":
            self._set_headers(201)  # STATUS CREATED
            new_category = create_category(post_body)
            self.wfile.write(json.dumps(new_category).encode())
        elif resource == "comments":
            self._set_headers(201)  # STATUS CREATED
            new_comment = create_comment(post_body)
            self.wfile.write(json.dumps(new_comment).encode())
        elif resource == "reactions":
            self._set_headers(201)
            new_reaction = create_reaction(post_body)
            self.wfile.write(json.dumps(new_reaction).encode())
        elif resource == "post_reactions":
            self._set_headers(201)
            new_post_reaction = create_post_reaction(post_body)
            self.wfile.write(json.dumps(new_post_reaction).encode())

    def do_PUT(self):
        """PUT fetch call handler
        """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "categories":
            success = update_category(id, post_body)
        if resource == "comments":
            success = edit_comment(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):  # pylint: disable=missing-docstring
        """Handles DELETE requests to the server
        """
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)

        if resource == "comments":
            delete_comment(id)

        self.wfile.write("".encode())


def main():  # pylint: disable=missing-docstring
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
