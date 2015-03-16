#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
from matplotlib import rcParams


########################################################################
#Setup plot enviroment 
########################################################################
#rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = ['Times']
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Helvetica']
#rcParams['font.weight'] = 'light'
rcParams['text.usetex'] = True

rcParams['axes.labelsize'] = 48
rcParams['xtick.labelsize'] = 48
rcParams['ytick.labelsize'] = 48
rcParams['legend.fontsize'] = 35
size_title=30
size_axes=48
l_w_1=6.5
l_w_2=6.5
m_s=38

rcParams['axes.linewidth'] = 2.5
rcParams.update({'figure.autolayout':True})


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Read raw data 
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def read_data(data_path, tstart, tend, tstep, nbins):
  
  ntimes = (tend - tstart) / tstep + 1
  interval= np.zeros((nbins,ntimes))
  eulerian= np.zeros((nbins,ntimes))
  l_diff= np.zeros((nbins,ntimes))
  l_nodiff= np.zeros((nbins,ntimes))
  i=0
  print 'ntimes',ntimes
  for t in np.arange(ntimes):
    l_t=t+(tstart/tstep)
    step=l_t*tstep
    data_name=data_path + 'particle_pdf.' + np.str(step)   #name of file
    
    interval[:,i],eulerian[:,i],l_diff[:,i], l_nodiff[:,i] = np.loadtxt(data_name, unpack=True) # read file into data
    i=i+1
  return (interval, eulerian, l_diff, l_nodiff)

#TIME
def read_timedata(data_path, time_data):
  data_name=data_path + 'times.log' #name of file
  print data_name
  time_data = np.loadtxt(data_name, unpack=True) # read file into data
  return (time_data)


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Function to compare different Re numbers
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def plot_data_compare(interval1,data1_1, data1_2, data1_3, 
                      interval2, data2_1, data2_2, data2_3,
                      interval3, data3_1, data3_2, data3_3,
                      names1, names2, names3):

  #COLORS FOR PLOTTING 
  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
  color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
 
  ########################################################################
  #Scale data
  ########################################################################
  data2_1=data2_1*30/18*1.3
  data2_2=data2_2*30/18*1.3
  data2_3=data2_3*30/18*1.3

  data3_1=data3_1*50/18*1.4 
  data3_2=data3_2*50/18*1.4
  data3_3=data3_3*50/18*1.4

  ########################################################################
  #Plot data
  ########################################################################
  ax.plot(interval1,data1_3, color=color_set[1],linewidth=l_w_1, label=names1[3])
  ax.plot(interval2,data2_3, color=color_set[3],linewidth=l_w_1, label=names2[3])
  ax.plot(interval3,data3_3, color=color_set[5],linewidth=l_w_1, label=names3[3])


  ########################################################################
  #Plot properties
  ########################################################################
  #GRID LINES
  #axes = plt.gca()
  #axes.grid(True)

  ax.set_yscale('symlog') #use 'symlog'= for symmetrical log  or 'log' for only positive values
  plt.xlabel(r'$M/M_r$', fontsize=size_axes) #the argument r allows for latex code
  plt.ylabel('Relative amount of droplets', fontsize=size_axes)

  plt.xlim(0.1,2.2)
  plt.ylim([10,10**8])
  plt.legend(loc=1, frameon=False) # set legend and the location 
  

  #Hide the right and top spines
  ax.spines['right'].set_visible(False)
  ax.spines['top'].set_visible(False)
  #Only show ticks on the left and bottom spines
  ax.yaxis.set_ticks_position('left')
  ax.xaxis.set_ticks_position('bottom')

  plt.show()



#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#Several time-steps and the flight data
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def several_times_and_flight(all_interval3, all_data3_3,
                  t_real, time_data,  
                  interval_flight, data_flight,interval_flight_2, 
                  data_flight_2, flight_err_2, data3_3, interval3):

  #setup colors and plot enviroment
  fig, ax1  = plt.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('YlGnBu', 'sequential', 9).mpl_colors
  color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
  color_set_4 = brewer2mpl.get_map('Purples', 'sequential', 9).mpl_colors
  

  shape= np.shape(all_interval3) 
  time_length=shape[1]

  #sum of all particles
  sum_all_data3_3 = np.zeros(time_length) 
  for i in np.arange(time_length):
    sum_all_data3_3[i]=np.sum(all_data3_3[:,i])
    sum_all_data3_3[i]=sum_all_data3_3[i]-all_data3_3[0,i]
  ########################################################################
  #Plot the flight data
  ########################################################################
  data_flight=data_flight*0.9*10**7   #change amount of particles accoding to simulation
  data_flight_2=data_flight_2*0.9*10**7
  flight_err_2 = data_flight_2[:] * flight_err_2[:]  #error data seems wrong

  #ax1.plot(interval_flight,data_flight,zorder=10, color=color_set_4[4],marker='.',linestyle='None',markersize=m_s+9 , label='Flight data')
  ax1.plot(interval_flight_2,data_flight_2,zorder=10, color=color_set_4[7],marker='.',linestyle='None',markersize=m_s+9 , label='Flight data')

  #if u need errorbars use this command
  #ax1.errorbar(interval_flight_2,data_flight_2,yerr=flight_err_2,zorder=10, color=color_set[8],marker='.',linestyle='None',markersize=m_s+9 , label='Flight data')

  ########################################################################
  #Plot the data+fit
  ########################################################################
  time_real_data=np.zeros(len(time_data))
  for i in np.arange(len(time_data)): 
    time_real_data[i]=round(time_data[i]*t_real/60,2)
    print 'real time',i,time_real_data[i]



  t_0 = 0 # timestep was before 55
  G = 0.09/20 #cooling rate from tkstat
  plot_t = [59,82,107,133,159,186] #"timesteps" we want to plot
  #plot_t = [186] # only last step 
  t_sim=time_data[plot_t[:]] #simulation time-step from time_data
  l_c = [0,1,2,3,4,5] # for colors of brewer color scale
  #l_c = [5] # red color
  j=0 #counter for colors
  for k in plot_t:
    time_real_data[k]=round(time_real_data[k],0)
    label_name='t=' + str(int(time_real_data[k])) + ' min'
    if (k < t_0 ):
      scale=0
    else:
      scale = G*(t_sim[j]-t_0)
    ax1.plot(all_interval3[:,k]-scale,all_data3_3[:,k],color=color_set[l_c[j]],linewidth=l_w_1, label=label_name)
    j=j+1 #used for color 

 
  ########################################################################
  #PLOT PROPERTIES
  ########################################################################

  #GRID LINES
  #axes = plt.gca()
  #axes.grid(True)

  ax1.set_yscale('symlog') # log y axis
  ax1.set_xlabel(r'$(M -G_ct)/M_r $', fontsize=size_axes)#das r hier markiert, dass jetz latex code kommt
  ax1.set_ylabel('Amount of cloud droplets', fontsize=size_axes)
  ax1.set_xlim(0,3.2)
  ax1.set_ylim([10**2,1*10**7])
  
  #Hide the right and top spines
  ax1.spines['right'].set_visible(False)
  ax1.spines['top'].set_visible(False)
  #Only show ticks on the left and bottom spines
  ax1.yaxis.set_ticks_position('left')
  ax1.xaxis.set_ticks_position('bottom')

  ax1.legend(loc=1, frameon=False, numpoints=1) #position of legend



  plt.show()
