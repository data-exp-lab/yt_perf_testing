import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv('parallel_ob_times.csv')

df = df.groupby('n_procs').mean(['n_procs', 'dt', 'total_serial_time', 'ideal_distrib_time'])
df = df.sort_values('n_procs')
df = df.reset_index()
print(df)

fig, axs = plt.subplots(nrows=1, ncols=3, figsize=(8,2))

axs[0].plot(df.n_procs, df['dt'], marker='.',label='actual')
axs[0].plot(df.n_procs, df['ideal_distrib_time'], marker='.', label='ideal')
axs[0].legend()
axs[0].set_xlabel('N processors')
axs[0].set_ylabel('elapsed time [s]')

axs[1].plot(df.n_procs, df['dt'] / df['ideal_distrib_time'] , marker='.',label='actual')
axs[1].set_xlabel('N processors')
axs[1].set_ylabel('actual / ideal')

axs[2].plot(df.n_procs, (df['dt'] - df['ideal_distrib_time']) / df['ideal_distrib_time'] , marker='.',label='actual')
axs[2].set_xlabel('N processors')
axs[2].set_ylabel('(actual - ideal) / ideal')

fig.set_tight_layout('tight')
fig.savefig('result.png')

