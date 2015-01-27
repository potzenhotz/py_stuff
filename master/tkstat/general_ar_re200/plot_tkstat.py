
import numpy as np
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl
from matplotlib import rcParams
import prettyplotlib as ppl
 
########################################################################
#Setup plot enviroment 
########################################################################
#rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = ['Times']
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Helvetica']
#rcParams['font.weight'] = 'light'
rcParams['text.usetex'] = True

rcParams['axes.labelsize'] = 58
rcParams['xtick.labelsize'] = 58
rcParams['ytick.labelsize'] = 58
rcParams['legend.fontsize'] = 52
size_title=30
size_axes=58
l_w_1=3.5
l_w_2=4.5

#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
#rc('text', usetex=True)
#font = {'size'   : 18}
#matplotlib.rc('font', **font)
rcParams['axes.linewidth'] = 2.5
rcParams.update({'figure.autolayout':True})



########################################################################
#Load Data
########################################################################

data_name='general_ar_re200_avg3.dat'
avg3_time, avg3_value = np.loadtxt(data_name, unpack=True)

data_name='general_ar_re200_avg5.dat'
avg5_time, avg5_value = np.loadtxt(data_name, unpack=True)

data_name='general_ar_re200_avg6.dat'
avg6_time, avg6_value = np.loadtxt(data_name, unpack=True)

avg3_time=avg3_time*50/60
avg5_time=avg5_time*50/60
avg6_time=avg6_time*50/60


########################################################################
#PLOT
########################################################################


fig, ax = ppl.subplots()
color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors

ax.plot(avg5_time,avg5_value , color=color_set[3], label='Parcel Liquid', linestyle='-',linewidth=l_w_1)
ax.plot(avg6_time,avg6_value , color=color_set[5], label='Droplet Liquid', linestyle='-',linewidth=l_w_1)


plt.xlabel('Time', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
plt.ylabel('Differences', fontsize=size_axes)#,fontdict=font)
plt.xlim(0,30)
plt.ylim([0.02,0.1])
plt.legend(loc=1, frameon=False)

plt.show()

