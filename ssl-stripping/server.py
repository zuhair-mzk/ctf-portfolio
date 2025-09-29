from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from http.client import HTTPSConnection
from urllib import parse
import sys

class Server(BaseHTTPRequestHandler):

    def __init__(self, filepath, *args, **kwargs):
        self.filepath = filepath
        super().__init__(*args, **kwargs)

    # GET request handler
    def do_GET(self):
    # Retrieve the path and headers from the HTTP request
        path = self.path
        headers = self.headers
        print("Received GET request from Alice to:", path)

        if path == "/check":
            # Connect to the real server over HTTPS
            conn = HTTPSConnection("welcome.seclab.space")
            conn.request("GET", path, headers=headers)
            res = conn.getresponse()
            data = res.read()  # Read response data once
            status_code = res.status
            conn.close()

            # Write the flag to file if the path is /check
            with open(self.filepath, "wb") as f:
                f.write(data)
                print("Flag written to file:", data.decode("utf-8"))

            # Exit after capturing the flag
            sys.exit(0)

            # Send the response back to Alice for /check path
            self.send_response(status_code)
            for k, v in res.getheaders():
                self.send_header(k, v)
            self.end_headers()
            self.wfile.write(data)
        else:
            # Handle non-/check requests
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 Not Found\n")
            print("Received non-flag request, ignoring.")


    # POST request handler
    def do_POST(self):
        path = self.path
        headers = self.headers
        body = self.rfile.read(int(self.headers.get('Content-Length')))

        # Forward the POST request to the real server
        conn = HTTPSConnection("welcome.seclab.space")
        conn.request("POST", path, body, headers)
        res = conn.getresponse()
        response_body = res.read()
        conn.close()

        # Send response back to Alice
        self.send_response(res.status)
        for k, v in res.getheaders():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(response_body)

    # PUT request handler
    def do_PUT(self):
        path = self.path
        headers = self.headers
        body = self.rfile.read(int(self.headers.get('Content-Length')))

        # Forward the PUT request to the real server
        conn = HTTPSConnection("welcome.seclab.space")
        conn.request("PUT", path, body, headers)
        res = conn.getresponse()
        response_body = res.read()
        conn.close()

        # Send response back to Alice
        self.send_response(res.status)
        for k, v in res.getheaders():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(response_body)

# =============================================
# ===== do not modify the code below ==========
# =============================================
        
def run_server(filepath):
    handler = partial(Server, filepath)
    httpd = HTTPServer(('', 8080), handler)
    httpd.serve_forever()

if __name__ == "__main__":
    import os, sys, getopt
    def usage():
        print('Usage:    ' + os.path.basename(__file__) + ' filepath ')
        sys.exit(2)
    # extract parameters
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.GetoptError as err:
        print(err)
        usage()
        sys.exit(2)
    filepath = args[0] if len(args) > 0 else None
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
    if (filepath is None):
        print('filepath is missing\n')
        usage()
    # run the command
    run_server(filepath)
