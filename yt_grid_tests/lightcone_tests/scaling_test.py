import time
import sys
import yt
from mpi4py import MPI

yt.set_log_level(50)

yt.enable_parallelism()

def write_result(filename, time, n_reps=None):
    if MPI.COMM_WORLD.Get_rank() == 0:
        mysize = MPI.COMM_WORLD.Get_size()
        with open(filename, "a") as f:
            if n_reps is not None:
                s = "{}, {}, {}\n".format(mysize, time, n_reps)
            else:
                s = "{}, {}\n".format(mysize, time)
            f.write(s)

def profile1d(data):
    ds = yt.load(data)
    ad = ds.all_data()
    profile = yt.ProfilePlot(ad, ("gas", "density"), [("gas", "temperature")])

    if yt.is_root():
        profile.save()

def find_max(data, with_profiling=True, field=("gas", "density")):
    ds = yt.load(data)
    ad = ds.all_data()
    if with_profiling:
        with yt.funcs.parallel_profile('find_max_profiling_results'):
            _ = ad.quantities.extrema(field)
    else:
        _ = ad.quantities.extrema(field)

def find_max_repeat(data, field=("gas", "density"), nreps=5):
    ds = yt.load(data)
    _ = ds.index  # dont profile the index
    #ds.index.set_grid_cache_mask(False)  # turn off all cacheing of masks
    with yt.funcs.parallel_profile(f"find_max_profiling_results_n_{nreps}"):
        for i in range(nreps):
            print(f"loop {i}")
            ad = ds.all_data()
            _ = ad.quantities.extrema(field)

def index_grid_loop(data, nreps=2):
    ds = yt.load(data)
    for i in range(nreps):
        for g in ds.index.grids:
            g.get_global_startindex()

def indexing_init(data, fprefix: str):
    with yt.funcs.parallel_profile(f"{fprefix}_indexing_init"):
        ds = yt.load(data)
        _ = ds.index
   

def projection(data):
    ds = yt.load(data)
    p = yt.ProjectionPlot(ds, "z", ("gas", "density"), width=(1.0, 'unitary'))

    if yt.is_root():
        p.save()

if __name__ == "__main__":

    # mpirun -n $PPR --bind-to hwthread --map-by ppr:1:core --report-bindings python3.8 test.py
    # mpirun -n $PPR --bind-to hwthread --map-by ppr:1:core --report-bindings python scaling_test.py
    # mpirun -n $PPR --map-by ppr:1:core python scaling_test.py

    # Santa Fe Light Code at redshift 0 (RD0036), available at 
    # https://library.ucsd.edu/dc/object/bb2049101m
    data = "LightCone/RD0036/RD0036" # TODO : dataset

    # arg 1 : test name
    # arg 2 : with_profiling bool
    # arg 3 : nreps int

    valid_tests = ('profile1d', 'projection', 'find_max', 'find_max_repeat', 'index_grid_loop')
    if (sys.argv) == 0:
        test_to_run = 'profile1d'
    else:
        test_to_run = sys.argv[1] 
        if test_to_run not in valid_tests:
            raise ValueError(f"test_to_run not valid, needs to be one of: {valid_tests}")

    with_profiling = bool(sys.argv[2])

    if test_to_run == 'profile1d':
        start = time.time()
        profile1d(data)
        end = time.time()
        write_result("fullprof1d-result.csv", end - start)
    elif test_to_run== 'find_max':
        start = time.time()
        find_max(data, with_profiling=with_profiling, field=("index", "ones"))
        end = time.time()
        write_result("findmax-result.csv", end - start)
    elif test_to_run == 'find_max_repeat':
        start = time.time()
        nreps = int(sys.argv[3])
        find_max_repeat(data, field=("index", "ones"), nreps=nreps)
        end = time.time()
        write_result("findmax-repeat.csv", end-start, nreps)
    elif test_to_run == 'index_grid_loop':
        start = time.time()
        nreps = int(sys.argv[3])
        index_grid_loop(data, nreps=nreps)
        end = time.time()
        write_result("index-grid-loop.csv", end - start, nreps)
    else: 
        start = time.time()
        projection(data)
        end = time.time()
        write_result("fullproj-result.csv", end - start)


