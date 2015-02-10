
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
rcParams['legend.fontsize'] = 38
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
#Load data
########################################################################
nbins=1000
tend=600
tstart=100
tstep=100

ntimes = (tend - tstart) / tstep + 1

interval= np.zeros((nbins,ntimes))
residence_lambda= np.zeros((nbins,ntimes))
residence_base= np.zeros((nbins,ntimes))
i=0

print 'ntimes',ntimes
data_path = 'test_data_2D/'

for t in np.arange(ntimes):
  l_t=t+(tstart/tstep)
  step=l_t*tstep
  data_name=data_path + 'residence_pdf.' + np.str(step)   #name of file
  
  interval[:,i],residence_lambda[:,i],residence_base[:,i] = np.loadtxt(data_name, unpack=True) # read file into data
  i=i+1




########################################################################
#Plot data
########################################################################

fig, ax = ppl.subplots()
color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors

#ax.plot(interval, residence_lambda, color=color_set[1], label='Eulerian Re200', linestyle='-',linewidth=l_w_1)
ax.plot(interval[:,5], np.log(residence_lambda[:,5]),marker='.',linestyle='None',markersize=19,linewidth=l_w_1)
#ax.bar(interval[:,0], residence_lambda[:,0], color='#3F5D7D')

#plt.xlabel('Liquid', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
#plt.ylabel('Height from cloud top (m)', fontsize=size_axes)#,fontdict=font)
#plt.xlim(-0.5,20)
#plt.ylim(0,30000)
#plt.legend(loc=1, frameon=False)


#Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')


plt.show()

