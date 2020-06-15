# Author: Kiran Chhatre
import os, subprocess, time, glob, csv
import pandas as pd

beam_repo = '/home/berkeleylab/Repository/beam'
file_conf = '/home/berkeleylab/Repository/beam/test/input/sf-light/urbansim-10k.conf'
file_txt = '/home/berkeleylab/Repository/beam/test/input/sf-light/urbansim-10k.txt'
shared = '/home/berkeleylab/Model/storage'

################################### Edit phase
os.rename(file_conf, file_txt)

with open(file_txt, 'r') as fin:
    file_text = fin.readlines()

current_last_iter = int(file_text[13].split('= ',1)[1])
file_text[13].split('=',1)[0]+'= 0'

with open(file_text, 'w') as fini:  
    for i in file_text:
        fini.write(i)

os.rename(file_txt, file_conf)

subprocess.call(beam_repo+'/runme.sh')

################################### Iteration Count

with open(shared+'/total_iters.txt', 'w') as f:
    f.write(1)

iter_now = open(shared+'/total_iters.txt', 'r')

################################### Repair phase (maintaining original lastIteration value)
os.rename(file_conf, file_txt)

with open(file_txt, 'r') as fin:
    file_text = fin.readlines()

file_text[13].split('=',1)[0]+str(current_last_iter)+' \n'

with open(file_text, 'w') as fini:
    for i in file_text:
        fini.write(i)

os.rename(file_txt, file_conf)

################################### Bookkeeping phase

out_dir = max(glob.glob(os.path.join(beam_repo+'/output/sf-light', '*/')), key=os.path.getmtime)
out_file = out_dir + 'referenceRealizedModeChoice.csv'

while not os.path.exists(out_file):
    time.sleep(1) 

if os.path.isfile(out_file):
    df =  pd.read_csv(out_file)
else:
    raise ValueError("%s isn't a file!" % file_path)

df['iterations'][1] = 'modeshare_now'
df.loc[-1] = ['intercepts_now', 0,0,0,0,0,0,0,0,0]
df.index = df.index+1 
df.sort_index(inplace=True)
df.set_index('iterations', inplace=True)
df.loc['L1'] = df.loc['benchmark'] - df.loc['modeshare_now']
df.loc['L1_rank'] = df.loc['L1'].abs().rank(ascending=False)
df.loc['Positive_Directionality'] =  df.loc['L1'].ge(0) 
df.loc['v_dIntercept'] = [0,0,0,0,0,0,0,0,0]
total_L1 = df.loc['L1'].abs().sum()

# intercepts_now, benchmark, modeshare_now, L1, L1_rank, Positive_Directionality, v_dIntercept
df.to_csv(shared+'/'+iter_now+'_'+total_L1+'.csv', sep='\t', encoding='utf-8')

