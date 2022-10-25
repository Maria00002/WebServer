import re
import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler


MACOS_ROOT_DIR = '/Users/stephen/SourceCode/Maria/WebServer/AMPds/'
WINDOWS_ROOT_DIR = 'C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\'

#ROOT_DIR = MACOS_ROOT_DIR
ROOT_DIR = WINDOWS_ROOT_DIR

# localhost:8000/AMPds/B1E/V@12234~21234
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
                    'HTW': "HTW.CSV", 
                    'OFE': "OFE.CSV", 
                    'OUE': "OUE.CSV", 
                    'TVE': "TVE.CSV", 
                    'UTE': "UTE.CSV", 
                    'WHE': "WHE.CSV", 
                    'WHG': "WHG.CSV", 
                    'WHW': "WHW.CSV", 
                    'WOE': "WOE.CSV" } 

data = ['AMPds']
line_num = 10

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global data, dataverse_files, line_num
        time = []
        start_end_list = []
       
        #break the self.path into a list
        self_path_list = re.split(r'[/@+]', self.path)

        contain_data = list_contains(self_path_list, data) #return true if URL contains the dataset in used, false otherwise
        # localhost:8000/AMPds
        if contain_data:
            self.send_response(200)
            self.send_header('content-type','text/html')
            self.end_headers()
            output = ''
            output += '<html><body>'			
            output += '<h1>AMPds</h1>'
            output += '</body></html>' 
            self.wfile.write(output.encode())

            # check File name
            contain_file = list_contains(self_path_list, dataverse_files.keys()) #return true if the URL contains the file, false otherwise
            #localhost:8000/AMPds/B1E (B1E,B2E,BME,CDE,CWE,DNE,DWE,EBE,EQE,FGE,FRE,FRG,GRE,HPE,HTE,HTW,OFE,OUE,TVE,UTE,WHE,WHG,WHW,WOE)
            if contain_file:
                file_list_input = common(self_path_list, dataverse_files.keys())
                output = ''
                output += '<html><body>'
                ## can only read one file right now
                df = pd.read_csv('%s%s.csv' % (ROOT_DIR, file_list_input[0]))
                df.set_index('TS',inplace = True, drop = False)
                # reading the column names from the file selected
                col_names = df.columns.tolist()
                #reads the min and max timestamp
                min_timestamp=df['TS'].min()
                max_timestamp=df['TS'].max()
                output += '<p>The minimum timestamp is %d and the maximum timestamp is %d </p>' %(min_timestamp,max_timestamp)
                # total read
                total_count = df['TS'].count()
                output += '<p>The number of entries for time series data are %d </p>' %(total_count)
                # standard deviation
                stats = df.describe()
                output += '<pre>'
                output += '<p>The statistical information </p>'
                output +=  '%s' %(stats)
                output += '</pre>'
                output += '</body></html>'
                self.wfile.write(output.encode())

                # check column
                contain_column = list_contains(self_path_list, col_names) #return true if the URL contains the column names, false otherwise
                #localhost:8000/AMPds/B1E/V (TS  V  I  f  DPF  APF  P  Pt  Q  Qt  S  St)    
                if contain_column:
                    column_list_input = common(self_path_list, col_names)
                    output = ''
                    output += '<html><body>'
                    # can only display one column selected
                    column_selected_TS = df[['TS', column_list_input[0]]]
                    printed_version = column_selected_TS.head(line_num)
                    df2 = printed_version.to_string(index=False)
                    # if common(self_path_list, "*"):
                    #     df2 = column_selected_TS.to_string(index=False) 

                    #Time Selection
                    # http://localhost:8000/AMPds/DWE/V@1333263600~1333264020   
                    for item in self_path_list:
                        if item.find("~") != -1:
                            time.append(item)
                    for times in time:
                        time_col = times.split("~")
                        start_end_list.append(time_col)
                    if len(time) != 0:
                        # if the start time is not on record, the previous recorded timestamp is used
                        start = df["TS"].loc[df['TS']<= int(float(start_end_list[0][0]))].max()
                        end = df["TS"].loc[df['TS'] >= int(float(start_end_list[0][1]))].min()
                        
                        # if the end time is not on record, the next recorded timestamp is used
                        df_time = column_selected_TS.loc[start:end]
                        df_time_with_selected_column = df_time.to_string(index=False)
                        df2 = df_time_with_selected_column
                        output += '*Note the timestamp on file is not consecutive numbers <br>'
                        output += '*If the corresponding Start Time is not on record, the previous recorded timestamp is used <br>'
                        output += '*If the corresponding End Time is not on record, the next recorded timestamp is used <br>'
        
                    output += '<pre>' 
                    output += '%s' % df2
                    output += '</pre>'
                    output += '</body></html>'
                    self.wfile.write(output.encode())



def list_contains(List1, List2): 
        set1 = set(List1) 
        set2 = set(List2) 
        if set1.intersection(set2): 
            return True 
        else: 
            return False

def common(lst1, lst2): 
    return list(set(lst1) & set(lst2))
                
                        
def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   

if __name__ == '__main__':
    main()
