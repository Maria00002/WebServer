from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

dataverse_files = { 1: 'B1E',2: 'B2E', 3: 'BME', 4: 'CDE', 5: 'CWE', 6:'DNE', 7:'DWE', 8: 'EBE', 9: 'EQE', 
                    10: 'FGE', 11: 'FRE', 12: 'FRG', 13: 'GRE', 14: 'HPE', 15 : 'HTE', 16: 'HTW' , 17: 'OFE', 
                    18: 'OUE', 19: 'TVE', 20: 'UTE', 21: 'WHE', 22: 'WHG', 23: 'WHW', 24: 'WOE'} 


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/dataverse_files'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'			
            output += '<h1>dataverse_files</h1>'
            for (id,name) in dataverse_files.items():
                output += '<h3><a href=""> %s </a></h3>' % dataverse_files[id]
                output += '</br>'
            output += '</body></html>'
            self.wfile.write(output.encode())
            
def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()




