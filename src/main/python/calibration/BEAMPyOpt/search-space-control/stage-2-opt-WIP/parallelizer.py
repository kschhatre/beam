
from multiprocessing import Pool,Queue
from time import sleep

def f(x):
    import os 
    print("process id = " , os.getpid())
    return x*x   

# Queue that will hold amount of time to sleep
# for each worker in the initialization
sleeptimes = Queue()
for times in [2,3,0,2]:
    sleeptimes.put(times)

# each worker will do the following init.
# before they are handed any task.
# in our case the 3rd worker won't sleep
# and get all the work.
def slowstart(q):
    import os
    num = q.get()
    print("slowstart: process id = {0} (sleep({1}))".format(os.getpid(),num))
    sleep(num)

if __name__ == '__main__':
    pool = Pool(processes=4,initializer=slowstart,initargs=(sleeptimes,))    # start 4 worker processes
    result  =  pool.map_async(f, (11,))   #Start job 1 
    result1 =  pool.map_async(f, (10,))   #Start job 2
    print("result = ", result.get(timeout=3))
    print("result1 = ", result1.get(timeout=3))
