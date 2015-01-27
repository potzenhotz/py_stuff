#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm
import os
import math


########################################################################
#Read raw data 
########################################################################
def read_data(data_path, tstart, tend, tstep, nbins):
    
  ntimes = (tend - tstart) / tstep + 1
  interval= np.zeros((nbins,ntimes))
  eulerian= np.zeros((nbins,ntimes))
  l_diff= np.zeros((nbins,ntimes))
  l_nodiff= np.zeros((nbins,ntimes))
  i=0
  for t in np.arange(ntimes):
    l_t=t+(tstart/100)
    step=l_t*tstep
    data_name=data_path + 'particle_pdf.' + np.str(step)   #name of file
    
    interval[:,i],eulerian[:,i],l_diff[:,i], l_nodiff[:,i] = np.loadtxt(data_name, unpack=True) # read file into data
    i=i+1
  return (interval, eulerian, l_diff, l_nodiff)


def read_timedata(data_path, time_data):
     
  data_name=data_path + 'times.log' #name of file
  print data_name
  time_data = np.loadtxt(data_name, unpack=True) # read file into data
  return (time_data)



########################################################################
#Save plot routine
########################################################################
def save(path, ext, close, verbose):
  # Extract the directory and filename from the given path
  directory = os.path.split(path)[0]
  filename = "%s.%s" % (os.path.split(path)[1], ext)
  if directory == '':
    directory = '.'
   
  # If the directory does not exist, create it
  if not os.path.exists(directory):
    os.makedirs(directory)
   
  # The final path to save to
  savepath = os.path.join(directory, filename)
   
  if verbose:
    print("Saving figure to '%s'..." % savepath),
   
  # Actually save the figure
  plt.savefig(savepath)
  # Close it
  if close:
    plt.close()
   
  if verbose:
    print("Done")



########################################################################
#Plotting routine
########################################################################
def plot_data(interval,data_1, data_2, data_3, names, style, p_title):

  close='all'
  if ( style == 0): 

    fig, ax = plt.subplots()
    ax.plot(interval,data_1, color='black', label=names[1])
    ax.plot(interval,data_2, color='red',  label=names[2])
    ax.plot(interval,data_3, color='blue',linestyle='-', label=names[3])
    
#    ax.plot(extra_interval,extra_data_1, color='black',linestyle='--', label='low resolution')
#    ax.plot(extra_interval,extra_data_2, color='red', linestyle='--', label='low resolution')
#    ax.plot(extra_interval,extra_data_3, color='blue',linestyle='--', label='low resolution')
    
    ax.set_yscale('symlog')
    plt.title(p_title)
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0.5,4)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
    
    plt.show()
  elif (style == 1):
  
    width = 0.05
    opacity=0.7
    fig, ax = plt.subplots()
    ax.bar(interval,data_2,width, color='red', label=names[2])
    ax.bar(interval,data_3,width, color='black', alpha=opacity, label=names[3])
    plt.title('First plot')
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0.5,2)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
    
    plt.show()


########################################################################
#Plotting to compare to caeses
########################################################################
def plot_data_compare(interval1,data1_1, data1_2, data1_3, 
                      interval2, data2_1, data2_2, data2_3,
                      names1, style, p_title1, names2, p_title2):

  close='all'
  if ( style == 0): 

    fig, ax = plt.subplots()
    ax.plot(interval1,data1_1, color='black', label=names1[1])
    ax.plot(interval1,data1_2, color='red',  label=names1[2])
    ax.plot(interval1,data1_3, color='blue',linestyle='-', label=names1[3])

#    data2_1=data2_1*30/18 # add the scaling factor
#    data2_2=data2_2*30/18
#    data2_3=data2_3*50/18*8
#    ax.plot(interval2,data2_1, color='black',linestyle='--', label=names2[1])
#    ax.plot(interval2,data2_2, color='red',linestyle='--',  label=names2[2])
#    ax.plot(interval2,data2_3, color='blue',linestyle='--', label=names2[3])
    
    axes = plt.gca()
    axes.grid(True)

    ax.set_yscale('symlog')
    plt.title(p_title1)
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0.5,4)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
    
    plt.show()

