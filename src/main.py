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
    if "{" in non_f_str:
        if "}" in non_f_str:
            return eval(f'f"""{non_f_str}"""')
        else:
            return non_f_str
    else:
        return non_f_str

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
            html = strTobyteArray(fileopen(htmlFile[htmlFileIndex], self, query))

            return html
        
        else:

            html = strTobyteArray(fileopen(htmlFile[0], self, query))

            return html

        if callBackFunction:
            eval(f'callbackfunctions.{callBackFunction}(self, {query}, {htmlFileIndex}')

def addCss(path, cssFile, self, query, callBackFunction=None, middleWareFunction=None):
    actualPath = self.path.split("?")

    if actualPath[0] == path:
        
        if middleWareFunction:
            cssFileIndex = eval(f'middleware.{middleWareFunction}(self, {query})')
            css = strTobyteArray(fileopen(cssFile[cssFileIndex], self, query))

            return css
        
        else:

            css = strTobyteArray(fileopen(cssFile[0], self, query))

            return css

        if callBackFunction:
            eval(f'callbackfunctions.{callBackFunction}(self, {query}, {cssFileIndex})')

class Server(BaseHTTPRequestHandler):
    def do_GET(self):
        rawQuery = urlparse(self.path).query
        query = {}
        pagesLength = 5
        css = []
        html = []
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()

        if rawQuery != "":
            query = dict(qc.split("=") for qc in rawQuery.split("&"))
        
        for page in pages.pages:
            if len(page) < pagesLength:
                for i in range(pagesLength-len(page)):
                    page.append("")
            
            while css == []:
                css = addCss(page[0], page[2], self, query, page[3], page[4])
        
        for page in pages.pages:
            if len(page) < pagesLength:
                for i in range(pagesLength-len(page)):
                    page.append("")
            while html == []:
                html = addPage(page[0], page[1], self, query, page[3], page[4])
                cssAppendIndex = -1
                for i in range(len(html)-1):
                    line = html[i]
                    if not line.find(b"<head>"):
                        cssAppendIndex = i+1
                
                if not cssAppendIndex == -1:
                    html.insert(cssAppendIndex, b"</style>")
                    for i in range(len(css)):
                        line = css[len(css)-1-i]
                        html.insert(cssAppendIndex, line)
                    html.insert(cssAppendIndex, b"<style>")
                
                self.wfile.writelines(html)

        
if __name__ == "__main__":
    webServer = HTTPServer((hostname, serverport), Server)
    print(f"Server started http://{hostname}:{serverport}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server Stopped")