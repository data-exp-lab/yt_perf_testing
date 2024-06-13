import yt
from dask import delayed, compute
from dask.distributed import Client
import sys
import time

def find_min_val(ds):
    # just something to take some time
    return ds.all_data()['gas', 'density'].min()

yt.set_log_level(50)

# The store_parameter_files config option controls how datasets
# are pickled. If True, an on-disk csv file is created. If False,
# an in-memory store is used, which can introduce some
# tricky state-dependence. Make sure it is False here:
assert not yt.config.ytcfg.get('yt','store_parameter_files')

# Putting Load HERE works
# fname = 'IsolatedGalaxy/galaxy0030/galaxy0030'
# ds = yt.load(fname)

if __name__ == "__main__":

    n_workers = int(sys.argv[1])
    tpw = int(sys.argv[2])

    start_time = time.time()
    print((n_workers, tpw))

    c = Client(n_workers=n_workers, threads_per_worker=tpw)

    tasks = []

    # Putting Load HERE fails with
    #   File "/home/chavlin/miniconda3/envs/yt_py39/lib/python3.9/site-packages/distributed/protocol/pickle.py", line 96, in loads
    #     return pickle.loads(x)
    #   File "/home/chavlin/src/yt_general/yt/yt/data_objects/static_output.py", line 2053, in _reconstruct_ds
    #     ds = datasets.get_ds_hash(*args)
    #   File "/home/chavlin/src/yt_general/yt/yt/utilities/parameter_file_storage.py", line 91, in get_ds_hash
    #     return self._convert_ds(self._records[hash])
    # KeyError: 'e34a252e426f6cc81be22b03b77786ea'

    fname = 'IsolatedGalaxy/galaxy0030/galaxy0030'
    ds = yt.load(fname)

    for _ in range(10):
        tasks.append(delayed(find_min_val)(ds))

    results = compute(*tasks)
    print(time.time() - start_time)
    c.close()