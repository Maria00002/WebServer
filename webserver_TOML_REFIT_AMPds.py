from ctypes import sizeof
import re
import pandas as pd
import tomllib
from http.server import HTTPServer, BaseHTTPRequestHandler

WEBSERVER_TOML = 'C:\\Maria\\Figure 17 Research Paper\\webserver\\'

class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global line_num
        line_num = 10

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

        # self_path_list and if contain data/file/column
        self_path_list = re.split(r'[/@]', self.path)
        logic_path = self_path_list

        #using data stored in webserver TMOL file
        with open ('%s%s'%(WEBSERVER_TOML, 'webserver.toml'), mode = "rb") as file:
            webserver = tomllib.load(file)       

        # localhost:8000/AMPds
        # localhost:8000/REFIT
        contain_data = list_contains(self_path_list, webserver["data"])
        if contain_data:
            self_response(200)
            output = ''
            output += '<html><body>'			
            output += '<h1>%s</h1>' %(self_path_list[1])
            output += '<link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon">' #added to prevent favicon.ico request
            output += '</body></html>'

            if len(self_path_list) >= 3:                                            
                contain_file = str_contains_in_list(self_path_list[2], list(webserver[self_path_list[1]].keys()))            
                if contain_file:
                    output = ''
                    output += '<html><body>'
                    output += '<link rel="shortcut icon" href="data:image/x-icon;," type="image/x-icon">' #added to prevent favicon.ico request

                    df = pd.read_csv('%s%s\\%s' % (webserver['directories']["WINDOWS_ROOT_DIR"],self_path_list[1], webserver[self_path_list[1]][self_path_list[2]]))
                    df.set_index('%s' %(webserver[self_path_list[1]]['primary_key']),inplace = True, drop = False)
                    # df = pd.to_numeric(df[df.columns.tolist()])
                    # print(df.dtypes)

                    output += 'This is file %s' %(self_path_list[2])
                    min_timestamp=df['%s' %(webserver[self_path_list[1]]['primary_key'])].min()
                    max_timestamp=df['%s' %(webserver[self_path_list[1]]['primary_key'])].max()
                    output += '<p>The minimum timestamp is %d and the maximum timestamp is %d </p>' %(min_timestamp,max_timestamp)
                    total_count = df['%s' %(webserver[self_path_list[1]]['primary_key'])].count()
                    output += '<p>The number of entries for time series data are %d </p>' %(total_count)
                    stats = df.describe()

                    output += '<pre>'
                    output += '<p>The statistical information </p>'
                    output +=  '%s' %(stats)
                    output += '</pre>'
                    output += '</body></html>'

                    #localhost:8000/AMPds/B1E/V (TS  V  I  f  DPF  APF  P  Pt  Q  Qt  S  St)
                    #localhost:8000/REFIT/House1/Appliance1 (Time Unix Aggregate Appliance1	Appliance2	Appliance3	Appliance4	Appliance5	Appliance6	Appliance7	Appliance8	Appliance9	Issues)
                    col_names = df.columns.tolist()

                    


                    if len(self_path_list) >= 4:
                        
                        contain_column = list_contains(self_path_list[3].split(r'+'), col_names)
                        # contain_column = self_path_list[3] in col_names
                        # inputted_columns = re.split(r'[+]', self_path_list[3])
                        # print(contain_column, col_names, self_path_list[3])
                        if self_path_list[-1].find("~") == -1:
                            not_contain_timestamp = True
                            contain_timestamp = False
                        elif self_path_list[-1].find("~") != -1:
                            not_contain_timestamp = False
                            contain_timestamp = True   
                        
                        if contain_column:
                            # print("if contain_column")
                            inputted_columns = re.split(r'[+]', self_path_list[3])
                            num_of_columns_selected = len(inputted_columns)

                            output = ''
                            output += '<html><body>'
                        
                            index = 0
                            column_used = ['%s' %(webserver[self_path_list[1]]['primary_key'])]
                            while index < num_of_columns_selected: 
                                column_used.append(inputted_columns[index])
                                index += 1   
                            # print(column_used)
                            # print(self_path_list)
                            column_selected_TS = df[column_used]
                            printed_version = column_selected_TS.head(line_num)
                            df2 = printed_version.to_string(index=False)
                            #localhost:8000/AMPds/B1E/V@* (TS  V  I  f  DPF  APF  P  Pt  Q  Qt  S  St) 
                            if common(self_path_list, "*"):
                                df2 = column_selected_TS.to_string(index=False)
                                if(self_path_list[-1] != "*"):
                                    try:
                                        cross_fold_integer = int(float(self_path_list[-1]))
                                    except ValueError as e:
                                        print(e)
                                        print("Please enter the cross fold value as an integer instead")
                                        page_404_not_found()
                                    # check if the last item in the list is an integer or not
                                    if isinstance(cross_fold_integer, int) == True: #if testing with string, there will be a ValueError: invalid literal for int() with base 10
                                        total_line = len(column_selected_TS)
                                        individual_line = int(total_line/cross_fold_integer)
                                        remainder = total_line-(individual_line*cross_fold_integer)
                                        elem = 1
                                        cross_fold_list = [] 
                                        while elem <= cross_fold_integer:
                                            a_list = [str(elem)]*individual_line
                                            cross_fold_list.extend(a_list)
                                            elem += 1
                                        remainder_list = [None] * remainder
                                        cross_fold_list.extend(remainder_list)
                                        column_selected_TS['Chunk'] = cross_fold_list
                                        df2 = column_selected_TS.to_string(index=False)
                            output += '%s' %self_path_list[2]
 
                            if not_contain_timestamp:
                                output += '<pre>' 
                                output += '%s' % df2
                                output += '</pre>'
                                output += '</body></html>'      

                            # # Time Selection
                            # # http://localhost:8000/AMPds/DWE/V@1333263600~1333264020   
                            if contain_timestamp: 
                                time_undivided = []
                                exclusion_time = []
                                time = []
                                if self_path_list[4].find("~") != -1:
                                    time_undivided.append(self_path_list[4])
                                    if time_undivided[0].find("+") != -1:
                                       time = re.split(r'[+]', time_undivided[0])
                                    else:
                                        time = time_undivided  
                                # print(time)
                                if self_path_list[4] == "":
                                    exclusion_time.append(self_path_list[5])

                                output += '<br>'
                                output += '*Note the timestamp on file is not consecutive numbers <br>'
                                output += '*If the corresponding Start Time is not on record, the previous recorded timestamp is used <br>'
                                output += '*If the corresponding End Time is not on record, the next recorded timestamp is used <br>'
                                                              
                                length = len(time)
                                
                                start_list = []
                                end_list = []
                                start_end_list = []
                                exclusion_start_end_list = []

                                for times in time:
                                    time_col = times.split("~")
                                    start_end_list.append(time_col)
                                        
                                for item in exclusion_time:
                                    if item.find("~") != -1:
                                        time_col = item.split("~")
                                        exclusion_start_end_list.append(time_col)
                                # print(start_end_list)
                                
                                primary_key = '%s' %(webserver[self_path_list[1]]['primary_key'])
                                i = 0
                                while i<length:
                                    start = df [primary_key].loc[df[primary_key]<= int(float(start_end_list[i][0]))].max()
                                    end = df [primary_key].loc[df[primary_key] >= int(float(start_end_list[i][1]))].min()
                                    start_list.append(start)
                                    end_list.append(end)
                                    i += 1
                                
                                j = 0
                                while j<length:
                                    df_time = column_selected_TS.loc[start_list[j]:end_list[j]]
                                    df_time_with_selected_column = df_time.to_string(index=False)
                                    output += '<pre>' 
                                    output += '%s' % df_time_with_selected_column
                                    output += '</pre>'
                                    output += '</body></html>'
                                    j += 1
                            
                                if len(exclusion_time) == 1:
                                    primary_key = '%s' %(webserver[self_path_list[1]]['primary_key'])
                                    exculsion_start = df[primary_key].loc[df[primary_key]<= int(float(exclusion_start_end_list[0][0]))].max()
                                    exculsion_end = df[primary_key].loc[df[primary_key] >= int(float(exclusion_start_end_list[0][1]))].min()
                                    df_2 = column_selected_TS.loc[exculsion_start:exculsion_end]
                                    col = df_2[primary_key]
                                    exclusion_df = column_selected_TS.index.isin(col)
                                    df2 = column_selected_TS[~exclusion_df].head(line_num)
                                    df_time_with_selected_column = df2.to_string(index=False)
                                    df_exclusion = df_time_with_selected_column
                                    output += '<pre>' 
                                    output += '%s' % df_exclusion
                                    output += '</pre>'
                                    output += '</body></html>'

        if len(logic_path) == 2:
            if contain_data:                                   
                statement = True
            else:                             
                statement = False
        if len(logic_path) == 3:
            if contain_data and contain_file:                  
                statement = True
            else:            
                statement = False
        if len(logic_path) > 3:
            statement = True

                ##
        # if len(logic_path) == 4:
        #     if contain_data and contain_file:
        #         column_input = re.split(r'[+]', logic_path[-1])
        #         for column in column_input:
        #             if list_contains(column, col_names):                 
        #                 statement = True
        #             else:            
        #                 statement = False
        # if len(logic_path) == 5 and logic_path[-1] == '*':
        #     statement = True
        # if len(logic_path) == 6 and logic_path[-2] == '*'and isinstance(cross_fold_integer, int) == True:
        #     statement = True
        # if len(logic_path) == 5:
        #     if logic_path[-1].find("~")!=-1:
        #         time_select = re.split(r'[+~]', logic_path[-1])
        #         if check_min(time_select, min_timestamp) and check_max(time_select, max_timestamp):
        #             statement = True
        #         else:
        #             statement = False
        # if len(logic_path) == 6:
        #     if logic_path[-2]=='' and logic_path[-1].find("~")!=-1:
        #         time_exclude = re.split(r'[~]', logic_path[-1])
        #         if check_min(time_exclude, min_timestamp) and check_max(time_exclude, max_timestamp):
        #             statement = True
        #         else:
        #             statement = False
        # if len(logic_path) > 6:                                   
        #     statement = False
          
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

def str_contains_in_list(str1,list1):
    if str1 in list1:
        return True
    else:
        return False

def common(lst1, lst2): 
    slist2 = set(lst2)
    return [x for x in lst1 if x in slist2]

def check_min(list1, val):
    return(all(int(float(x)) >= val for x  in list1))

def check_max(list1, val):
    return(all(int(float(x)) <= val for x in list1))

def main():
    PORT = 8000
    server = HTTPServer(('', PORT),requestHandler)
    print('Server running on port %s' % PORT)
    server.serve_forever()
   
if __name__ == '__main__':
    main()
