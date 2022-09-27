import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler

MACOS_ROOT_DIR = '/Users/stephen/SourceCode/Maria/WebServer/AMPds/'
WINDOWS_ROOT_DIR = 'C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\'

#ROOT_DIR = MACOS_ROOT_DIR
ROOT_DIR = WINDOWS_ROOT_DIR

# localhost:8000/AMPds.B1E.V@12234~21234

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
                    'WOE': "WOE.CSV" } 

filename = ''
line_num = 10
header = ''
col_names = []

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global filename, line_num, header, col_names

        #localhost:8000/AMPds
        if self.path.endswith('/AMPds'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'			
            output += '<h1>AMPds</h1>'
            for (id,path_directory) in dataverse_files.items():
                output += '<h3><a href="/AMPds.%s"> %s </a></h3>' % (id,id)
            output += '</body></html>'
            self.wfile.write(output.encode())

        #localhost:8000/AMPds.B1E
        for filename in dataverse_files.keys():
            if self.path.endswith('.%s' % filename):
                self.send_response(200)
                self.send_header('content-type','text/html')
                self.end_headers()
                output = ''
                output += '<html><body>'
                with open('%s%s' % (ROOT_DIR, dataverse_files[filename])) as myfile:
                    header = myfile.readline()
                    col_names = list(header.split(','))
                for col_name in col_names:
                    output += '<a href="http://localhost:8000/AMPds.%s.%s"><button>&nbsp;&nbsp;%s&nbsp;&nbsp;</button></a>&nbsp;&nbsp;' % (filename,col_name,col_name)
                output += '<a href="http://localhost:8000/AMPds"><button>&nbsp;&nbsp;back&nbsp;&nbsp;</button></a>'
                output += '</body></html>'
                self.wfile.write(output.encode())

        #localhost:8000/AMPds.B1E.V
        for filename in dataverse_files.keys():
            for col_name in col_names:
                if self.path.endswith('.%s.%s' % (filename,col_name)):
                        self.send_response(200)
                        self.send_header('content-type','text/html')
                        self.end_headers()
                        output = ''
                        output += '<html><body>'
                        output += '<pre>'
                        output += '&nbsp;&nbsp;&nbsp;&nbsp;  TS &nbsp;&nbsp;&nbsp;'
                        output += '&nbsp; %s \n' % (col_name)
                        file_reading = pd.read_csv('%s%s' % (ROOT_DIR, dataverse_files[filename]), nrows = line_num)
                        for i, row in file_reading.iterrows():
                            output += '%s %s\n' % ( row['TS'], row[col_name])                   
                        output += '</pre>'
                        output += '<a href="http://localhost:8000/AMPds"> <button> Back to Home Page </button></a>'
                        output += '</body></html>'
                        self.wfile.write(output.encode())
                
def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   

if __name__ == '__main__':
    main()