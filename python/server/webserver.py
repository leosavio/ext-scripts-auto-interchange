import http.server
import socketserver

class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/test/health':
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Healthy!')
        else:
            self.send_response(404)
            self.end_headers()

PORT = 9080

with socketserver.TCPServer(("", PORT), MyHTTPRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
