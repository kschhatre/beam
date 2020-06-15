# Author: Kiran Chhatre
import itertools, glob, re
from functools import reduce
from operator import add
import pandas as pd

shared = '/home/berkeleylab/Model/storage'

# Maintain total_iters.txt to store iteration count info, also is it required since we are saving file names with iter count?

def initializers(what_type, which_iter, which_stage):
    
    df =  pd.read_csv(glob.glob(shared+'/1_*.csv'))
    num_neg_directionality = (df.loc['Positive_Directionality']==0).astype(int).sum() 

    # to do corner case: num_neg_directionality = 0 and 8

    def compute_intercept(prior_df, post_df):

        intercept_prior = prior_df.iloc[0]
        L1_prior = prior_df.iloc[3]
        intercept_post = post_df.iloc[0]
        L1_post = post_df.iloc[3]  
        v_dIntercept_prior = prior_df.iloc[6]
        dIntercept = (L1_prior[1:]-L1_post[1:])/(intercept_prior[1:]-intercept_post[1:])
        # Old implementation
        #m = (modeshare_prior[1:]-modeshare_post[1:])/(intercept_prior[1:]-intercept_post[1:])
        #del_nudges = (post_df.iloc[3][1:])/m              
        # Parameters:
        beta = 0.9
        alpha = 0.01 # optimization step size
        updated_v_dIntercept = list(map(add, list(map(lambda x: x * beta, v_dIntercept_prior)), list(map(lambda x: x * (1 - beta), dIntercept))))
        input_vector = intercept_post[1:] - list(map(lambda x: x * alpha, updated_v_dIntercept)) # analyse addition or substraction suitability
        return updated_v_dIntercept, input_vector

    if what_type == 'base_nudge':
        # returns updated nudge with 0.5 increment or decrement

        params = []
        for i in range(1,9):
            params.append(reduce(lambda x, k: x+"b" if k%2 else x+"a", range(i), "")) 

        # a, b = 5, 15
        neg_identifier, pos_identifier = params[num_neg_directionality-1], params[7-num_neg_directionality]

        p_permuts = set([''.join(a) for a in itertools.permutations(pos_identifier)])
        n_permuts = set([''.join(a) for a in itertools.permutations(neg_identifier)])

        total_combos = list(itertools.product(p_permuts, n_permuts)) #(p_permuts,n_permuts)

        ip_vec_grp = []
        for i in range(len(total_combos)):
            single_ip_vec=[]
            for j in range(len(total_combos[i][0])):
                if total_combos[i][0][j] == 'a':
                    single_ip_vec.append(5)
                elif total_combos[i][0][j]== 'b':
                    single_ip_vec.append(15)
            for k in range(len(total_combos[i][1])):
                if total_combos[i][1][k]== 'a':
                    single_ip_vec.append(-5)
                elif total_combos[i][1][k]== 'b':
                    single_ip_vec.append(-15)
            ip_vec_grp.append(single_ip_vec)

        next_ip_vec_grp = []
        for i in range(len(ip_vec_grp)):
            single_ip_vec=[]
            for j in range(len(ip_vec_grp[i])):
                if ip_vec_grp[i][j] > 0:
                    single_ip_vec.append(ip_vec_grp[i][j]+0.5)
                else:
                    single_ip_vec.append(ip_vec_grp[i][j]-0.5)
            next_ip_vec_grp.append(single_ip_vec)

        input_vector_group = ip_vec_grp + next_ip_vec_grp
        input_vector = input_vector_group[int(which_iter)]

    elif what_type == 'linear_inter_extra_polate':
        # returns updated nudge based on first order extrapolation
        # required args: what_type, which_iter, which_stage
        # Arg file info:
        #iterations                  bike        car       cav    drive_transit  ride_hail  ride_hail_pooled    ride_hail_transit  walk    walk_transit
        #intercepts_now            0.000000   0.000000  0.000000       0.000000   0.000000          0.000000           0.000000  0.000000      0.000000
        #benchmark                 0.000000  64.856712  0.000000       5.982906   5.228758          5.027652           5.982906  6.938160      5.982906
        #modeshare_now            23.567151  56.159110  5.132592       1.796407   0.171086          8.383234           0.000000  0.598802      4.191617
        #L1                      -23.567151   8.697602 -5.132592       4.186499   5.057672         -3.355581           5.982906  6.339357      1.791289
        #L1_rank                   1.000000   2.000000  5.000000       7.000000   6.000000          8.000000           4.000000  3.000000      9.000000
        #Positive_Directionality   0.000000   1.000000  0.000000       1.000000   1.000000          0.000000           1.000000  1.000000      1.000000
        #v_dIntercept              0.000000   0.000000  0.000000       0.000000   0.000000          0.000000           0.000000  0.000000      0.000000
        # Name: shared+'/5_60.csv'

        # 2 stage implementation only

        if num_neg_directionality == 1 or num_neg_directionality == 5: 
            last_results = 70 # no of iterations:from 35*2 to 70th -> 18 (88th) -> 18 (106th) -> 9 (115th) -> 9 (124th)
            last_results_stage_1 = 18
        elif num_neg_directionality == 2 or num_neg_directionality == 6:
            last_results = 80 # no of iterations:from 40*2 to 20 -> 20 -> 10 -> 10
            last_results_stage_1 = 20
        elif num_neg_directionality == 3 or num_neg_directionality == 7:
            last_results = 60 # no of iterations:from 30*2 to 16 -> 16 -> 8 -> 8
            last_results_stage_1 = 16
        elif num_neg_directionality == 4:
            last_results = 72 # no of iterations:from 36*2 to 18 -> 18 -> 9 -> 9
            last_results_stage_1 = 18 

        if which_stage == '1_1':

            prior, post = ([] for i in range(2)) 
            for i in range(1,(last_results/2)+1):
                prior.append(glob.glob(shared+'/'+str(i)+'_*.csv'))
            for i in range((last_results/2)+1,last_results+1):
                post.append(glob.glob(shared+'/'+str(i)+'_*.csv'))

            merged = list(itertools.chain(*post))
            best_results_ranked = sorted(merged, key=lambda merged: re.split('_|.csv',merged)[2], reverse=False)

            iter_rank_nums_1_1 = []
            for i in range(len(best_results_ranked)):
                iter_rank_nums_1_1.append(int(re.split('/|_',best_results_ranked[i])[6]))
            iter_rank_index = [x - 1 for x in iter_rank_nums_1_1]

            stage_1_1_results = []
            if len(prior) == len(post):

                for i in range(len(prior)): 
                    prior_df = pd.read_csv(prior[i][0])
                    post_df = pd.read_csv(post[i][0])  
                    updated_v_dIntercept, input_vector = compute_intercept(prior_df, post_df)
                    data = pd.concat([prior_df, post_df], ignore_index=True)
                    updated_v_dIntercept.insert(0, "updated_v_dIntercept")
                    data.loc[12] = updated_v_dIntercept
                    data.loc[13] = input_vector
                    data.at[13, 'iterations'] = 'input_vector'
                    stage_1_1_results.append(data)
                else:
                    raise ValueError('Collected output files in prior and post are not equal!')

            input_vector = [stage_1_1_results[i] for i in iter_rank_index][:last_results_stage_1] # 18 top computed second order optimized input vectors
            # list with two dfs, v_dI, and input_vector, handle carefully!

        elif which_stage == '1_2':

            prior, post = ([] for i in range(2)) 

            for i in range(len(iter_rank_nums_1_1)):
                prior.append(glob.glob(shared+'/'+str(iter_rank_nums_1_1[i])+'_*.csv'))     
            for i in range(last_results+1,last_results+last_results_stage_1+1):
                post.append(glob.glob(shared+'/'+str(i)+'_*.csv'))

            merged = list(itertools.chain(*post))
            best_results_ranked = sorted(merged, key=lambda merged: re.split('_|.csv',merged)[2], reverse=False)

            iter_rank_nums_1_2 = []
            for i in range(len(best_results_ranked)):
                iter_rank_nums_1_2.append(int(re.split('/|_',best_results_ranked[i])[6]))
            iter_rank_index = [x - (last_results + 1) for x in iter_rank_nums_1_2] 

            stage_1_2_results = []
            if len(prior) == len(post):

                for i in range(len(prior)): 
                    prior_df = pd.read_csv(prior[i][0])
                    post_df = pd.read_csv(post[i][0])  
                    updated_v_dIntercept, input_vector = compute_intercept(prior_df, post_df)
                    data = pd.concat([prior_df, post_df], ignore_index=True)
                    updated_v_dIntercept.insert(0, "updated_v_dIntercept")
                    data.loc[12] = updated_v_dIntercept
                    data.loc[13] = input_vector
                    data.at[13, 'iterations'] = 'input_vector'
                    stage_1_2_results.append(data)
                else:
                    raise ValueError('Collected output files in prior and post are not equal!')

            input_vector = [stage_1_2_results[i] for i in iter_rank_index] # 18 top computed second order optimized input vectors
            # list with two dfs, v_dI, and input_vector, handle carefully!

        elif which_stage == '2_1':

            prior, post = ([] for i in range(2)) 
            for i in range(last_results+1,last_results+last_results_stage_1+1):
                prior.append(glob.glob(shared+'/'+str(i)+'_*.csv'))
            for i in range(last_results+last_results_stage_1+1, last_results+(2 * last_results_stage_1)+1):
                post.append(glob.glob(shared+'/'+str(i)+'_*.csv'))

            merged = list(itertools.chain(*post))
            best_results_ranked = sorted(merged, key=lambda merged: re.split('_|.csv',merged)[2], reverse=False)

            iter_rank_nums_2_1 = []
            for i in range(len(best_results_ranked)):
                iter_rank_nums_2_1.append(int(re.split('/|_',best_results_ranked[i])[6]))
            iter_rank_index = [x - (last_results+last_results_stage_1+1) for x in iter_rank_nums_2_1]

            stage_2_1_results = []
            if len(prior) == len(post):

                for i in range(len(prior)): 
                    prior_df = pd.read_csv(prior[i][0])
                    post_df = pd.read_csv(post[i][0])  
                    updated_v_dIntercept, input_vector = compute_intercept(prior_df, post_df)
                    data = pd.concat([prior_df, post_df], ignore_index=True)
                    updated_v_dIntercept.insert(0, "updated_v_dIntercept")
                    data.loc[12] = updated_v_dIntercept
                    data.loc[13] = input_vector
                    data.at[13, 'iterations'] = 'input_vector'
                    stage_2_1_results.append(data)
                else:
                    raise ValueError('Collected output files in prior and post are not equal!')

            input_vector = [stage_2_1_results[i] for i in iter_rank_index][:int(last_results_stage_1/2)] # 9 top computed second order optimized input vectors
            # list with two dfs, v_dI, and input_vector, handle carefully! 

        elif which_stage == '2_2':

            prior, post = ([] for i in range(2)) 
            for i in range(len(iter_rank_nums_2_1)): 
                prior.append(glob.glob(shared+'/'+str(iter_rank_nums_2_1[i])+'_*.csv')) 
            for i in range(last_results+(2*last_results_stage_1)+1, last_results+int((5/2)*last_results_stage_1)+1): 
                post.append(glob.glob(shared+'/'+str(i)+'_*.csv')) 

            merged = list(itertools.chain(*post)) 
            best_results_ranked = sorted(merged, key=lambda merged: re.split('_|.csv',merged)[2], reverse=False)

            iter_rank_nums_2_2 = [] 
            for i in range(len(best_results_ranked)):
                iter_rank_nums_2_2.append(int(re.split('/|_',best_results_ranked[i])[6]))
            iter_rank_index = [x - ( last_results + int((5/2)*last_results_stage_1) + 1) for x in iter_rank_nums_2_2] 

            stage_2_2_results = []
            if len(prior) == len(post):

                for i in range(len(prior)): 
                    prior_df = pd.read_csv(prior[i][0])
                    post_df = pd.read_csv(post[i][0])  
                    updated_v_dIntercept, input_vector = compute_intercept(prior_df, post_df)
                    data = pd.concat([prior_df, post_df], ignore_index=True)
                    updated_v_dIntercept.insert(0, "updated_v_dIntercept")
                    data.loc[12] = updated_v_dIntercept
                    data.loc[13] = input_vector
                    data.at[13, 'iterations'] = 'input_vector'
                    stage_2_2_results.append(data) 
                else:
                    raise ValueError('Collected output files in prior and post are not equal!')

            input_vector = [stage_2_2_results[i] for i in iter_rank_index] # 9 top computed second order optimized input vectors
            # list with two dfs, v_dI, and input_vector, handle carefully!

    elif what_type == 'advanced_nudge':
        # returns advanced updated nudge
        pass

    elif what_type == 'send_2_BOHB':

        results = glob.glob(shared+'/*.csv') 
        best_results_ranked = sorted(results, key=lambda results: re.split('_|.csv',results)[2], reverse=False) 
        df = pd.read_csv(best_results_ranked[0][0])
        input_vector = df.iloc[0] # create a range of this and start BOHB optimization  

    return input_vector





