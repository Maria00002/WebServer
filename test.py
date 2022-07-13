line_num=10
with open("C:\Maria\SFU\SFU Thesis\Figure 17 Research Paper\dataverse_files\excel_files\B1E.csv") as myfile:
    head = [next(myfile) for x in range(line_num)]
print(head)
print(type(head))
myfile.close()

data = [1,2,3]
max_id = max(list(data))  
print(max_id)

