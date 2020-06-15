# Author: Kiran Chhatre
# Implementation 2 related
import os, subprocess, time, glob, csv
import pandas as pd

# KEEP ALL INTERCEPTS AS ZERO and KEEP OUTPUT FOLDER EMPTY!!

beam_repo = '/home/ubuntu/calibration_stage1/beam'
file_conf = '/home/ubuntu/calibration_stage1/beam/test/input/sf-light/urbansim-10k.conf'
file_txt  = '/home/ubuntu/calibration_stage1/beam/test/input/sf-light/urbansim-10k.txt'
shared    = '/home/ubuntu/calibration_stage1/storage' 

################################### Fire BEAM
os.chdir(beam_repo) 
subprocess.call(beam_repo+'/runme.sh')
os.chdir('/home/ubuntu/calibration_stage1/beam-calibration/search-space-control')

################################### Bookkeeping phase

out_dir = glob.glob(beam_repo+'/output/sf-light/*')

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
df.to_csv(shared+'/'+'1_'+str(total_L1)+'.csv', sep='\t', encoding='utf-8')

