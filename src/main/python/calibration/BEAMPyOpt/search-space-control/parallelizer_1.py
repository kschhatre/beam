# Author: Kiran Chhatre
# Implementation 2 related
from multiprocessing import Process
import random, time, psutil, logging, sys, multiprocessing, subprocess, glob, os
from worker_1 import fire_BEAM, bookkeep

#sys.stdout=open("test.txt","w")     # if required to export the outputs to a file

beam = '/home/ubuntu/beam'   
BEAM_procs = []
bookkeeping_procs = []

# information inline to the info fed in the worker
total_rel_nudge_trials = 36
rel_nudge_stages = list(range(8,total_rel_nudge_trials+1,4))
counter = list(range(len(rel_nudge_stages)+1))
bookkeeping_iters = [7]+[4]*len(rel_nudge_stages) 

for k in range(len(counter)): # per stage start x=(number of parallel pass 7 or 4) and 1(for bookkeeping) procs

    while True:
        with open(beam+"/writecue.txt", 'r') as fin: 
            file_text=fin.readlines()
        print('Waiting for the write cue...')
        if file_text == 'write stage '+str(k+1)+' done': 
            break 

    if k == 0:
        parallel_passes = list(range(7))
    else:
        parallel_passes = list(range(4))        

    for m in range(len(parallel_passes)):               
        #multiprocessing.log_to_stderr(logging.DEBUG)
        if parallel_passes == 7:
            which_conf = int(m + 1)  
        else:
            which_conf = int(rel_nudge_stages[k] - m) 
        p = Process(target=fire_BEAM, args=(which_conf))
        p.start()
        BEAM_procs.append(p)

    with open(beam+"/firecue.txt", "w") as text_file: 
        text_file.write('fire '+str(k+1)+' done')    

    q = Process(target=bookkeep, args=(int(k+1)))  
    q.start()
    bookkeeping_procs.append(q) 

'''
for filename in glob.glob(beam+'/test/input/sf-light/urbansim-10k_*'):  
    os.remove(filename)
'''

for p in BEAM_procs:
   p.join()

for q in bookkeeping_procs:
   q.join()

#sys.stdout.close()     # if required to export the outputs to a file

