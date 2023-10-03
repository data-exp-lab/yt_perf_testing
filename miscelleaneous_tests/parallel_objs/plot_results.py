import pandas as pd 
import matplotlib.pyplot as plt 

df = pd.read_csv('parallel_ob_times.csv')

df = df.groupby('n_procs').mean(['n_procs', 'dt', 'total_serial_time', 'ideal_distrib_time'])
df = df.sort_values('n_procs')
df = df.reset_index()
print(df)

plt.plot(df.n_procs, df['dt'], marker='.',label='actual')
plt.plot(df.n_procs, df['ideal_distrib_time'], marker='.', label='ideal')
plt.legend()
plt.xlabel('N processors')
plt.ylabel('elapsed time [s]')
plt.gcf().savefig('result.png')
plt.show()
