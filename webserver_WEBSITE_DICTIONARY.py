from http.server import HTTPServer, BaseHTTPRequestHandler
import cgi
## Process Thoughts
# 1 The user enters the website address
# 2 All files found on the web are returned back 
# 3 User select the file(s) needed
# 4 Headings of the files are returned back 
# 5 The user selects the headings needed & Enter the timestamp (from -> to)
# 6 Information about the specific timeframe is returned back (can return back to the same website or return back a downloadable file)

tasklist = {1: 'https://www.google.com/', 2: 'https://www.sfu.ca/'}

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.endswith('/website'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            
            output = ''
            output += '<html><body>'
            output += '<h1>Website</h1>'
            output += '<h3><a href="/website/new">Add website URL to start</a></h3>'
            for (id,name) in tasklist.items():
                output += name
                output += '<a/ href="/website/%d/remove">x</a>' % (id,)
                output += '</br>'
            output += '</body></html>'
            self.wfile.write(output.encode())

        if self.path.endswith('/new'):
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()

            output = ''
            output += '<html><body>'
            output += '<h1>Add New Website Information</h1>'

            output += '<form method="POST" enctype="multipart/form-data" action="/website/new">'
            output += '<input name="task" type="text" placeholder="Add information here">'
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
            output += '<h1>Remove website address: %s? </h1>' % tasklist[int(listIDPath.replace('%20', ' '))] 
           
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
                new_task = fields.get('task')
                max_id = max(list(tasklist.keys()))                
                print(len(tasklist))
                tasklist[max_id+1] = new_task[0]
                print(tasklist)
                
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/website')
            self.end_headers()
            
        if self.path.endswith('/remove'):
            listIDPath = self.path.split('/')[2]
            ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
            if ctype == 'multipart/form-data':
                del tasklist[int(listIDPath)]
                
            self.send_response(301)
            self.send_header('content-type','text/html')
            self.send_header('Location','/website')
            self.end_headers()


def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()

if __name__ == '__main__':
    main()
