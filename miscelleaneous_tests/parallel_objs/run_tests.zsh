max_proc=$MAX_ALLOWED_MPI_PROCS

for ((i=2; i<=$max_proc; i++)); do
    echo $i
    cmd="mpirun -n $i ${PYENV_ROOT}/versions/yt_dev/bin/python test_parallel_ob_scaling_v2.py"
    eval $cmd
done
 