########################################################################
#Plotting to compare to caeses plus flight data
########################################################################
def plot_data_compare_2(interval1,data1_1, data1_2, data1_3, 
                      interval2, data2_1, data2_2, data2_3,
                      names1, style, p_title1, names2, p_title2, flight_i, flight_d):

  close='all'
  if ( style == 0): 


    integral_flight= np.zeros(1)  
    integral_dy= np.zeros(1)  
#    flight_d=flight_d*5*129533000
    for i in np.arange(len(interval1)):
      integral_dy=integral_dy+data1_3[i]*0.05
    
    for i in np.arange(len(flight_i)-1):
      integral_flight=integral_flight +(flight_i[i+1]-flight_i[i])*flight_d[i]
 
    fig, ax = plt.subplots()
    
    
    
#    data1_3=data1_3*integral_flight
    ax.plot(interval1,data1_1, color='black', label=names1[1])
    ax.plot(interval1,data1_2, color='red',  label=names1[2])
    ax.plot(interval1,data1_3, color='blue',linestyle='-', label=names1[3])

    data2_1=data2_1*30/18 # add the scaling factor
    data2_2=data2_2*30/18
    data2_3=data2_3*50/18*5
#    ax.plot(interval2,data2_1, color='black',linestyle='--', label=names2[1])
#    ax.plot(interval2,data2_2, color='red',linestyle='--',  label=names2[2])
    ax.plot(interval2,data2_3, color='blue',linestyle='--', label=names2[3])
   
  
    flight_d=flight_d*integral_dy/integral_flight
#    flight_d=flight_d*30000000
    ax.plot(flight_i,flight_d, color='green',linestyle='-', label='flight data')
    
    axes = plt.gca()
    axes.grid(True)

#    ax.set_yscale('symlog')
    plt.title(p_title1)
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0,4)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
    
    plt.show()

#    integral_flight= np.zeros(1)  
#    integral_dy= np.zeros(1)  
#    flight_d=flight_d*5*129533000
#    for i in np.arange(len(interval1)):
#      integral_dy=integral_dy+data1_3[i]*0.05
#    
#    for i in np.arange(len(flight_i)-1):
#      integral_flight=integral_flight +(flight_i[i+1]-flight_i[i])*flight_d[i]
#    print integral_dy, integral_flight 

########################################################################
#Plotting stuff with time
########################################################################
def plot_data_time(interval,data_1, data_2, data_3, names, style, nbins, tstart, tend, tstep, p_title_part,time_data):

  close='all'

  a_o_p_threshold=5 #amout of particle threshold
  ntimes = (tend - tstart) / tstep + 1
  time= np.zeros((ntimes))
  max_data_1= np.zeros((ntimes))
  max_data_2= np.zeros((ntimes))
  max_data_3= np.zeros((ntimes))
  for j in np.arange(ntimes):
    time[j]=(j+1)*100
    for i in np.arange(nbins):
      if (data_1[i,j] >= math.pow(10,a_o_p_threshold)):
        max_data_1[j]=i
      if (data_2[i,j] >= math.pow(10,a_o_p_threshold)):
        max_data_2[j]=i
      if (data_3[i,j] >= math.pow(10,a_o_p_threshold)):
        max_data_3[j]=i

  max_data_1[:]=max_data_1[:]*0.05
  max_data_2[:]=max_data_2[:]*0.05
  max_data_3[:]=max_data_3[:]*0.05
  
