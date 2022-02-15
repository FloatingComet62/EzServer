from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import pages
import callbackfunctions
import middleware
from urllib.parse import urlparse
import static

hostname = "localhost"
serverport = 6969

def strTobyteArray(array):
    output = []
    for item in array:
        output.append(bytes(item, "utf-8"))
    
    return output

def turntoFString(non_f_str, self, query):
    if "{" in non_f_str:
        if "}" in non_f_str:
            return eval(f'f"""{non_f_str}"""')
        else:
            return non_f_str
    else:
        return non_f_str


def fileopen(fileToOpen, self, query):
    with open(fileToOpen , 'r', encoding='utf-8') as file:
        content = file.readlines()

    output = []
    for line in content:
        output.append(line)
    
    return output

def addPage(page, self, query):
    actualPath = self.path.split("?")
    path = page[0]
    htmlFile = page[2]
    callBackFunction = page[3] or None
    middleWareFunction = page[4] or None

    if actualPath[0] == path:
        self.send_header("Content-Type", f"{page[1]}")
        self.end_headers()
        
        if middleWareFunction:
            htmlFileIndex = eval(f'middleware.{middleWareFunction}(self, {query})')
            self.wfile.writelines(strTobyteArray(fileopen(htmlFile[htmlFileIndex], self, query)))
        
        else:

                self.wfile.writelines(strTobyteArray(fileopen(htmlFile[0], self, query)))

        if callBackFunction:
            eval(f'callbackfunctions.{callBackFunction}(self, {query}, {htmlFileIndex})')

def addStatic(page, self, query):
    actualPath = self.path.split("?")
    path = page[0]
    file = page[1]

    if actualPath[0] == path:
        self.send_header("Content-Type", f"{page[2]}")
        self.end_headers()

        if not "image" in page[2]:
            try:
                self.wfile.writelines(strTobyteArray(fileopen(file, self, query)))
            except:
                print(f"ERROR FILE: {file}")
                print(exception)
        else:
            with open(file, "rb") as image:
                try:
                    self.wfile.writelines([bytearray(image.read())])
                except Exception as exception:
                    print(f"ERROR FILE: {file}")
                    print(exception)

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        rawQuery = urlparse(self.path).query
        query = {}
        if rawQuery != "":
            query = dict(qc.split("=") for qc in rawQuery.split("&"))
        
        for item in static.static:
            addStatic(item, self, query)
        
        for page in pages.pages:
            if len(page) < 5:
                for i in range(5-len(page)):
                    page.append("")
            addPage(page, self, query)

if __name__ == "__main__":
    webServer = HTTPServer((hostname, serverport), Server)
    print(f"Server started http://{hostname}:{serverport}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server Stopped")