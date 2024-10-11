import yt
import numpy as np
import sys
rs = np.random.RandomState(0)
import timeit
import matplotlib.pyplot as plt

from pathlib import Path

def get_active_branch_name():
    # see https://stackoverflow.com/a/62724213/9357244
    yt_repo = Path(yt.__file__).parent.parent
    head_dir = yt_repo / ".git" / "HEAD"
    with head_dir.open("r") as f: content = f.read().splitlines()

    for line in content:
        if line[0:4] == "ref:":
            return line.partition("refs/heads/")[2]

    raise RuntimeError("could not determine active branch")


yt.set_log_level(500)
def get_2d_ds(n_r, n_theta):

    shp = (n_r,n_theta,1)
    bbox = np.array([[0, 1], [0, np.pi*2],[-.5, .5]])
    data = {
         'density': rs.random(shp)
            }
    ds = yt.load_uniform_grid(data,
                              shp,
                              bbox=bbox,
                              geometry='cylindrical',
                              axis_order=('r', 'theta', 'z'))
    return ds

def plot_ds(ds):
    slc = yt.SlicePlot(ds, 'z', ('stream', 'density'))
    slc.render()

if __name__ == "__main__":

    branch = get_active_branch_name()
    print(f"on branch {branch}")
    results_fname = f"slice_2d_cylindrical_times_{branch}.npy"
    theta_fname = f"slice_2d_cylindrical_times_{branch}_th.npy"
    r_fname = f"slice_2d_cylindrical_times_{branch}_r.npy"

    n_repeats = 10

    # grid resolution settings
    n_r_th_min = 4  # min resolution 2**n_r_th_min for r, theta
    n_r_exp_max = 11  # max r resolution, 2**n_r_exp_max
    n_theta_exp_max = 11  # max theta resolution, 2**n_theta_exp_max

    # resolution arrays
    n_r_exps = np.arange(n_r_th_min, n_r_exp_max)
    n_theta_exps = np.arange(n_r_th_min, n_theta_exp_max)

    if int(sys.argv[1]) == 1:

        tot_times = np.empty((n_r_exps.size, n_theta_exps.size))

        for i_r, n_r_exp in enumerate(n_r_exps):
            for i_th, n_theta_exp in enumerate(n_theta_exps):
                n_r = 2 ** n_r_exp
                n_theta = 2 ** n_theta_exp
                test_id = f"n_r_{n_r}_n_th_{n_theta}"
                print(test_id)
                ds = get_2d_ds(n_r, n_theta)

                t = timeit.Timer(lambda: plot_ds(ds),'gc.enable()')
                tot_times[i_r, i_th] = t.timeit(n_repeats)

        np.save(results_fname, tot_times)
        np.save(r_fname, n_r_exps)
        np.save(theta_fname, n_theta_exps)

    tot_times = np.load(results_fname)
    ave_times = tot_times / n_repeats
    for i_r in range(n_r_exps.size):
        plt.plot(2**n_theta_exps, ave_times[i_r, :], label=f"n_r {2**n_r_exps[i_r]}", marker='.')

    plt.xlabel(r'n_{\theta}')
    plt.ylabel('ave. time [s]')
    plt.legend()
    plt.show()

