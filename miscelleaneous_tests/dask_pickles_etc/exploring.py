import yt
from dask import delayed, compute
from dask.distributed import Client
import sys
import time
import pickle


def indexed_operation(ds):


    return ds * 2


def separate_loads(fname):
    ds = yt.load(fname)
    _ = ds.index
    return ds.all_data()['gas', 'density'].min()

def pre_loaded(ds):
    return ds.all_data()['gas', 'density'].min()

yt.set_log_level(50)

"""
important note on dask state: 

When you start the dask distributed cluster, new subprocesses are created. 
Unless you use fork (&), this will involve reimporting the current script, with 
a name other than __main__ . This is how the if block prevents each worker process 
from also trying to create clusters-within-clusters. So, by placing your import 
within the if block, you stop the workers from executing them.

https://stackoverflow.com/questions/75837897/dask-worker-has-different-imports-than-main-thread

so, need to:

1. set 'store_parameter_files' config to true 

and before __name__ need to ensure the object registries are updated
"""
# yt.config.ytcfg.set('yt', 'store_parameter_files', True)
# try:
#     _ = yt.load("lwkrjewlrkeja")
# except FileNotFoundError:
#     pass

if __name__ == "__main__":


    n_workers = int(sys.argv[1])
    processes = bool(sys.argv[2])
    tpw = int(sys.argv[3])

    start_time = time.time()
    print((n_workers, processes, tpw))

    c = Client(n_workers=n_workers, threads_per_worker=tpw)

    tasks = []

    # case 1: load on each process (works)
    # fname = 'IsolatedGalaxy/galaxy0030/galaxy0030'
    # for _ in range(10):
    #     tasks.append(delayed(separate_loads)(fname))

    # case 2: pre-load, pass ds
    fname = 'IsolatedGalaxy/galaxy0030/galaxy0030'
    ds = yt.load(fname)
    for _ in range(10):
        tasks.append(delayed(pre_loaded)(ds))

    results = compute(*tasks)
    print(time.time() - start_time)
    c.close()