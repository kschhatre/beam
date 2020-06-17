import glob, csv, os

shared = '/home/ubuntu/beam/src/main/python/calibration/BEAMPyOpt/storage'  

def modify_csv(csv_name):
    reader = csv.reader(open(csv_name, "r"), delimiter='\t') 
    writer = csv.writer(open(shared+'/output.csv', 'w'), delimiter=',')   
    writer.writerows(reader) 
    os.remove(csv_name)  
    os.rename(shared+'/output.csv', shared+'/'+csv_name[34:])  
