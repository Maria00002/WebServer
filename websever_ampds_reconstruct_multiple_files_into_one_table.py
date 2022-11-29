from ctypes import sizeof
import re
import pandas as pd
from http.server import HTTPServer, BaseHTTPRequestHandler
import glob
import os

MACOS_ROOT_DIR = '/Users/stephen/SourceCode/Maria/WebServer/AMPds/'
WINDOWS_ROOT_DIR = 'C:\\Maria\\Figure 17 Research Paper\\dataverse_files\\excel_files\\'
# WINDOWS_ROOT_DIR = 'C:\\Maria\\SFU\\SFU Thesis\\Figure 17 Research Paper\\dataverse_files\\excel_files\\'
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
                    # 'FRG': "FRG.CSV", 
                    'GRE': "GRE.CSV", 
                    'HPE': "HPE.CSV", 
                    'HTE': "HTE.CSV", 
                    # 'HTW': "HTW.CSV", 
                    'OFE': "OFE.CSV", 
                    'OUE': "OUE.CSV", 
                    'TVE': "TVE.CSV", 
                    'UTE': "UTE.CSV", 
                    'WHE': "WHE.CSV", 
                    # 'WHG': "WHG.CSV", 
                    # 'WHW': "WHW.CSV", 
                    'WOE': "WOE.CSV" } 


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global data, dataverse_files, line_num, statement, index_of_first_timestamp, all_data_file_column_name
        time = []
        exclusion_time = []
        start_end_list = []
        exclusion_start_end_list = []
        output = ''
        statement = False
        line_num = 10
        data = ['AMPds']
        index_of_first_timestamp= 0
        all_data_file_column_name = []
        
        # self_path_list and if contain data/file/column
        self_path_list = re.split(r'[/@+]', self.path)
        contain_data = list_contains(self_path_list, data) #return true if URL contains the dataset in used, false otherwise
        
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
                num_of_file_selected = len(file_list_input)
                z = 0
                output = ''
                output += '<html><body>'
                
                # trying to implement so it read multiple files
                while z < num_of_file_selected:
                    df = pd.read_csv('%s%s.csv' % (ROOT_DIR, file_list_input[z]))
                    df.set_index('TS',inplace = True, drop = False)
                    output += 'This is file %s' %(file_list_input[z])
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
                    z += 1 

                #localhost:8000/AMPds/B1E/V (TS  V  I  f  DPF  APF  P  Pt  Q  Qt  S  St)    
                contain_column = list_contains(self_path_list, col_names) #return true if the URL contains the column names, false otherwise
                # Time Selection
                # http://localhost:8000/AMPds/DWE/V@1333263600~1333264020   
                # check to see if it has the ~ in between the time selection, such as 1333263600~1333264020
                for index, item in enumerate(self_path_list):
                    if item.find("~") != -1:
                        index_of_first_timestamp = index
                        break
                # Check if it is exclusion @@ or just regular time selection @
                for item in self_path_list:
                    if self_path_list[index_of_first_timestamp-1] == '':
                        exclusion_time.append(item)
                    elif item.find("~") != -1:
                        time.append(item)
                    
                not_contain_timestamp = not time and not exclusion_time
                contain_timestamp = not not_contain_timestamp                   

                #localhost:8000/AMPds/B1E/V (TS  V  I  f  DPF  APF  P  Pt  Q  Qt  S  St)    
                if contain_column:
                    column_list_input = common(self_path_list, col_names)
                    num_of_columns_selected = len(column_list_input)
                    output = ''
                    output += '<html><body>'
                    output += '*Note the timestamp on file is not consecutive numbers <br>'
                    output += '*If the corresponding Start Time is not on record, the previous recorded timestamp is used <br>'
                    output += '*If the corresponding End Time is not on record, the next recorded timestamp is used <br>'
                    # Try to implement code here so one or multiple files can be selected
                    # single file 
                    if len(file_list_input) <2:
                        file_in_use = pd.read_csv('%s%s.csv' % (ROOT_DIR, file_list_input[0]))                         
                        file_in_use.set_index('TS',inplace = True, drop = False)
                        index = 0
                        column_used = ['TS']
                        position = 0
                        while index < num_of_columns_selected: 
                            column_used.append(column_list_input[index])
                            index += 1   
                        column_selected_TS = file_in_use[column_used]
                        printed_version = column_selected_TS.head(line_num)
                        df2 = printed_version.to_string(index=False)
                        if common(self_path_list, "*"):
                            df2 = column_selected_TS.to_string(index=False)
                        output += '%s' %file_list_input[0] 

                    if len(file_list_input) > 1:
                        print("Will continue working on this")
                        ## Below code works if concatnation is needed
                        # all_files = glob.glob(os.path.join(ROOT_DIR, "*.csv"))
                        # df_from_each_file = (pd.read_csv(f) for f in all_files)
                        # concatenated_file = pd.concat(df_from_each_file, ignore_index=True)
                        # print(concatenated_file)
                        
                        # index = 0
                        # while index < num_of_columns_selected: 
                        #     column_selected_TS = file_in_use[['TS', column_list_input[index]]]
                        #     printed_version = column_selected_TS.head(line_num)
                        #     df2 = printed_version.to_string(index=False)
                        #     if common(self_path_list, "*"):
                        #         df2 = column_selected_TS.to_string(index=False)
                        #     index += 1
                        #     output += '%s' %file_list_input[position]
