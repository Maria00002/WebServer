from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

MACOS_ROOT_DIR = '/Users/stephen/SourceCode/Maria/WebServer/AMPds/'
WINDOWS_ROOT_DIR = 'C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\'

ROOT_DIR = WINDOWS_ROOT_DIR

dataverse_files = { 'B1E': "B1E.CSV",
'B2E': "B2E.CSV", 
'BME': "BME.CSV", 
'CDE': "CDE.CSV", 
'CWE': "CWE.CSV", 
'DNE': "DNE.CSV", 
'DWE': "DWE.CSV", 
'EBE': "EBE.CSV", 
'EQE': "EQE.CSV", 
'FGE': "FGE.CSV", 
'FRE': "FRE.CSV", 
'FRG': "FRG.CSV", 
'GRE': "GRE.CSV", 
'HPE': "HPE.CSV", 
'HTE': "HTE.CSV", 
'HTW': "HTW.CSV" , 
'OFE': "OFE.CSV", 
'OUE': "OUE.CSV", 
'TVE': "TVE.CSV", 
'UTE': "UTE.CSV", 
'WHE': "WHE.CSV", 
'WHG': "WHG.CSV", 
'WHW': "WHW.CSV", 
'WOE': "WOE.CSV"} 

line_num = 10
header_row = 1
header = []
new_header = []

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global line_num
        global file_name
        global header
        global new_header
        if self.path.endswith('/AMPds'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'			
            output += '<h1>AMPds</h1>'
            for (id,path_directory) in dataverse_files.items():
                output += '<h3><a href="/AMPds/%s"> %s </a></h3>' % (id,id)
            output += '</body></html>'
            self.wfile.write(output.encode())
        
        for file_name in dataverse_files.keys():
            if self.path.endswith('/%s' % file_name):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                output += '<pre>'
                with open('%s%s' % (ROOT_DIR, dataverse_files[file_name])) as myfile:
                    for x in range(header_row):
                        header += next(myfile)
                        word = ''
                        for individual_letter in header:
                            if individual_letter == ',':
                                new_header.append(word)
                                word = ''
                            if individual_letter == '\n':
                                new_header.append(word)
                            else:
                                word += individual_letter
                        # print(new_header) ## new_header is <class 'list'>
                output += '</pre>'
                for index in new_header:
                    output += '<a href="http://localhost:8000/AMPds/%s"> <button> %s </button></a>' % (index,index)                 
                output += '<a href="http://localhost:8000/AMPds"> <button> back </button></a>'
                output += '</body></html>'
                self.wfile.write(output.encode())

## New Code to be changed
        # for index in new_header:
        #     if self.path.endswith('/%s' % index):
        #         self.send_response(200)
        #         self.send_header('content-type','text/html')
        #         self.end_headers()
        #         output = ''
        #         output += '<html><body>'
        #         output += '<pre>'
        #         with open('%s%s' % (ROOT_DIR, dataverse_files[file_name])) as myfile:
        #             for x in range(line_num):
        #                 output += next(myfile)                    
        #         output += '</pre>'
        #         output += '<a href="http://localhost:8000/AMPds"> <button> back </button></a>'
        #         output += '</body></html>'
        #         self.wfile.write(output.encode())
    
                
def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   

if __name__ == '__main__':
    main()
