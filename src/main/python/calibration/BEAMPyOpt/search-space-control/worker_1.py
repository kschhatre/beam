# Author: Kiran Chhatre
# Implementation 2 related

from relativeFactoredNudges import getNudges
from config import *
import pandas as pd 
import subprocess, os, shutil, glob, time, fnmatch
from modify_csv import modify_csv


# NO MECHANISM TO START 0TH ITERATION WITH ALL ZERO INTERCEPTS. Design it accordingly! Current workaround: run correlational_1.py before running parallelizer_1.py

# iterator
total_rel_nudge_trials = 36
rel_nudge_stages = list(range(8,total_rel_nudge_trials+1,4)) # 8, 12, 16, 20, 24, 28, 32, 36

# constants
finaliteration = '0'
p = 24 # intercepts
q = 13 # last iterations
time_now_for_stages = []

# Methods

def create_conf_copies(no_iters, which_stage):    
    if which_stage == 8:
        for num in range(no_iters): # no_iters = 7
            shutil.copy(base_urbansim_config, copy_urbansim_config % (num+2))  
    else: # which_stage is 12, 16, 20, 24, 28, 32, 36
        for num in range(no_iters): # no_iters = 4
            shutil.copy(base_urbansim_config, copy_urbansim_config % (which_stage-num))

def ext_change(param, picked_conf_file, filename):
    if param == 'edit':
        os.rename(picked_conf_file, picked_conf_file[:-4] + 'txt')    
    elif param == 'save':  
        os.rename(filename, filename[:-3] + 'conf')

def change_conf(input_vector, filename):
    with open(filename, 'r') as fin: 
        file_text=fin.readlines()

    # Adding the intercepts values

    for i in range(p,p+8,1):               
        file_text[i] = file_text[i].split('=',1)[0]+'= '

    '''
    MATCHING INDICES FROM MEMORY BANK CSVS TO CONF MODE CHOICES:
    Output CSV:
    bike,car,drive_transit,ride_hail,ride_hail_pooled,ride_hail_transit,walk,walk_transit
    0    1   2             3         4                5                 6    7              
    CONF:
    car,walk_transit,drive_transit,ride_hail_transit,ride_hail,ride_hail_pooled,walk,bike
    0   1            2             3                 4         5                6    7
    Line number in Conf file:
    25  26           27            28                29        30               31   32
    file_text index will be: line number in conf - 1
    required input_vector indices:
    1   7            2             5                 3         4                6    0
    '''

    file_text[p]   = file_text[p]  +str(input_vector[1]) #car_intercept
    file_text[p+1] = file_text[p+1]+str(input_vector[7]) #walk_transit_intercept
    file_text[p+2] = file_text[p+2]+str(input_vector[2]) #drive_transit_intercept
    file_text[p+3] = file_text[p+3]+str(input_vector[5]) #ride_hail_transit_intercept
    file_text[p+4] = file_text[p+4]+str(input_vector[3]) #ride_hail_intercept
    file_text[p+5] = file_text[p+5]+str(input_vector[4]) #ride_hail_pooled_intercept
    file_text[p+6] = file_text[p+6]+str(input_vector[6]) #walk_intercept
    file_text[p+7] = file_text[p+7]+str(input_vector[0]) #bike_intercept
        
    for j in range(p,p+8,1):
        file_text[j] = file_text[j]+' \n'

    # Repairing the lastiteration value of the conf file

    for i in range(q,q+1,1):                
        file_text[i] = file_text[i].split('=',1)[0]+'= '

    file_text[q] = file_text[q]+finaliteration
            
    for j in range(q,q+1,1):
        file_text[j] = file_text[j]+' \n'
        
    with open(filename, 'w') as fini:
        for i in file_text:
            fini.write(i)

def vector(whichCounter):
    input_vector = getNudges(whichCounter)  
    if whichCounter == 8:
        required = 7
    else:
        required = 4
    if len(input_vector) == required:
        return input_vector
    else:
        return vector(whichCounter)  



def find_op_folder(time_now, parallel_passes):  # increment op folder count
    output_folders = []
    for i in range(len(glob.glob(sf_light_dir))):
        if time.ctime(os.path.getctime(glob.glob(sf_light_dir)[i])) < time_now:
            pass 
        elif time.ctime(os.path.getctime(glob.glob(sf_light_dir)[i])) > time_now: 
            output_folders.append(glob.glob(sf_light_dir)[i]) if glob.glob(sf_light_dir)[i] not in output_folders else output_folders
    if any( [not output_folders, len(output_folders) < parallel_passes] ):
        return find_op_folder(time_now, parallel_passes)
    else:
        return output_folders 


# Recipe

