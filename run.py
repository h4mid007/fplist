from http.server import BaseHTTPRequestHandler,HTTPServer
import os
PORT_NUMBER = int(os.environ.get('PORT', 5000))
import subprocess
#This class will handles any incoming request from
#the browser#
import urllib.parse as urlparse
class myHandler(BaseHTTPRequestHandler):
    
    #Handler for the GET requests
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        subprocess.run(["python", "proxy.py"])
        self.wfile.write(b"Oh, Thanks Cronnie! I'm waked up!")

        return
try:
    #Create a web server and define the handler to manage the
    #incoming request
    server = HTTPServer(('0.0.0.0', PORT_NUMBER), myHandler)
    print('Started httpserver on port ' , PORT_NUMBER)
    
    #Wait forever for incoming htto requests
    server.serve_forever()
    #server.handle_request()

except KeyboardInterrupt:
    print('^C received, shutting down the web server')
    server.socket.close()