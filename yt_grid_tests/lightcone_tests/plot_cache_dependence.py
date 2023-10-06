import pandas as pd 

import matplotlib.pyplot as plt 

df = pd.read_csv('./nocache/findmax-repeat.csv', header=None)
df = df.sort_values(0)
dfw = pd.read_csv('./withcache/findmax-repeat.csv', header=None)
dfw = dfw.sort_values(0)

plt.plot(df[0], df[1], marker='.', linestyle='none', label='no mask cache')
plt.plot(dfw[0], dfw[1], marker='.', linestyle='none', label='with mask cache')
plt.xlabel('np')
plt.ylabel('time [s]')
plt.title('findmax on repeat (5), chris macbook')
plt.savefig('findmax_repeat_results.png')

plt.loglog(df[0], df[1], marker='.', linestyle='none', label='no mask cache')
plt.loglog(dfw[0], dfw[1], marker='.', linestyle='none', label='with mask cache')
plt.xlabel('np')
plt.ylabel('time [s]')
plt.title('findmax on repeat (5), chris macbook')
plt.legend()
plt.savefig('findmax_repeat_results_logged.png')
