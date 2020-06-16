import socketserver
import os
from datetime import datetime
from http.server import SimpleHTTPRequestHandler
from urllib.parse import parse_qs
from typing import Dict

year = datetime.now().year
hour = datetime.now().hour

PORT = int(os.getenv("PORT", 8000))
print(f"PORT = {PORT}")


class MyHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        path = self.path_calculating()
        handlers = {
            "/hello": self.hello_response,
            "/goodbye": self.goodbye_response
        }
        handler = handlers.get(path, super().do_GET)
        handler()

    def hello_response(self):
        arguments = self.parse_function()
        path = self.path_calculating()
        name = self.name_calculating(arguments)
        age = self.age_calculating(arguments)
        msg = f"""
                                    Hello {name}!                

                                    Your path: {path}

                                                       """
        if 'age':
            born = year - age
            msg += f"\n\t\t\t\t   You were born in {born}"

        self.response(msg)

    def goodbye_response(self):
        if hour in range(6, 11):
            msg = f"\n\t\t\t\t   Good morning!"
        elif hour in range(12, 24):
            msg = f"\n\t\t\t\t   Good day!"
        else:
            msg = f"\n\t\t\t\t   Good night!"

        self.response(msg)

    def path_calculating(self):
        return self.path.split("?")[0]

    def name_calculating(self, qs_arguments: Dict):
        return qs_arguments.get('name', 'anonymous')

    def age_calculating(self, qs_arguments: Dict):
        return int(qs_arguments.get('age', 0))

    def parse_function(self):
        _path, *qs = self.path.split("?")
        arguments = {}

        if len(qs) != 1:
            return arguments

        qs = qs[0]
        qs = parse_qs(qs)

        for keys, values in qs.items():
            if not values:
                continue
            arguments[keys] = values[0]

        return arguments

    def response(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.send_header("Content-length", len(msg))
        self.end_headers()

        self.wfile.write(msg.encode())


with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
    print("it works")
    httpd.serve_forever()
