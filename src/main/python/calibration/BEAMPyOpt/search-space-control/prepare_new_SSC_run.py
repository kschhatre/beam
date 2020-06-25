from config import *
import os, subprocess, glob

'''
1. Deletes all *.log file in BEAM dir
2. Deletes all urbansim-10k_*.conf or txt files from sf-light folder
3. Deletes all files except 1_*.csv from the storage folder
'''

for item in os.listdir(beam):
    if item.endswith(".log"): 
        os.remove(os.path.join(beam, item)) # point 1

for filename in glob.glob(sf_light_ip_dir+'/urbansim-10k_*'):
    os.remove(filename) # point 2

os.chdir(shared)
bashCommand = "find . \! -name '1_*.csv' -a \! -name '*.py' -a \! -type d -delete"
subprocess.Popen(bashCommand, shell=True, executable='/bin/bash') # point 3
os.chdir(search_space)
print('Ready for a fresh SSC run!')