########################################################################################

                    if not contain_timestamp:
                        output += '<pre>' 
                        output += '%s' % df2
                        output += '</pre>'
                        output += '</body></html>'        
                    
                    #localhost:8000/AMPds/B1E/V@1333263650~1333264030      
                    if contain_timestamp:
                        length = len(time)
                        i = 0
                        j = 0
                        start_list = []
                        end_list = []

                        for times in time:
                            time_col = times.split("~")
                            start_end_list.append(time_col)
                                
                        for item in exclusion_time:
                            if item.find("~") != -1:
                                time_col = item.split("~")
                                exclusion_start_end_list.append(time_col)
                        
                        while i<length:
                            start = df["TS"].loc[df['TS']<= int(float(start_end_list[i][0]))].max()
                            end = df["TS"].loc[df['TS'] >= int(float(start_end_list[i][1]))].min()
                            start_list.append(start)
                            end_list.append(end)
                            i += 1

                        while j<length:
                            df_time = column_selected_TS.loc[start_list[j]:end_list[j]]
                            df_time_with_selected_column = df_time.to_string(index=False)
                            output += '<pre>' 
                            output += '%s' % df_time_with_selected_column
                            output += '</pre>'
                            output += '</body></html>'
                            j += 1
                    
                
                        if len(exclusion_time) != 0:
                            exculsion_start = df["TS"].loc[df['TS']<= int(float(exclusion_start_end_list[0][0]))].max()
                            exculsion_end = df["TS"].loc[df['TS'] >= int(float(exclusion_start_end_list[0][1]))].min()
                            df_2 = column_selected_TS.loc[exculsion_start:exculsion_end]
                            list = df_2['TS']
                            exclusion_df = column_selected_TS.index.isin(list)
                            df2 = column_selected_TS[~exclusion_df].head(line_num)
                            df_time_with_selected_column = df2.to_string(index=False)
                            df_exclusion = df_time_with_selected_column
                            output += '<pre>' 
                            output += '%s' % df_exclusion
                            output += '</pre>'
                            output += '</body></html>'

            
        

        if len(self_path_list) >0 :                            
                statement = True

        

        # start_timestamp			end_timestamp
        # 1333263600  			1364799540

        # if len(self_path_list) == 2:
        #     if contain_data:                                   
        #         statement = True#     else:                             
        #         statement = False
        # if len(self_path_list) == 3:
        #     if contain_data and contain_file:                  
        #         statement = True
        #     else:            
        #         statement = False
        # if len(self_path_list) == 4:
        #     if contain_data and contain_file and contain_column:          
        #         statement = True
        #     else:             
        #         statement = False
        # if len(self_path_list) == 5:
        #     statement = True
        # # if len(self_path_list) == 5:
        # #     if contain_data and contain_file and contain_column and self_path_list[-1] == '*':          
        # #         statement = True
        # #     elif contain_data and contain_file and contain_column and len(self_path_list[-1]) == 21 and start < end:
        # #         statement = True
        # if len(self_path_list) >= 6:         
        #     statement = True
            

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
    slist2 = set(lst2)
    return [x for x in lst1 if x in slist2]
                              

def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   

if __name__ == '__main__':
    main()

