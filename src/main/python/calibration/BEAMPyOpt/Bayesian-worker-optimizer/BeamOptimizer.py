
import shutil, os, glob, sys, datetime
sys.path.insert(1, '/home/ubuntu/ksc_test/HpBandSter/hpbandster')
import core.nameserver as hpns
import core.result as hpres
from optimizers import BOHB as BOHB
from BeamWorker import BeamWorker

NS = hpns.NameServer(run_id='BEAM', host='127.0.0.1', port=None)
NS.start()

# User defined variables
Repo='/home/ubuntu/ksc_test/beam/test/input/'
no_of_workers = 4
selection = 'urbansim-10k' 
#selection is 'beamville' or 'urbansim-1k' or 'urbansim-10k' -> to be update in configselector.py too

with open('/home/ubuntu/ksc_test/HpBandSter/hpbandster/core/timer.txt', 'w') as txtfile:
    txtfile.write(str(datetime.datetime.now())) 

if selection == 'beamville':
    Repo = Repo+'beamville/'
    conf = 'beam'
else:
    Repo = Repo+'sf-light/'
    conf = selection
    
def create_conf_copies(no_of_workers):
    for num in range(no_of_workers):
        shutil.copy(Repo+conf+'.conf',Repo+conf+'_'+str(num+1)+'.conf')
        
create_conf_copies(no_of_workers)

workers=[]
for i in range(no_of_workers):   
    w = BeamWorker(nameserver='127.0.0.1', run_id='BEAM', id=i)
    w.run(background=True)
    workers.append(w)

result_logger = hpres.json_result_logger(directory='/home/ubuntu/ksc_test/beam-calibration-dev/TUNE_integrate/TUNE_test/worker_n_optimizer', overwrite=True)
#previous_run = hpres.logged_results_to_HBS_result('/home/ubuntu/ksc_test/beam-calibration-dev/TUNE_integrate/TUNE_test/worker_n_optimizer')
bohb = BOHB(configspace=w.get_configspace(),run_id='BEAM',min_budget=2, max_budget=12, result_logger=result_logger)     
res = bohb.run(n_iterations=16,min_n_workers=no_of_workers)


bohb.shutdown(shutdown_workers=True)
NS.shutdown()

# Delete conf copies
for filename in glob.glob('/home/ubuntu/ksc_test/beam/test/input/beamville/beam_*.conf'): 
    os.remove(filename) 






