
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

rcParams['axes.labelsize'] = 48
rcParams['xtick.labelsize'] = 48
rcParams['ytick.labelsize'] = 48
rcParams['legend.fontsize'] = 35
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
rcParams['axes.linewidth'] = 3.0
rcParams.update({'figure.autolayout':True})



########################################################################
#Load Data
########################################################################

#data_name='general_ar_re200_avg3.dat'
#data_name='general_ar_re200_avg3_t2000.dat'
#avg3_time, avg3_value = np.loadtxt(data_name, unpack=True)
#
#data_name='general_ar_re200_avg5.dat'
#avg5_time, avg5_value = np.loadtxt(data_name, unpack=True)
#
#data_name='general_ar_re200_avg6.dat'
#data_name='general_ar_re200_avg6_t2000.dat'
#avg6_time, avg6_value = np.loadtxt(data_name, unpack=True)
#
#avg3_time=avg3_time*50/60
#avg5_time=avg5_time*50/60
#avg6_time=avg6_time*50/60

#
#LOAD DIFFERENT SET
#
data_name='general_ar_re200_avg3_t900.dat'
avg3_y, avg3_value = np.loadtxt(data_name, unpack=True)

data_name='general_ar_re200_avg6_t900.dat'
avg6_y, avg6_value = np.loadtxt(data_name, unpack=True)

data_name='general_ar_re800_avg3_t2900.dat'
re800_avg3_y, re800_avg3_value = np.loadtxt(data_name, unpack=True)

data_name='general_ar_re800_avg6_t2900.dat'
re800_avg6_y, re800_avg6_value = np.loadtxt(data_name, unpack=True)


#modify y-axes so that cloud top is zero
avg3_y_mod = (avg3_y - 67.40)*15
avg6_y_mod = (avg6_y - 67.40)*15
re800_avg3_y_mod = (re800_avg3_y - 29.16)*15
re800_avg6_y_mod = (re800_avg6_y - 29.16)*15
########################################################################
#PLOT
########################################################################


fig, ax = ppl.subplots()
color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors

#ax.plot(avg5_time,avg5_value , color=color_set[3], label='Parcel Liquid', linestyle='-',linewidth=l_w_1)
#ax.plot(avg6_time,avg6_value , color=color_set[5], label='Droplet Liquid', linestyle='-',linewidth=l_w_1)
#plt.xlabel('Time', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
#plt.ylabel('Differences', fontsize=size_axes)#,fontdict=font)
#plt.xlim(0,30)
#plt.ylim([0.02,0.1])
#plt.legend(loc=1, frameon=False)

#ax.plot(avg3_value, avg3_y, color=color_set[3], label='Liquid', linestyle='-',linewidth=l_w_1)
#ax.plot(avg6_value, avg6_y, color=color_set[5], label='Droplet Liquid', linestyle='-',linewidth=l_w_1)

ax.plot(re800_avg3_value, re800_avg3_y_mod, color=color_set[1], label='Eulerian Re800', linestyle='-',linewidth=l_w_1)
ax.plot(re800_avg6_value, re800_avg6_y_mod, color=color_set[3], label='Lagrange Re800', linestyle='-',linewidth=l_w_1)

ax.plot(avg3_value, avg3_y_mod, color=color_set[1], label='Eulerian Re200', linestyle='--',linewidth=l_w_1)
ax.plot(avg6_value, avg6_y_mod, color=color_set[3], label='Lagrange Re200', linestyle='--',linewidth=l_w_1)


plt.xlabel('Liquid', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
plt.ylabel('Height from cloud top (m)', fontsize=size_axes)#,fontdict=font)
plt.xlim(0.0,1.3)
#plt.ylim(40,70)
plt.ylim(-150,20)
plt.legend(loc=3, frameon=False)


#Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


plt.show()

