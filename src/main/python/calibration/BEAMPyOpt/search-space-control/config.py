beam = '/home/ubuntu/kiran_thesis/beam'
# alternative path for local repository
#beam = '/home/berkeleylab/kiran_thesis/beam'

total_rel_nudge_trials = 48 # should always be even and multiple of 4

shared = beam + '/src/main/python/calibration/BEAMPyOpt/storage' 
search_space= beam + '/src/main/python/calibration/BEAMPyOpt/search-space-control'

base_urbansim_config = beam+ '/test/input/sf-light/urbansim-10k.conf'
copy_urbansim_config = beam+ '/test/input/sf-light/urbansim-10k_%d.conf'
copy_urbansim_txt = beam +'/test/input/sf-light/urbansim-10k_%d.txt'

sf_light_ip_dir = beam + '/test/input/sf-light' 

sf_light_dir = beam + '/output/sf-light/*'

output_csv=f'/{shared}/%d_%d.csv'

runme=beam + '/runme.sh'

writecue = beam + '/writecue.txt'
firecue = beam + '/firecue.txt'

nudge_method = 'methodA'
