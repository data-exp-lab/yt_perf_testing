import matplotlib.pyplot as plt
import numpy as np


figs, axs = plt.subplots(nrows=2, ncols=3, figsize=(12,10))

results = {}
branch_names = ('main', 'release_gil_in_pixelize_cylinder')
for ibranch, branch in enumerate(branch_names):
    results_fname = f"slice_2d_cylindrical_times_{branch}.npy"
    theta_fname = f"slice_2d_cylindrical_times_{branch}_th.npy"
    r_fname = f"slice_2d_cylindrical_times_{branch}_r.npy"

    n_repeats = 10
    r = (2 ** np.load(r_fname)).astype(int)
    theta = (2 ** np.load(theta_fname)).astype(int)
    tot_times = np.load(results_fname)
    ave_times = tot_times / n_repeats

    for i_r in range(r.size):
        axs[0, ibranch].plot(theta, ave_times[i_r, :], label=f"n_r {r[i_r]}", marker='.')
        axs[0, ibranch].set_xlabel('n_{theta}')
        axs[0, ibranch].set_title(branch)

    axs[0, 0].set_ylabel('ave. time [s]')

    for i_th in range(theta.size):
        axs[1, ibranch].plot(r, ave_times[:, i_th], label=f"n_th {theta[i_th]}", marker='.')
        axs[1, ibranch].set_xlabel('n_{r}')
        axs[1, ibranch].set_title(branch)

    axs[1, 0].set_ylabel('ave. time [s]')

    results[branch] = ave_times


speedup = 100*(results[branch_names[0]] - results[branch_names[1]]) / results[branch_names[0]]

results['speedup'] = speedup

for i_r in range(r.size):
    axs[0, 2].plot(theta, speedup[i_r, :], label=f"n_r {r[i_r]}", marker='.')
    axs[0, 2].set_xlabel('n_{theta}')

axs[0, 2].set_ylabel('speedup %')

for i_th in range(theta.size):
    axs[1, 2].plot(r, speedup[:, i_th], label=f"n_th {theta[i_th]}", marker='.')
    axs[1, 2].set_xlabel('n_{r}')

axs[1, 2].set_ylabel('speedup %')

f2, axs = plt.subplots(nrows=1, ncols=3,figsize=(10,6))
clims = [[0.25, 0.75], [.25, .75], [25, 40]]
cmaps = ['viridis', 'viridis', 'summer_r']
for iax, (branch, result) in enumerate(results.items()):
    im = axs[iax].imshow(result, origin='lower')
    im.set_clim(*clims[iax])
    im.set_cmap(cmaps[iax])
    axs[iax].set_yticks(np.arange(len(r)), r, fontsize=10,)
    axs[iax].set_ylabel('N r')
    axs[iax].set_xlabel('N theta')
    axs[iax].set_title(branch)
    axs[iax].set_xticks(np.arange(len(theta)), theta, fontsize=10, rotation=-45)
    plt.colorbar(im, ax=axs[iax],fraction=0.046, pad=0.04)

plt.tight_layout()
ave_speedup = speedup.mean()
print(f"\n\n********************\n average speedup is : {ave_speedup}")
f2.savefig("results.png")

