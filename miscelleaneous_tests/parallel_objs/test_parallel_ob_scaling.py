import yt 
from yt.utilities.parallel_tools import parallel_analysis_interface as pai 
import time 
import os


if __name__ == "__main__":
    yt.enable_parallelism() 

    t1 = time.time()
    calc_range = list(range(0,1000))
    wait_time = 0.01

    total_serial_time_ideal = wait_time * len(calc_range)
    storage = {}

    for sto, c in pai.parallel_objects(calc_range, storage=storage):
        time.sleep(0.01)
        sto.result = 1


    t2 = time.time()
    dt = t2 - t1 

    my_communicator = pai.communication_system.communicators[-1]
    my_size = my_communicator.size
    my_rank = my_communicator.rank
    ideal_mpi_time = total_serial_time_ideal / my_size
    if my_rank == 0:
        print((my_size, dt))
        fname = 'parallel_ob_times.csv'
        if os.path.isfile(fname) is False:
            with open(fname, 'w') as fh:
                fh.write("n_procs,dt,total_serial_time,ideal_distrib_time\n")

        with open(fname, 'a') as fh:
            fh.write(f"{my_size},{dt},{total_serial_time_ideal},{ideal_mpi_time}\n")