#  np.save('extra_max_data_1',max_data_1)
#  np.save('extra_max_data_2',max_data_2)
#  np.save('extra_max_data_3',max_data_3)
#  np.save('extra_time',time_data)
  
  extra_data_1=np.load('extra_max_data_1.npy')
  extra_data_2=np.load('extra_max_data_2.npy')
  extra_data_3=np.load('extra_max_data_3.npy')
  extra_time=np.load('extra_time.npy')


  if ( style == 0): 
    
    fig, ax = plt.subplots()
    ax.plot(time_data,max_data_1, color='black',marker='o', label=names[1])
    ax.plot(time_data,max_data_2, color='red', marker='o' , label=names[2])
    ax.plot(time_data,max_data_3, color='blue',linestyle='-',marker='o', label=names[3])

    ax.plot(extra_time,extra_data_1, color='black',linestyle='--', marker='o', label='low resolution')
    ax.plot(extra_time,extra_data_2, color='red', linestyle='--', marker='o' , label='low resolution')
    ax.plot(extra_time,extra_data_3, color='blue',linestyle='--',marker='o', label='low resolution')
#    ax.set_yscale('symlog')
    plt.title(p_title_part)
    plt.xlabel('Time')
    plt.ylabel('Liquid')
#    plt.xlim(0.5,4)
    plt.ylim([min(max_data_1)-0.1, max(max_data_3)+0.1])
    plt.legend(loc=2, prop={'size':12})   
    
    plt.show()


########################################################################
#Plotting stuff with time
########################################################################
def plot_data_several(interval,data_1, data_2, data_3, names, style, nbins, tstart, tend, tstep, p_title):

  close='all'

  if ( style == 0): 

    actual_timestep_1=2000
    first_data=(actual_timestep_1-tstart)/tstep
    actual_timestep_2=3100
    second_data=(actual_timestep_2-tstart)/tstep

    l1_interval=interval[:,first_data] 
    l1_data_1=data_1[:,first_data] 
    l1_data_2=data_2[:,first_data] 
    l1_data_3=data_3[:,first_data] 

    l2_interval=interval[:,second_data] 
    l2_data_1=data_1[:,second_data] 
    l2_data_2=data_2[:,second_data] 
    l2_data_3=data_3[:,second_data] 


    opacity=1
    fig, ax = plt.subplots()
    ax.plot(l1_interval,l1_data_1, color='black',linestyle='--', alpha=opacity, label=names[1])
    ax.plot(l1_interval,l1_data_2, color='red', linestyle='--', alpha=opacity , label=names[2])
    ax.plot(l1_interval,l1_data_3, color='blue',linestyle='--', alpha=opacity, label=names[3])
    ax.plot(l2_interval,l2_data_1, color='black', label=names[1])
    ax.plot(l2_interval,l2_data_2, color='red', label=names[2])
    ax.plot(l2_interval,l2_data_3, color='blue', label=names[3])
    ax.set_yscale('symlog')
    plt.title(p_title)
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0.5,4)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
   
    plt.show()

########################################################################
#Save Plots
########################################################################
def save_plot_data(interval,data_1, data_2, data_3, names, style, p_title, s_title, format):
  close='all'
  if ( style == 0): 
    
    fig, ax = plt.subplots()
    ax.plot(interval,data_1, color='black', label=names[1])
    ax.plot(interval,data_2, color='red' , label=names[2])
    ax.plot(interval,data_3, color='blue',linestyle='-', label=names[3])
    ax.set_yscale('symlog')
    plt.title(p_title)
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0.5,4)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
    
    save(s_title, ext=format, close=False, verbose=True)
  elif (style == 1):
  
    width = 0.05
    opacity=0.7
    fig, ax = plt.subplots()
    ax.bar(interval,data_2,width, color='red', label=names[2])
    ax.bar(interval,data_3,width, color='black', alpha=opacity, label=names[3])
    plt.title('First plot')
    plt.xlabel('Liquid') #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles')
    plt.xlim(0.5,2)
    #plt.ylim([-0.5,2])
    plt.legend(loc=1, prop={'size':12})   
    
    save(s_title, ext='pdf', close=False, verbose=True)

