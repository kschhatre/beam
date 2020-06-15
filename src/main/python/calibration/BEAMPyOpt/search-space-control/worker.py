# Author: Kiran Chhatre
from initializers import initializers
import pandas as pd 
import subprocess, os, shutil, glob, time

shared = '/home/berkeleylab/Model/storage'
beam = '/home/berkeleylab/Repository/beam'

df =  pd.read_csv(glob.glob(shared+'/1_*.csv'))
num_neg_directionality = (df.loc['Positive_Directionality']==0).astype(int).sum() 

# Constants
# !!! UNDER THE ASSUMPTION THAT ONCE FOUND THE NEGATIVE DIRECTIONALITY DOES NOT CHANGE !!! (Opportunity to include this corner case later.)

if num_neg_directionality == 1 or num_neg_directionality == 5: 
    # 35,35,18,18,9,9
    base_iter = 70
    f_f_stage = 18     
elif num_neg_directionality == 2 or num_neg_directionality == 6:
    # 40,40,20,20,10,10
    base_iter = 80
    f_f_stage = 20
elif num_neg_directionality == 3 or num_neg_directionality == 7:
    # 30,30,16,16,8,8
    base_iter = 60
    f_f_stage = 16
elif num_neg_directionality == 4:
    #36,36,18,18,9,9 
    base_iter = 72
    f_f_stage = 18

finaliteration = '0'
p = 25 # intercepts
q = 13 # last iterations

# Args

base_all_args = ['base_nudge',list(range(1, base_iter+1)) , None] 
stage_all_args = ['linear_inter_extra_polate', [list(range(1, f_f_stage+1)), list(range(1, f_f_stage+1)), list(range(1, int(f_f_stage/2)+1)), list(range(1, int(f_f_stage/2)+1))], ['1_1', '1_2', '2_1', '2_2']]
advanced_nudge_args = [None, None, None]
send_2_BOHB_args = ['send_2_BOHB', None, None]

# Methods

def create_conf_copies(no_iters):
    for num in range(no_iters):
        shutil.copy(beam+'/test/input/sf-light/urbansim-10k.conf',beam+'/test/input/sf-light/urbansim-10k_'+str(num+1)+'.conf')

def ext_change(param):
if param == 'edit':
    os.rename(picked_conf_file, picked_conf_file[:-4] + 'txt')
elif param == 'save':
    for filename in glob.iglob(os.path.join(Repo, 'test/input/'+selected_sim+'/',conf_identifier+'txt' )):
        os.rename(filename, filename[:-3] + 'conf')

def del_conf_copies():
    for filename in glob.glob(beam+'/test/input/sf-light/urbansim-10k_*.conf'):  
        os.remove(filename)

def change_conf(input_vector):
    with open(beam+'/test/input/sf-light/urbansim-10k_'+str(i)+'.txt', 'r') as fin: 
        file_text=fin.readlines()

    # Adding the intercepts values

    for i in range(p,p+8,1):               
        file_text[i] = file_text[i].split('=',1)[0]+'= '

    file_text[p]   = file_text[p]  +str(input_vector[1]) #car_intercept
    file_text[p+1] = file_text[p+1]+str(input_vector[8]) #walk_transit_intercept
    file_text[p+2] = file_text[p+2]+str(input_vector[3]) #drive_transit_intercept
    file_text[p+3] = file_text[p+3]+str(input_vector[6]) #ride_hail_transit_intercept
    file_text[p+4] = file_text[p+4]+str(input_vector[4]) #ride_hail_intercept
    file_text[p+5] = file_text[p+5]+str(input_vector[5]) #ride_hail_pooled_intercept
    file_text[p+6] = file_text[p+6]+str(input_vector[7]) #walk_intercept
    file_text[p+7] = file_text[p+7]+str(input_vector[0]) #bike_intercept
        
    for j in range(p,p+8,1):
        file_text[j] = file_text[j]+' \n'

    # Repairing the lastiteration value of the conf file

    for i in range(q,q+1,1):                
        file_text[i] = file_text[i].split('=',1)[0]+'= '

    file_text[q] = file_text[q]+finaliteration
            
    for j in range(q,q+1,1):
        file_text[j] = file_text[j]+' \n'
        
    with open(beam+'/test/input/sf-light/urbansim-10k_'+str(i)+'.txt', 'w') as fini:
        for i in file_text:
            fini.write(i)

# Recipe

def recipe():

    # Base trials
    create_conf_copies(base_iter)
    output_folder_base = []
    input_vector_base = []
    for i in range(len(base_all_args[1])):
        input_vector = initializers(what_type=base_all_args[0], which_iter=base_all_args[1][i], which_stage=base_all_args[2])
        input_vector_base.append(input_vector)
        ext_change('edit')  
        change_conf(input_vector)            
        ext_change('save')
        with open(beam+"instanceconfpath.txt", "w") as text_file: 
            text_file.write('test/input/sf-light/urbansim-10k_'+str(i)+'.conf')
        subprocess.call([Repo+'runme.sh'])
        time_now = time.ctime()
        
        for i in range(len(glob.glob(beam+'/output/sf-light/*'))):
            while not time.ctime(os.path.getctime(glob.glob(beam+'/output/sf-light/*')[i])) > time_now:
                time.sleep(1)
            output_folder_base.append(glob.glob(beam+'/sf-light/*')[i])
    
    # This bottom part can be improved further! Example: iterating over a dynamic list.

    while not len(output_folder_base) == base_iter:
        time.sleep(1)
    
    for i in range(len(output_folder_base)):
        out_file = output_folder_base[i] + 'referenceRealizedModeChoice.csv'
        while not os.path.exists(out_file):
            time.sleep(1) 
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
        df.loc['v_dIntercept'] = [0,0,0,0,0,0,0,0,0]
        total_L1 = df.loc['L1'].abs().sum()
        df.to_csv(shared+'/'+str(i)+'_'+total_L1+'.csv', sep='\t', encoding='utf-8')  

    del_conf_copies()

    # 1_1 trials

    # 1_2 trials

    # 2_1 trails

    # 2_2 trials

   



    
 







