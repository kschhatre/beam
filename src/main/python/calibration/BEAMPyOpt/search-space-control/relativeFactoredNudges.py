# Author: Kiran Chhatre
# Implementation 2 related
import numpy as np 
import pandas as pd 
import itertools, glob, fnmatch, os, random, csv
from modify_csv import modify_csv
import warnings
from config import *

warnings.simplefilter(action='ignore', category=FutureWarning)

def getNudges():
    input_vector = []
    if (len(fnmatch.filter(os.listdir(shared), '*.csv')) == 1):
        csv_name = glob.glob(shared+'/1_*.csv')[0]
        modify_csv(csv_name=csv_name)   
        df =  pd.read_csv(csv_name)    
        for j in range(7): 
            vector_4_gradients = []
            for i in range(1,len(df.loc[5])):
                if (df.loc[5][i] == 1):
                    vector_4_gradients.append(random.sample(range(1, 18),1))
                else:
                    vector_4_gradients.append(random.sample(range(-18, -1),1))
            del vector_4_gradients[2]
            vector_4_gradients = list(itertools.chain(*vector_4_gradients))
            input_vector.append(vector_4_gradients)  # 7 vector for first 8 runs based on the directionality

    else:
        total_rel_nudge_trials = 36
        rel_nudge_stages = list(range(8,total_rel_nudge_trials+1,4)) # [8, 12, 16, 20, 24, 28, 32, 36]

        for i in range(len(rel_nudge_stages)): 
            last_needed_csv = glob.glob(shared+'/'+str(i)+'_*.csv')
            while not os.path.exists(last_needed_csv):
                time.sleep(1) 
            if os.path.isfile(last_needed_csv):
                if (len(fnmatch.filter(os.listdir(shared), '*.csv')) == rel_nudge_stages[i]):
                    # example if last needed csv = 8, we will compute nudges for 9,10,11,12 trails from (1,2),(3,4),(5,6), and (7,8) pairs.
                    #input_vector = i+1 i+2 i+3 i+4
                    #prev = i-7 i-6 i-5 i-4
                    #next = i-3 i-2 i-1 i
                    iterators_ip_vec, iterators_prev, iterators_next = list(range(1,5)), list(range(7,3,-1)), list(range(3,-1,-1))

                    for i in range(len(iterators_ip_vec)):
                        df_prev =  pd.read_csv(glob.glob(shared+'/'+str(iterators_prev[i])+'_*.csv'))
                        df_next =  pd.read_csv(glob.glob(shared+'/'+str(iterators_next[i])+'_*.csv')) 
                        #df_next.loc[4] is  row and df_next.iloc[:,4] is column
                        Rank_L1_df = df_next.loc[3:4].T
                        fetch_ratios = {}
                        for i in range(1,5):
                            fetch_ratios[list(Rank_L1_df.loc[Rank_L1_df.iloc[:, 1] == int('{i}'.format(i=i)),3].to_dict().keys())[0]] = abs(list(Rank_L1_df.loc[Rank_L1_df.iloc[:, 1] == int('{i}'.format(i=i)),3].to_dict().values())[0] / list(Rank_L1_df.loc[Rank_L1_df.iloc[:, 1] == 1,3].to_dict().values())[0])
                        relative_variation_factor = df_next.loc[3].to_dict()
                        del relative_variation_factor[' iterations  ']
                        relative_variation_factor = dict.fromkeys(relative_variation_factor, 0)
                        relative_variation_factor.update(fetch_ratios) # relative variation factors computed
                        # compute d_L1/d_m ratio
                        compute_df = pd.concat([df_next.ix[list(range(0,1)) + list(range(3,4))],df_prev.ix[list(range(0,1)) + list(range(3,4))]], ignore_index=True, sort =False)  
                        del compute_df[' iterations  ']
                        compute_df.loc['d_L1/d_m'] = abs(compute_df.loc[3].astype(float) - compute_df.loc[1].astype(float)) / abs(compute_df.loc[2].astype(float) - compute_df.loc[0].astype(float))
                        # check if L1 has decreased or not: 1 yes, 0 no
                        compute_df.loc['L1_progress'] = [ 1 if min([compute_df.loc[1][x], compute_df.loc[3][x]], key=abs) == compute_df.loc[3][x]  else 0 for x in range(len(compute_df.loc[3]))]
                        # check if modes were incremented or decremented: 1 decremented, 0 incremented
                        compute_df.loc['m_progress'] = [ 1 if min([compute_df.loc[0][x], compute_df.loc[2][x]], key=abs) == compute_df.loc[2][x]  else 0 for x in range(len(compute_df.loc[3]))]
                        # compute direction for the nudge: 1 negative, 0 positive
                        compute_df.loc['nudge_direction'] = [ compute_df.loc['m_progress'][x] if compute_df.loc['L1_progress'][x].astype(int) == 1  else 1-compute_df.loc['m_progress'][x].astype(int) for x in range(len(compute_df.loc[3]))]
                        # compute new intercepts
                        compute_df.loc['factor'] = relative_variation_factor
                        compute_df.loc['m_(t+1)'] = [compute_df.loc[2][x]-compute_df.loc['factor'][x]*compute_df.loc['d_L1/d_m'][x] if compute_df.loc['nudge_direction'][x].astype(int) == 1 else compute_df.loc[2][x]+compute_df.loc['factor'][x]*compute_df.loc['d_L1/d_m'][x] for x in range(len(compute_df.loc[3]))]
                        input_vector.append(compute_df.loc['m_(t+1)'].tolist())
            else:
                raise ValueError("%s file isn't ready yet!" % file_path) 
    return input_vector




  
