from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

dataverse_files = { 'B1E': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\B1E.CSV",
'B2E': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\B2E.CSV", 
'BME': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\BME.CSV", 
'CDE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\CDE.CSV", 
'CWE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\CWE.CSV", 
'DNE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\DNE.CSV", 
'DWE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\DWE.CSV", 
'EBE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\EBE.CSV", 
'EQE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\EQE.CSV", 
'FGE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\FGE.CSV", 
'FRE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\FRE.CSV", 
'FRG': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\FRG.CSV", 
'GRE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\GRE.CSV", 
'HPE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\HPE.CSV", 
'HTE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\HTE.CSV", 
'HTW': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\HTW.CSV" , 
'OFE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\OFE.CSV", 
'OUE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\OUE.CSV", 
'TVE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\TVE.CSV", 
'UTE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\UTE.CSV", 
'WHE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\WHE.CSV", 
'WHG': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\WHG.CSV", 
'WHW': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\WHW.CSV", 
'WOE': "C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\WOE.CSV"} 

line_num = 10
data = []

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
            for (id,path_directory) in dataverse_files.items():
                output += '<h3><a href="/dataverse_files/extract"> %s </a></h3>' % id
            output += '</body></html>'
            self.wfile.write(output.encode())
        
        if self.path.endswith('/extract'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'
            output += '<pre>'
            for (id,path_directory) in dataverse_files.items():
                with open(path_directory) as myfile:
                    # head = [next(myfile) for x in range(line_num)]
                    for x in range(line_num):
                        output += next(myfile)                    
            output += '</pre>'
            output += '</body></html>'
            # output = [information.encode('utf-8') for information in output]
            self.wfile.write(output.encode())
    
    
    # def do_POST(self):
    #     if self.path.endswith('/extract'):
    #         ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
    #         pdict['boundary'] = bytes(pdict['boundary'],"utf-8")
    #         fields = cgi.parse_multipart(self.rfile,pdict)
    #         fields = head                
    #         self.send_response(301)
    #         self.send_header('content-type','text/html')
    #         self.send_header('Location','/website')
    #         self.end_headers()
    #         self.wfile.write(output.encode())
       
                     
        
def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   

if __name__ == '__main__':
    main()

 