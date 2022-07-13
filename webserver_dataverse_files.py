from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

# dataverse_files = { 1: 'B1E',2: 'B2E', 3: 'BME', 4: 'CDE', 5: 'CWE', 6:'DNE', 7:'DWE', 8: 'EBE', 9: 'EQE', 
#                     10: 'FGE', 11: 'FRE', 12: 'FRG', 13: 'GRE', 14: 'HPE', 15 : 'HTE', 16: 'HTW' , 17: 'OFE', 
#                     18: 'OUE', 19: 'TVE', 20: 'UTE', 21: 'WHE', 22: 'WHG', 23: 'WHW', 24: 'WOE'} 

dataverse_files = { 1: 'B1E'} 
data = []
line_num = 10

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global line_num
        if self.path.endswith('/dataverse_files'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'			
            output += '<h1>dataverse_files</h1>'
            for (id,name) in dataverse_files.items():
                output += '<h3><a href="/dataverse_files/extract"> %s </a></h3>' % dataverse_files[id]
                # output += '<pre>  </pre>' #this should print out the list of dataverse_file in python
            for index in data:
                output += '<h3><a href="/dataverse_files"> %s </a></h3>' % data[index]
            output += '</body></html>'
            self.wfile.write(output.encode())


    
    def do_POST(self):
        if self.path.endswith('/extract'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'],"utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile,pdict)
                max_id = max(list(data))     
                with open("C:\Maria\SFU\SFU Thesis\Figure 17 Research Paper\dataverse_files\excel_files\B1E.csv") as myfile:
                    head = [next(myfile) for x in range(line_num)]
                    data[max_id+1] = head
                    print(head)
                myfile.close()

            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/dataverse_files')
            self.end_headers()
                     
        
def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   

if __name__ == '__main__':
    main()

 