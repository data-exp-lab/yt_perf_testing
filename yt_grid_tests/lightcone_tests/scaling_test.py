import time
import sys
import yt
from mpi4py import MPI

yt.set_log_level(50)

yt.enable_parallelism()

def write_result(filename, time):
    if MPI.COMM_WORLD.Get_rank() == 0:
        mysize = MPI.COMM_WORLD.Get_size()
        with open(filename, "a") as f:
            s = "{}, {}\n".format(mysize, time)
            f.write(s)

def profile1d(data):
    ds = yt.load(data)
    ad = ds.all_data()
    profile = yt.ProfilePlot(ad, ("gas", "density"), [("gas", "temperature")])

    if yt.is_root():
        profile.save()

def find_max(data):
    ds = yt.load(data)
    ad = ds.all_data()
    with yt.funcs.parallel_profile('find_max_profiling_results'):
        _ = ad.quantities.extrema(("gas", "density"))

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

    
 
    valid_tests = ('profile1d', 'projection', 'find_max')
    if (sys.argv) == 0:
	    test_to_run = 'profile1d'
    else:
        test_to_run = sys.argv[1] 
        if test_to_run not in valid_tests:
            raise ValueError(f"test_to_run not valid, needs to be one of: {valid_tests}")

    if test_to_run == 'profile1d':
        start = time.time()
        profile1d(data)
        end = time.time()
        write_result("fullprof1d-result.csv", end - start)
    elif test_to_run== 'find_max':
        start = time.time()
        find_max(data)
        end = time.time()
        write_result("findmax-result.csv", end - start)
    else: 
        start = time.time()
        projection(data)
        end = time.time()
        write_result("fullproj-result.csv", end - start)


