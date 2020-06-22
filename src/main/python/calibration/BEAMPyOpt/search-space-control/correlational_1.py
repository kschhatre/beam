# Author: Kiran Chhatre
# Implementation 2 related
import os, subprocess, time, glob, csv
import pandas as pd
from config import *

# KEEP ALL INTERCEPTS AS ZERO and KEEP OUTPUT FOLDER EMPTY!!

# Deleting shared o/p folder contents
filelist = [ f for f in os.listdir(shared) ]
for f in filelist:
    os.remove(os.path.join(shared, f))

################################### Fire BEAM
os.chdir(beam) 
subprocess.call(runme)
os.chdir(search_space)

################################### Bookkeeping phase

out_dir = glob.glob(sf_light_dir)

while not out_dir:
    time.sleep(1)

out_file = out_dir[0]+'/referenceRealizedModeChoice.csv'

if os.path.isfile(out_file):
    df =  pd.read_csv(out_file)
else:
    raise ValueError("%s isn't a file!" % file_path)

df.loc[1,'iterations'] = 'modeshare_now'
df.loc[-1] = ['intercepts_now', 0,0,0,0,0,0,0,0,0]
df.index = df.index+1 
df.sort_index(inplace=True)
df.set_index('iterations', inplace=True)
df.loc['L1'] = df.loc['benchmark'] - df.loc['modeshare_now']
df.loc['L1_rank'] = df.loc['L1'].abs().rank(ascending=False)
df.loc['Positive_Directionality'] =  df.loc['L1'].ge(0) 
total_L1 = df.loc['L1'].abs().sum()

# intercepts_now, benchmark, modeshare_now, L1, L1_rank, Positive_Directionality
df.to_csv(output_csv % (1, total_L1), sep='\t', encoding='utf-8')
