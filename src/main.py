from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import pages
import callbackfunctions
import middleware
from urllib.parse import urlparse

hostname = "localhost"
serverport = 6969

def strTobyteArray(array):
    output = []
    for item in array:
        output.append(bytes(item, "utf-8"))
    
    return output

def turntoFString(non_f_str, self, query):
    return eval(f'f"""{non_f_str}"""')


def fileopen(fileToOpen, self, query):
    with open(fileToOpen) as file:
        content = file.readlines()

    output = []
    for line in content:
        output.append(turntoFString(line, self, query))
    
    return output

def addPage(path, htmlFile, self, query, callBackFunction=None, middleWareFunction=None):
    actualPath = self.path.split("?")

    if actualPath[0] == path:
        
        if middleWareFunction:
            htmlFileIndex = eval(f'middleware.{middleWareFunction}(self, {query})')
            self.wfile.writelines(strTobyteArray(fileopen(htmlFile[htmlFileIndex], self, query)))
        
        else:

            self.wfile.writelines(strTobyteArray(fileopen(htmlFile[0], self, query)))

        if callBackFunction:
            eval(f'callbackfunctions.{callBackFunction}(self, {query}, {htmlFileIndex})')

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        rawQuery = urlparse(self.path).query
        query = {}
        if rawQuery != "":
            query = dict(qc.split("=") for qc in rawQuery.split("&"))
        
        for page in pages.pages:
            if len(page) < 4:
                for i in range(4-len(page)):
                    page.append("")
            addPage(page[0], page[1], self, query, page[2], page[3])

if __name__ == "__main__":
    webServer = HTTPServer((hostname, serverport), Server)
    print(f"Server started http://{hostname}:{serverport}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server Stopped")