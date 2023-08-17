import yt

yt.enable_parallelism()

ds = yt.load("enzo_tiny_cosmology/DD0005/DD0005")



print("go fetch")
with yt.funcs.parallel_profile('profiling_results'):
    v, c = ds.find_max(("gas", "density")) 
print("done")
print(v,c)
