# Author: Kiran Chhatre
# Implementation 2 related
import numpy as np 
import pandas as pd 
import itertools, glob, fnmatch, os, random, csv
import warnings
from config import *

warnings.simplefilter(action='ignore', category=FutureWarning)

def getNudges(whichCounter):

    input_vector = []
    total_rel_nudge_trials = 36
    rel_nudge_stages = list(range(8,total_rel_nudge_trials+1,4)) # [8, 12, 16, 20, 24, 28, 32, 36]

    if whichCounter == 8:
        last_needed_csv = 1
    else:
        last_needed_csv = rel_nudge_stages[rel_nudge_stages.index(whichCounter)-1] 

    last_needed_csv_path = glob.glob(shared+'/'+str(last_needed_csv)+'_*.csv')[0] 
    validate = any([len(fnmatch.filter(os.listdir(shared), '*.csv')) == last_needed_csv, len(fnmatch.filter(os.listdir(shared), '*.csv')) > last_needed_csv-1]) 
    while not os.path.exists(last_needed_csv_path):                       # Condition 1 to verify the file exists
        time.sleep(5) 
        print('In relativeFactoredNudges: waiting for the last BEAM output csv...') 
    while not validate:                                                   # Condition 2 to be true
        time.sleep(5)
        print('Waiting to validate required number of csv files for nudge compuations...')  

    if whichCounter == 8:
        print('Creating nudges for stage 1...')
        csv_name = glob.glob(shared+'/1_*.csv')[0]  
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
        # example if last needed csv = 12 (say 'i'), we will compute nudges for 9,10,11,12 trails from (1,5),(2,6),(3,7), and (4,8) pairs.
        # input_vector = i-3 i-2 i-1 i-0   |@16| 13 14 15 16  |@12| 9 10 11 12
        # prev         = i-11 i-10 i-9 i-8 |   | 5 6 7 8      |   | 1 2 3 4
        # next         = i-7 i-6 i-5 i-4   |   | 9 10 11 12   |   | 5 6 7 8
        iterators_ip_vec, iterators_prev, iterators_next = list(range(3,-1,-1)), list(range(11,7,-1)), list(range(7,3,-1))
        
        for i in range(4):
            df_prev =  pd.read_csv(glob.glob(shared+'/'+str(whichCounter-iterators_prev[i])+'_*.csv')[0])
            df_next =  pd.read_csv(glob.glob(shared+'/'+str(whichCounter-iterators_next[i])+'_*.csv')[0]) 
            #INFO: df_next.loc[4] is  row and df_next.iloc[:,4] is column 
            # Create a separate df from df_next with 2 cols: L1 and L1_rank
            Rank_L1_df = df_next.loc[3:4].T 
            # Compute relative ratios of top 4 worst performing mode choices wrt to observed L1 norms
            # Example: {'ride_hail': 1.0, 'walk_transit': 0.45877255803345796, 'walk': 0.40894045161300785, 'ride_hail_transit': 0.3808596172941896}
            fetch_ratios = {}
            for i in range(1,5):
                fetch_ratios[list(Rank_L1_df.loc[Rank_L1_df.iloc[:, 1] == int('{i}'.format(i=i)),3].to_dict().keys())[0]] = abs(list(Rank_L1_df.loc[Rank_L1_df.iloc[:, 1] == int('{i}'.format(i=i)),3].to_dict().values())[0] / list(Rank_L1_df.loc[Rank_L1_df.iloc[:, 1] == 1,3].to_dict().values())[0])
            relative_variation_factor = df_next.loc[3].to_dict()
            del relative_variation_factor['iterations']
            relative_variation_factor = dict.fromkeys(relative_variation_factor, 0)
            # update relative variation factors for all mode choices
            # Example: {'bike': 0, 'car': 0, 'drive_transit': 0, 'ride_hail': 1.0, 'ride_hail_pooled': 0, 'ride_hail_transit': 0.3808596172941896, 'walk': 0.40894045161300785, 'walk_transit': 0.45877255803345796}
            relative_variation_factor.update(fetch_ratios) 
            # create a df of rows: intercepts_now and L1 for first 2 rows from df_prev and next 2 from df_next
            compute_df = pd.concat([df_prev.loc[list(range(0,1)) + list(range(3,4))],df_next.loc[list(range(0,1)) + list(range(3,4))]], ignore_index=True, sort =False)  
            del compute_df['iterations']
            # compute d_L1/d_m = (L1_next-L1_prev)/(m_next-m_prev) where m: intercept and this value is an !!! ABSOLUTE VALUE
            # required addition or substraction is taken care of by other variables
            compute_df.loc['d_L1/d_m'] = abs(compute_df.loc[3].astype(float) - compute_df.loc[1].astype(float)) / abs(compute_df.loc[2].astype(float) - compute_df.loc[0].astype(float))
            # check if L1 has decreased or not: 1 yes, 0 no
            compute_df.loc['L1_progress'] = [ 1 if min([compute_df.loc[1][x], compute_df.loc[3][x]], key=abs) == compute_df.loc[3][x]  else 0 for x in range(len(compute_df.loc[3]))]
            # check if modes were incremented or decremented: 1 decremented, 0 incremented
            compute_df.loc['m_progress'] = [ 1 if min([compute_df.loc[0][x], compute_df.loc[2][x]], key=abs) == compute_df.loc[2][x]  else 0 for x in range(len(compute_df.loc[3]))]
            # compute direction for the nudge: 1 negative, 0 positive
            # Analogy: if L1 has decreased -> follow the same pattern in modes(increments remains increment and so on), otherwise reverse the sign (increments changes to decrement and so on)
            compute_df.loc['nudge_direction'] = [ compute_df.loc['m_progress'][x] if compute_df.loc['L1_progress'][x].astype(int) == 1  else 1-compute_df.loc['m_progress'][x].astype(int) for x in range(len(compute_df.loc[3]))]
            # append previously computed relative factors
            compute_df.loc['factor'] = relative_variation_factor
            # finally calculate the input vector for the subsequent stage
            # Formula: m_(t+1) = m_(t) +or- (relative_factor) * (d_L1/d_m)
            # !!! REMINDER: we are only optimizing the worst performing first four mode choices !!!
            # However the top 4 worst performing mode choices are recalculated at each stage, so once the higher worse performing choices are optimized, the model will automatically shift the optimization towards the lesser worse performing mode choices
            compute_df.loc['m_(t+1)'] = [compute_df.loc[2][x]-compute_df.loc['factor'][x]*compute_df.loc['d_L1/d_m'][x] if compute_df.loc['nudge_direction'][x].astype(int) == 1 else compute_df.loc[2][x]+compute_df.loc['factor'][x]*compute_df.loc['d_L1/d_m'][x] for x in range(len(compute_df.loc[3]))]
            input_vector.append(compute_df.loc['m_(t+1)'].tolist()) 

        # at the end of this loop, it will return 4 input vectors

    return input_vector




  
