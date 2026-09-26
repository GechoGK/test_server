from http.server import HTTPServer, BaseHTTPRequestHandler
import json

clicks = 0


class Server(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.send_file("index.html", "text/html")

        elif self.path == "/api/clicks":
            self.send_json({"clicks": clicks})

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        global clicks

        if self.path == "/api/click":
            clicks += 1
            self.send_json({"clicks": clicks})

        else:
            self.send_error(404, "Not Found")

    def send_json(self, data):
        response = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()

        self.wfile.write(response)

    def send_file(self, filename, content_type):
        with open(filename, "rb") as file:
            content = file.read()

        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()

        self.wfile.write(content)


import os

port = int(os.environ.get("PORT", 8000))

server = HTTPServer(("0.0.0.0", port), Server)

print(f"Server running on port {port}")

server.serve_forever()
