
import numpy as np
import matplotlib.pyplot as plt
from prettyplotlib import brewer2mpl
from matplotlib import rcParams
#import prettyplotlib as ppl
 
########################################################################
#Setup plot enviroment 
########################################################################
#rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = ['New Centrury Schoolbook']
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Helvetica']
#rcParams['font.weight'] = 'light'
rcParams['text.usetex'] = True

rcParams['axes.labelsize'] = 48
rcParams['xtick.labelsize'] = 48
rcParams['ytick.labelsize'] = 48
rcParams['legend.fontsize'] = 38
size_title=30
size_axes=58
l_w_1=3.5
l_w_2=25 #for markers

#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
#rc('text', usetex=True)
#font = {'size'   : 18}
#matplotlib.rc('font', **font)
rcParams['axes.linewidth'] = 2.5
rcParams['axes.linewidth'] = 3.0
rcParams.update({'figure.autolayout':True})

########################################################################
#Some calculations for VERDI case for real time
########################################################################
#VERDI 
t_lambda=15
t_F=60
t_gravity=9.81
t_rho_c=1.164
t_cp=1022
t_T_c=268.15
B=t_F*t_gravity/(t_rho_c*t_cp*t_T_c)
t_real=((t_lambda**2)/B)**(0.3333333)
u_0=(B*t_lambda)**(0.333333)
print 'verdi t_o is:' ,t_real
print 'verdi B_o is:' ,B
print 'verdi U_o is:' ,u_0



########################################################################
#Load data
########################################################################
nbins=1000
tend=18900
tstart=10100
tstep=100

ntimes = (tend - tstart) / tstep + 1
print "NTIMES IS:", ntimes

interval = np.zeros((nbins,ntimes))
residence_lambda = np.zeros((nbins,ntimes))
residence_base = np.zeros((nbins,ntimes))
i=0

print 'ntimes',ntimes
data_path = 'ar_re200_strat_residence/'

for t in np.arange(ntimes):
  l_t=t+(tstart/tstep)
  step=l_t*tstep
  data_name=data_path + 'residence_pdf.' + np.str(step)   #name of file
  
  interval[:,i],residence_lambda[:,i],residence_base[:,i] = np.loadtxt(data_name, unpack=True) # read file into data
  i=i+1

#remove the the first interval point
residence_lambda[0,:] = 0
residence_base[0,:] = 0


########################################################################
#Load and calculate real time
########################################################################
time_data=np.zeros(300) #300 is just a buffer
data_name=data_path + 'times.log' #name of times file
print data_name

#Load data
time_data = np.loadtxt(data_name, unpack=True) 

#Calculate real time
time_real_data=np.zeros(len(time_data))
for i in np.arange(len(time_data)): 
  time_real_data[i]=round(time_data[i]*t_real/60,2)

for k in np.arange(len(time_data)): 
  time_real_data[k]=round(time_real_data[k],0)

print time_real_data.shape

########################################################################
#Scale data
########################################################################
scale_residence_lambda = np.zeros((nbins,ntimes))
scale_residence_base = np.zeros((nbins,ntimes))
total_residence_lambda = np.zeros((ntimes))
total_residence_base = np.zeros((ntimes))

#Calculate the total amount of particles to total_*
#Take a running sum and divide by total number - scaled(i)=sum(pt(0:i)/total
#Then reverse - 1-scaled
for i in range(0,ntimes): 
  total_residence_lambda[i] = np.sum(residence_lambda[:,i])
  total_residence_base[i] = np.sum(residence_base[:,i])
  for j in range(0,nbins):
    scale_residence_lambda[j,i] = np.sum(residence_lambda[0:j,i]) / total_residence_lambda[i]
    scale_residence_base[j,i] = np.sum(residence_base[0:j,i]) / total_residence_base[i]
scale_residence_lambda = 1 - scale_residence_lambda
scale_residence_base = 1 - scale_residence_base

integral_time=9.1 #calculate with u* and L 
time_steps=interval[1,1]-interval[0,1]  

########################################################################
#Calculate derivative data
########################################################################
diff_residence_lambda = np.zeros((nbins-1,ntimes))

for i in range(0,ntimes): 
  for j in range(0,nbins-1): 
    diff_residence_lambda[j,i] = np.log(scale_residence_lambda[j,i]) - np.log(scale_residence_lambda[j+1,i])

########################################################################
#Plot data
########################################################################
fig, ax = plt.subplots()
#fig, ax = ppl.subplots() #not sure anymore why ppl should be better
color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors


t_inter=tstart/tstep
print 't_intermediate',t_inter

#Scaled data to plot
list = [22, 33, 44, 55, 66, 77, 88]
l_c = [2, 1, 0, 4, 5, 6, 7]
j=0
for i  in list:
  label_name='t=' + str(int(time_real_data[i+t_inter-1])) + ' min'
  ax.plot(interval[:,44]/integral_time, scale_residence_lambda[:,i], color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2, label='Simulation ' + label_name)
  j=j+1

#PLOT PROPERTIES
plt.legend(loc=1,numpoints=1, frameon=False)
ax.set_yscale('log')

ax.set_xlabel(r'$t/t^*$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
ax.set_ylabel(r'Percentile', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
plt.xlim(0,5)
plt.ylim(10**-5,1)

#Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

########################################################################
#Plot derivative
########################################################################
fig, ax2 = plt.subplots()

#Deriative data to plot
list = [22, 33, 44, 55, 66, 77, 88]
l_c = [2, 1, 0, 4, 5, 6, 7]
j=0
for i  in list:
  label_name='t=' + str(int(time_real_data[i+t_inter-1])) + ' min'
  ax2.plot(interval[0:nbins-1,44]/integral_time, diff_residence_lambda[:,i]/(time_steps/integral_time),color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2)
  j=j+1


plt.xlim(0,45/integral_time)
plt.ylim(1,0.055/(0.1/integral_time))
ax2.set_ylabel(r'$d(log(p))/dt$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
ax2.set_xlabel(r'$t/t^*$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt

#Hide the right and top spines
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax2.yaxis.set_ticks_position('left')
ax2.xaxis.set_ticks_position('bottom')

########################################################################
#Show all plots
########################################################################
plt.show()

