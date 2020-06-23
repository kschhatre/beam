import glob, csv, os
from config import *

def modify_csv(csv_name):
    reader = csv.reader(open(csv_name, "r"), delimiter='\t') 
    writer = csv.writer(open(shared+'/output.csv', 'w'), delimiter=',')   
    writer.writerows(reader) 
    os.remove(csv_name)  
    num = 77 # if on develop branch else 64
    os.rename(shared+'/output.csv', shared+'/'+csv_name[num:])  
