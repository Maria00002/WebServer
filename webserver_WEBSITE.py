from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi

## Process Thoughts
# 1 The user enters the website address
# 2 All files found on the web are returned back 
# 3 User select the file(s) needed
# 4 Headings of the files are returned back 
# 5 The user selects the headings needed & Enter the timestamp (from -> to)
# 6 Information about the specific timeframe is returned back (can return back to the same website or return back a downloadable file)


website = ['https://www.nature.com/articles/sdata201637','https://github.com/smakonin/RAE.dataset/blob/01fb4849674c76cd35e858b3542ee2c7d35cd513/Eagle200_logger.py']
website = {1:'https://www.nature.com/articles/sdata201637',2:'https://github.com/smakonin/RAE.dataset/blob/01fb4849674c76cd35e858b3542ee2c7d35cd513/Eagle200_logger.py'}

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/website'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Website</h1>'
            output += '<h3><a href="/website/new">Please enter the website address</a></h3>'
            for task in website:
                output += task
                output += '<a/ href="/website/%s/remove">x</a>' % task
                output += '</br>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Add New Website Address</h1>'
            output += '<form method="POST" enctype="multipart/form-data" action="/website/new">'
            output += '<input name="website address" type="text" placeholder="Add New website">'
            output += '<input type="submit" value="Add">'
            output += '</form>'
            output += '</body></html>'
            self.wfile.write(output.encode())
        
        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Remove website Entered: %s?</h1>' % listIDPath.replace('%20', ' ')
            output += '<form method="POST" enctype="multipart/form-data" action="/website/%s/remove">' % listIDPath
            output += '<input type="submit" value = "Remove"></form>'
            output += '<a href="/website">Cancel</a>'
            output += '</body></html>'
            self.wfile.write(output.encode())

    
    def do_POST(self):
        if self.path.endswith('/new'):
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            pdict['boundary'] = bytes(pdict['boundary'],"utf-8")
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile,pdict)
                new_website = fields.get('task')
				
                website.append(new_website)
                
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/website')
            self.end_headers()
            
        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                list_item = listIDPath.replace('%20', ' ')
                website.remove(list_item)
                
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/website')
            self.end_headers()

			
#################################################
    # def do_GET(self):
    #     if self.path == '/':
    #         self.path = '/index.html'
    #     try:
    #         file_to_open = open(self.path[1:]).read()
    #         self.send_response(200)
    #     except:
    #         file_to_open = "File not found"
    #         self.send_response(404)
    #     self.end_headers()
    #     self.wfile.write(bytes(file_to_open, 'utf-8'))

#################################################################


def main():
    PORT = 8000
    server = HTTPServer(('localhost', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
