import yt
from yt.config import ytcfg
yt.enable_parallelism()

ds = yt.load("enzo_tiny_cosmology/DD0005/DD0005")

my_proc = ytcfg.get("yt", "internals", "topcomm_parallel_rank")

count = 0
for i in yt.parallel_objects(ds.index.grids):
    count +=1
print("Not grids", my_proc, count)

dd = ds.all_data()
count = 0
for chunk in yt.parallel_objects(dd.chunks([], "io")):
    count += len(chunk._current_chunk.objs)
print("Grids", my_proc, count)

with yt.funcs.parallel_profile('profiling_results'):
    v, c = ds.find_max(("gas", "density")) 


print(v,c)
