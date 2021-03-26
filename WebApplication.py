#Author: Jhonatan Narvaez 
#Matrikelnummer: 1329832 

# Python 3 server example
from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import os

hostName = "192.168.1.225"
serverPort = 400

class MyServer(BaseHTTPRequestHandler):

    def do_GET(self):
        root = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'RedPitayaSFR02')
        print(self.path)
        if self.path == '/':
            filename = root + '/PaginaPrincipal.html'
        else:
            filename = root + self.path
        print(filename)
        print(root)
        #f = open('PaginaPrincipal.html','rb')
        self.send_response(200)
        if filename[-4:] == '.css':
            self.send_header('Content-type', 'text/css')
        elif filename[-5:] == '.json':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-3:] == '.js':
            self.send_header('Content-type', 'application/javascript')
        elif filename[-4:] == '.ico':
            self.send_header('Content-type', 'image/x-icon')
        else:
            self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fh:
            html = fh.read()
            #html = bytes(html, 'utf8')
            self.wfile.write(html)
        #self.wfile.write(f.read())
        #f.close()
        #self.wfile.write(bytes("<html><head><title>https://pythonbasics.org</title><meta http-equiv=\"refresh\" content=\"30\"></head>", "utf-8"))
        #self.wfile.write(bytes("<p>Request: %s</p>" % self.path, "utf-8"))
        #self.wfile.write(bytes("<body>", "utf-8"))
        #self.wfile.write(bytes("<p>This is an "+str(conteo)+".</p>", "utf-8"))
        #self.wfile.write(bytes("</body></html>", "utf-8"))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
