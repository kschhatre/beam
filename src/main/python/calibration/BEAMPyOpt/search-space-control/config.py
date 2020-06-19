beam = '/home/ubuntu/kiran_thesis/beam'

shared = beam + '/src/main/python/calibration/BEAMPyOpt/storage' 
search_space= beam + 'src/main/python/calibration/BEAMPyOpt/search-space-control'

base_urbansim_config = beam+ '/test/input/sf-light/urbansim-10k.conf'
copy_urbansim_config = beam+ '/test/input/sf-light/urbansim-10k_%d.conf'
copy_urbansim_txt = beam +'/test/input/sf-light/urbansim-10k_%d.txt'

sf_light_dir = beam + 'output/sf-light/*'

output_csv=f'${shared}/%d_%d.csv'

runme=beam + '/runme.sh'
