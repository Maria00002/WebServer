from ctypes import sizeof
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


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global data, dataverse_files, line_num, statement, index_of_first_timestamp
        time = []
        exclusion_time =  []
        start_end_list = []
        exclusion_start_end_list = []
        output = ''
        statement = False
        line_num = 10
        data = ['AMPds']
        index_of_first_timestamp= 0

        # self_path_list and if contain data/file/column
        self_path_list = re.split(r'[/@+]', self.path)
        contain_data = list_contains(self_path_list, data) #return true if URL contains the dataset in used, false otherwise
        
        ## functions
        def self_response(x):
            self.send_response(x)
            self.send_header('content-type','text/html')
            self.end_headers()

        def page_404_not_found():
            self_response(404)
            output = ''
            output += '<html><body>'			
            output += '<h1>404 Not Found</h1>'
            output += '<p>The URL you have entered is not correct. Please check your input and try again</p>'
            output += '</body></html>'
            self.wfile.write(output.encode())         
        
        # localhost:8000/AMPds
        if contain_data:
            self_response(200)
            output = ''
            output += '<html><body>'			
            output += '<h1>AMPds</h1>'
            output += '</body></html>'
            output += '<link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon">' 

            #localhost:8000/AMPds/B1E (B1E,B2E,BME,CDE,CWE,DNE,DWE,EBE,EQE,FGE,FRE,FRG,GRE,HPE,HTE,HTW,OFE,OUE,TVE,UTE,WHE,WHG,WHW,WOE)
            contain_file = list_contains(self_path_list, dataverse_files.keys()) #return true if the URL contains the file, false otherwise
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

                #localhost:8000/AMPds/B1E/V (TS  V  I  f  DPF  APF  P  Pt  Q  Qt  S  St)    
                contain_column = list_contains(self_path_list, col_names) #return true if the URL contains the column names, false otherwise
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
                    for index, item in enumerate(self_path_list):
                        if item.find("~") != -1:
                            index_of_first_timestamp = index
                            break
                    
                    for item in self_path_list:
                        if self_path_list[index_of_first_timestamp-1] == '':
                            exclusion_time.append(item)
                        elif item.find("~") != -1:
                            time.append(item)
                    ## run prin tcases to check if it is true
                    # print(exclusion_time)
                    # print("--------------------------")

                    for times in time:
                        time_col = times.split("~")
                        start_end_list.append(time_col)
                    
                    for item in exclusion_time:
                        if item.find("~") != -1:
                            time_col = item.split("~")
                            exclusion_start_end_list.append(time_col)
  
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
        
                    if len(exclusion_time) != 0:
                        # if the start time is not on record, the previous recorded timestamp is used
                        exculsion_start = df["TS"].loc[df['TS']<= int(float(exclusion_start_end_list[0][0]))].max()
                        exculsion_end = df["TS"].loc[df['TS'] >= int(float(exclusion_start_end_list[0][1]))].min()
                        
                        # if the end time is not on record, the next recorded timestamp is used
                        df_2 = column_selected_TS.loc[exculsion_start:exculsion_end]
                        list = df_2['TS']
                        exclusion_df = column_selected_TS.index.isin(list)
                        df2 = column_selected_TS[~exclusion_df].head(line_num)
                        df_time_with_selected_column = df2.to_string(index=False)
                        df2 = df_time_with_selected_column
                        output += '*Note the timestamp on file is not consecutive numbers <br>'
                        output += '*If the corresponding Start Time is not on record, the previous recorded timestamp is used <br>'
                        output += '*If the corresponding End Time is not on record, the next recorded timestamp is used <br>'
        
                    output += '<pre>' 
                    output += '%s' % df2
                    output += '</pre>'
                    output += '</body></html>'
        

        if len(self_path_list) == 2:
            if contain_data:                                   
                statement = True
            else:                             
                statement = False
        if len(self_path_list) == 3:
            if contain_data and contain_file:                  
                statement = True
            else:            
                statement = False
        if len(self_path_list) == 4:
            if contain_data and contain_file and contain_column:          
                statement = True
            else:             
                statement = False
        if len(self_path_list) == 5:
            if contain_data and contain_file and contain_column and self_path_list[-1] == '*':          
                statement = True
            elif contain_data and contain_file and contain_column and len(self_path_list[-1]) == 21 and start < end:
                statement = True
        if len(self_path_list) == 6:         
            statement = True
            

        ## print out error message page or the information page        
        if statement:
            self.wfile.write(output.encode())            
        else:
            page_404_not_found()
            

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