def recipe():
    for i in range(len(rel_nudge_stages)):
        if i == 0:
            pass
        else:
            while True:
                time.sleep(5)
                print('Recipe method waiting to validate required number of csv files before calling the relativeFactoredNudges() at stage '+str(i+1)+' ...')
                if any([len(fnmatch.filter(os.listdir(shared), '*.csv')) > rel_nudge_stages[i-1]-1, len(fnmatch.filter(os.listdir(shared), '*.csv')) == rel_nudge_stages[i-1]]):
                    break    
        print('Recipe method initialized at stage '+str(i+1)+'!') 
        input_vector_now = vector(whichCounter=rel_nudge_stages[i])  
        if len(input_vector_now) == 7: # [[...],[...],[...],[...],[...],[...],[...]]
            parallel_passes = 7
        else: # len(input_vector_now) == 4
            parallel_passes = 4

        which_stage = rel_nudge_stages[i] 
        
        create_conf_copies(no_iters=parallel_passes,which_stage=which_stage)
        print('Conf copies created for stage '+str(i+1)+'!') 
        for j in range(parallel_passes):
            if which_stage == 8:
                picked_conf_file = copy_urbansim_config % (j+2) 
                filename = copy_urbansim_txt % (j+2)  
                ext_change('edit', picked_conf_file, filename)
            else:
                picked_conf_file = copy_urbansim_config % (which_stage-j)
                filename = copy_urbansim_txt % (which_stage-j) 
                ext_change('edit', picked_conf_file, filename)
            print('Input vector at stage '+str(i+1)+'.'+str(j+1)+' is:') 
            print(input_vector_now[j])
            change_conf(input_vector=input_vector_now[j], filename=filename)     
            ext_change('save', picked_conf_file, filename)   

        print('All conf files ready for stage '+str(i+1)+'!') 
        with open(beam+"/writecue.txt", "w") as text_file:
            text_file.write('write stage '+str(i+1)+' done') 

        while True: 
            print('Checking firecue file content size...')
            while True:
                if os.path.getsize(beam+"/firecue.txt") > 0:
                    break 
            with open(beam+"/firecue.txt", 'r') as fin:  
                file_text=fin.readlines()
            time.sleep(5)
            print('Waiting for the fire cue...') 
            if file_text[0] == 'fire '+str(i+1)+' done':
                break
        time_now_for_stages.append(time.ctime())
        print('Complete stage '+str(i+1)+' fired at time: '+str(time_now_for_stages[i])) 
  
   
def fire_BEAM(number):  
    import os
    print('BEAM fired on '+str(os.getpid())+' PID.')
    picked_conf_file = copy_urbansim_config % number   # label the file
    with open(beam + "/instanceconfpath.txt", "w") as text_file: 
        text_file.write(picked_conf_file)
    os.chdir(beam)
    subprocess.call([runme])
    os.chdir(search_space)

def bookkeep(which_stage):
    if which_stage == 1:
        how_many = 7
    else:
        how_many = 4 
    while True:
        time.sleep(5)
        print('Inside bookkeep(): checking if required optimization stage has been fired...')
        if len(time_now_for_stages) > which_stage-1: 
            break
    output_folders = find_op_folder(time_now=time_now_for_stages[which_stage-1], parallel_passes=how_many)
    for j in range(len(output_folders)):
        out_file = output_folders[j] + '/referenceRealizedModeChoice.csv'
        while not os.path.exists(out_file):
            time.sleep(5) 
            print('In bookkeep method: waiting for BEAM output...')
        if os.path.isfile(out_file):
            df =  pd.read_csv(out_file)
        else:  
            raise ValueError("%s isn't a file!" % file_path)
        df['iterations'][1] = 'modeshare_now'
        df.loc[-1] = ['intercepts_now'] + input_vector_base[i] 
        df.index = df.index+1 
        df.sort_index(inplace=True) 
        df.set_index('iterations', inplace=True)
        df.loc['L1'] = df.loc['benchmark'] - df.loc['modeshare_now']
        df.loc['L1_rank'] = df.loc['L1'].abs().rank(ascending=False)
        df.loc['Positive_Directionality'] =  df.loc['L1'].ge(0) 
        #df.loc['v_dIntercept'] = [0,0,0,0,0,0,0,0,0]
        total_L1 = df.loc['L1'].abs().sum()
        if which_stage == 1:
            df.to_csv(output_csv % (j+2, total_L1), sep='\t', encoding='utf-8')   
            csv_name = output_csv % (j+2, total_L1) 
            modify_csv(csv_name=csv_name)
        else:
            offset_labeling_list = list(range(7,50,3)) 
            iter_label = offset_labeling_list[which_stage-2] + int(which_stage) + j 
            df.to_csv(output_csv % (iter_label, total_L1), sep='\t', encoding='utf-8')   
            csv_name = output_csv % (iter_label, total_L1) 
            modify_csv(csv_name=csv_name) 