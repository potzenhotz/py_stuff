#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.optimize as so
import scipy.stats as ss
import os
import math
from pylab import *                  
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
from matplotlib import rcParams
#from scipy.optimize import curve_fit


########################################################################
#Setup plot enviroment 
########################################################################
#rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = ['Times']
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Helvetica']
#rcParams['font.weight'] = 'light'
rcParams['text.usetex'] = True

rcParams['axes.labelsize'] = 58
rcParams['xtick.labelsize'] = 58
rcParams['ytick.labelsize'] = 58
#rcParams['legend.fontsize'] = 52
rcParams['legend.fontsize'] = 37
#rcParams['legend.fontsize'] = 72 #for different Re
size_title=30
size_axes=58
l_w_1=4.5
l_w_2=6.5
m_s=22

#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
#rc('text', usetex=True)
#font = {'size'   : 18}
#matplotlib.rc('font', **font)
rcParams['axes.linewidth'] = 2.5
rcParams.update({'figure.autolayout':True})


########################################################################
#Read raw data 
########################################################################

#DATA
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


########################################################################
#Plotting to compare to caeses plus flight data
########################################################################
def plot_data_compare_2(interval1,data1_1, data1_2, data1_3, 
                      interval2, data2_1, data2_2, data2_3,
                      interval3, data3_1, data3_2, data3_3,
                      interval_flight, data_flight,
                      names1, style, p_title1, names2, p_title2, names3, p_title3,
                      dycoms,extrapolation,extrapolation_2 , fitting,flight, only_last, s_point):
  close='all'
  if ( style == 0): 
    #COLORS FOR PLOTTING 
    fig, ax = ppl.subplots()
    color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
    color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
    #color_set_2 = brewer2mpl.get_map('Reds', 'sequential', 9).mpl_colors
    color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
   
  #!!!!!!!!!!!!!
  #General
  #!!!!!!!!!!!!!
    
    
#    ax.plot(interval1,data1_1, color='black', linewidth=l_w_1,label=names1[1])
#    ax.plot(interval1,data1_2, color='red',  linewidth=l_w_1,label=names1[2])
#    ax.plot(interval1,data1_3, color='blue',linestyle='-', label=names1[3])

    if (only_last !=1):
      #ax.plot(interval1,data1_3, color=color_set_2[8],linewidth=l_w_1, label=names1[3])
      ax.plot(interval1,data1_3, color=color_set[1],linewidth=l_w_1, label=names1[3])

    if (dycoms ==0):     
      data2_1=data2_1*30/18*1.9
      data2_2=data2_2*30/18*1.9
      data2_3=data2_3*30/18*1.9
    else: 
      data2_1=data2_1*30/18*1.75
      data2_2=data2_2*30/18*1.75
      data2_3=data2_3*30/18*1.75
#    ax.plot(interval2,data2_1, color='red',linestyle='-', linewidth=l_w_1,label=names2[1])
#    ax.plot(interval2,data2_2, color='black',linestyle='-', linewidth=l_w_1, label=names2[2])
    if (dycoms==1):
      if (only_last !=1):
        #ax.plot(interval2,data2_3, color=color_set_2[6],linewidth=l_w_1, label=names2[3])
        ax.plot(interval2,data2_3, color=color_set[3],linewidth=l_w_1, label=names2[3])
      else:  
        ax.plot(interval2,data2_3, color=color_set[1],linewidth=l_w_1, label=names2[3])
    else:
     # ax.plot(interval2,data2_3, color=color_set_2[6],linewidth=l_w_1, label=names2[3])
      if (only_last !=1):
        ax.plot(interval2,data2_3, color=color_set[3],linewidth=l_w_1, label=names2[3])
    if (dycoms==0):
      data3_1=data3_1*50/18 # add the scaling factor
      data3_2=data3_2*50/18
      data3_3=data3_3*50/18*0.92
      #ax.plot(interval3,data3_1, color='black',linestyle='-',linewidth=l_w_1, label=names3[1])
      #ax.plot(interval3,data3_2, color='red',linestyle='-',linewidth=l_w_1,  label=names3[2])
      #ax.plot(interval3,data3_3,color=color_set_2[4],linewidth=l_w_1, label=names3[3])
      if (only_last !=1):
        ax.plot(interval3,data3_3,color=color_set[5],linewidth=l_w_1, label=names3[3])
      else:
        if( flight ==0):
          ax.plot(interval3,data3_3,color=color_set[1],linewidth=l_w_1, label=names3[3])
  
  #!!!!!!!!!!!!!
  #Fitting
  #!!!!!!!!!!!!!
    if (dycoms ==0):     
      log_data= np.zeros(100)  
      log_interval= np.zeros(100) 
   
      for i in np.arange(len(data3_3)):
        if (data3_3[i] != 0):
          log_data[i] = np.log(data3_3[i])
        elif (data3_3[i] == 0):
          log_data[i]=data3_3[i]
      j=1
      max_val=max(log_data)   
      max_val_pos=len(log_data)+1 
      for i in np.arange(len(log_data)):
        if ( log_data[i] == max_val):
          max_val_pos=i
        if (i > max_val_pos):
          if (log_data[i] <= 0):
            end_pos=i
            break
            
      begin_pos=s_point
      print 'mean is set to', interval3[begin_pos] 
      print 'end_pos', end_pos 
      z = np.polyfit(interval3[begin_pos:end_pos+1], log_data[begin_pos:end_pos+1], 2)    
      print 'polyfit',z
      p = np.poly1d(z)
      #ax.plot(interval3[begin_pos:end_pos+1], np.exp(log_data[begin_pos:end_pos+1]), '.', color=color_set[5],linewidth=l_w_1, label='Fitting points' )
  
      mean=z[1]/(-2*z[0])
      sigma_square=(1/(-2*z[0]))
      
      #VERDI  
      if( flight ==0):
        sigma_extrapolation=0.545**2  #after 40 min
      else:  
        #sigma_extrapolation=0.764**2  #after 50 min
        sigma_extrapolation=0.74**2  #after 50 min
      #sigma_extrapolation=0.91**2  #after 60 min
      a=-1/(2*sigma_extrapolation)
      mean_extrapolation=z[1]/(-2*a)
      
      x = np.linspace(0,mean+6,1000)
      print 'mean and sigma_square', mean, sigma_square 
      y_log=( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
      
  
      if (flight != 1): #no fligh data
        if (fitting == 1):  #if we want fit
          ax.plot(x,y , color=color_set_3[0], label='Gaussian fit', linestyle='--', linewidth=l_w_2)
      if (extrapolation == 1):  #if we want extrapolation
        if( flight ==0):  #if we want no fligh data
          ax.plot(x,y_extrapolation , color=color_set[5], label='Extrapolation t=40', linestyle='--', linewidth=l_w_2)
          if(extrapolation_2==1): #if we want second extrapolation
            #extrapolation for all times
            growing=[0.91, 1.80, 5.37, 10.7, 21.4]
            for k in np.arange(len(growing)):
              sigma_extrapolation=growing[k]**2
              print sigma_extrapolation 
              x = np.linspace(0,mean+115,1000)
              y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
              ax.plot(x,y_extrapolation , color=color_set[k],  linestyle='--',linewidth=l_w_2)
        else: #if we want extrapolation with flight data together
          ax.plot(x,y_extrapolation , color=color_set[5], label=r'Extrapolation t$\,\approx\,$50 [min]', linestyle='--', linewidth=l_w_2)
      
      #SCALE FLIGHT DATA 
      data_flight=data_flight *5.5*10**7
      
      if (flight == 1):
        ax.plot(interval_flight,data_flight, color=color_set[9],marker='.',linestyle='None',markersize=m_s+9 , label='Flight measurements')
 
      
    else: #if we want DYCOMS instead of verdi
      log_data= np.zeros(100)  
      log_interval= np.zeros(100) 
   
      for i in np.arange(len(data2_3)):
        if (data2_3[i] != 0):
          log_data[i] = np.log(data2_3[i])
        elif (data2_3[i] == 0):
          log_data[i]=data2_3[i]
      j=1
      max_val=max(log_data)   
      max_val_pos=len(log_data)+1 
      for i in np.arange(len(log_data)):
        if ( log_data[i] == max_val):
          max_val_pos=i
        if (i > max_val_pos):
          if (log_data[i] <= 0):
            end_pos=i
            break
            
       
      z = np.polyfit(interval2[s_point:end_pos+1], log_data[s_point:end_pos+1], 2)    
      print 'polyfit',z
      p = np.poly1d(z)
      #ax.plot(interval3[24:end_pos+1], np.exp(log_data[24:end_pos+1]), '.', color=color_set[4], label='Fiting points' )
  
      mean=z[1]/(-2*z[0])
      sigma_square=(1/(-2*z[0]))
     
      #DYCOMS 
      sigma_extrapolation=0.525**2
      a=-1/(2*sigma_extrapolation)
      mean_extrapolation=z[1]/(-2*a)
      print sigma_extrapolation
      
      x = np.linspace(0,mean+6,1000)
      print 'mean and sigma_square', mean, sigma_square 
      y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
      
      if (fitting == 1):
        ax.plot(x,y , color=color_set_3[0], label='Gaussian fit', linestyle='--', linewidth=l_w_2)
      if (extrapolation == 1):
        ax.plot(x,y_extrapolation , color=color_set[5], label='Extrapolation t=40', linestyle='--',linewidth=l_w_2)
        if(extrapolation_2==1):    
          #extrapolation for all times
          growing=[0.76, 1.49, 4.4, 8.75, 17.4]
          for k in np.arange(len(growing)):
            sigma_extrapolation=growing[k]**2
            print sigma_extrapolation 
            x = np.linspace(0,mean+100,1000)
            y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
            ax.plot(x,y_extrapolation , color=color_set[k],  linestyle='--',linewidth=l_w_2)
 


  #!!!!!!!!!!!!!
  #Plotting
  #!!!!!!!!!!!!!
    
    #GRID LINES
    #axes = plt.gca()
    #axes.grid(True)

    ax.set_yscale('symlog')
#    if (dycoms ==0):     
#      plt.title(p_title3, fontsize=size_title)#,fontdict=font)
#    else:
#      plt.title(p_title2, fontsize=size_title)#,fontdict=font)
    plt.xlabel(r'$M/M_r$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
    if (extrapolation == 1):
      plt.xlim(0.9,5.2)
      plt.xlim(0.8,4.5)
      #plt.xlim(1.3,5.2)
      if(extrapolation_2==1):    
        plt.xlim(0.9,115)
      elif(flight == 1):
        ax2 = ax.twiny()
        ax2.set_xlabel(r"Radius [$\mu m$]", fontsize=size_axes)
        tick_locs = [1,2,3,4,5]
        tick_lbls = [10.3,13,14.9,16.4,17.7]
          
        ax2.set_xticks(tick_locs)
        ax2.set_xticklabels(tick_lbls)
        #ax2.set_xlim(1.3,5.2)
        ax2.set_xlim(0.8,4.5)
        ax.legend(loc=0, frameon=False)
    elif(fitting == 1):
      plt.xlim(0.9,2.6)
    else:
      plt.xticks([0.1,0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]) 
      plt.xlim(0.1,2.6)
    plt.ylim([10,10**8])
    #plt.ylim([10**3,10**9])
    plt.ylim([10**3,10**8])
    #plt.xlim([0.9,3.0])
    plt.legend(loc=1, frameon=False)  
  
    plt.show()

########################################################################
#plotting sigma in time for extrapolation
########################################################################
def extrapolation_sigma(all_interval1, all_data1_3, all_interval2, all_data2_3,
                        all_interval3, all_data3_3,
                        names1,names2,names3, p_title3, time_real_1,time_real_2,time_real_3,
                        delta_s,t_real, dycoms, fitting, s_point):

  sp=5  #part of determination of first timestep of sigma calculation

  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors

  #WE WILL ANALYZE THE DIFFERENT RE-NUMBER RUNS 

  #DATA RE800 
  if (dycoms == 1):
    cf=5
  else:
    cf=3
  shape= np.shape(all_interval1) 
  time_length=shape[1]
  
  data1_3= np.zeros(100)
  interval1= np.zeros(100)
  sigma_vector_1= np.zeros(time_length)

  for k in np.arange(sp+cf,time_length):
    data1_3[:] = all_data1_3[:,k]
    interval1[:] = all_interval1[:,k]
    log_data= np.zeros(100)  
   
    for i in np.arange(len(data1_3)):
      if (data1_3[i] != 0):
        log_data[i] = np.log(data1_3[i])
      elif (data1_3[i] == 0):
        log_data[i]=data1_3[i]
    j=1
    max_val=max(log_data)   
    max_val_pos=len(log_data)+1 
    for i in np.arange(len(log_data)):
      if ( log_data[i] == max_val):
        max_val_pos=i
      if (i > max_val_pos):
        if (log_data[i] <= 0):
          end_pos=i
          break
   
    z = np.polyfit(interval1[s_point:end_pos+1], log_data[s_point:end_pos+1], 2)    
    
    sigma_square=(1/(-2*z[0]))
    sigma_vector_1[k]= np.sqrt(sigma_square)
  sigma_fit_1 = np.polyfit(time_real_1[sp+cf:time_length], sigma_vector_1[sp+cf:time_length], 1)
  
  ax.plot(time_real_1[sp+cf:time_length],sigma_vector_1[sp+cf:time_length] , color=color_set[1],marker='.',
linestyle='None',markersize=m_s ,  label=names1[3])
  x_fit = np.linspace(0,60,1000)
  p = sigma_fit_1[0]*x_fit + sigma_fit_1[1] 
#  if (dycoms != 0): 
#    ax.plot(x_fit,p ,linestyle='--', color=color_set[2], label='Fiting', linewidth=l_w_1)


  #DATA RE400
  cf=3
  if (dycoms == 1):
    cf=5
  shape= np.shape(all_interval2) 
  time_length=shape[1]
  time_length_re400=shape[1]
  
  mean_fits400=np.zeros(50)
  data2_3= np.zeros(100)
  interval2= np.zeros(100)
  sigma_vector_2= np.zeros(time_length)
  for k in np.arange(sp+cf,time_length):
    data2_3[:] = all_data2_3[:,k]
    interval2[:] = all_interval2[:,k]

    log_data= np.zeros(100)  
   
    for i in np.arange(len(data2_3)):
      if (data2_3[i] != 0):
        log_data[i] = np.log(data2_3[i])
      elif (data2_3[i] == 0):
        log_data[i]=data2_3[i]
    j=1
    max_val=max(log_data)   
    max_val_pos=len(log_data)+1 
    for i in np.arange(len(log_data)):
      if ( log_data[i] == max_val):
        max_val_pos=i
      if (i > max_val_pos):
        if (log_data[i] <= 0):
          end_pos=i
          break
   
  
    mean_fits400[k]=log_data[s_point]
    z = np.polyfit(interval2[s_point:end_pos+1], log_data[s_point:end_pos+1], 2)    
    
    sigma_square=(1/(-2*z[0]))
    sigma_vector_2[k]= np.sqrt(sigma_square)
    #print sigma_square, z[0]
  sigma_fit_2 = np.polyfit(time_real_2[sp+cf:time_length], sigma_vector_2[sp+cf:time_length], 1)
  ax.plot(time_real_2[sp+cf:time_length],sigma_vector_2[sp+cf:time_length] , color=color_set[3],marker='.',linestyle='None',markersize=m_s,  label=names2[3])
  if (dycoms != 0): 
    #LIQUID AFTER SPECIFIED TIME  
    #1 hour
    x_fit = np.linspace(0,60,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=60: ', p[len(p)-1]
    #2 hour
    x_fit = np.linspace(0,120,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=120: ', p[len(p)-1]
    #6 hour
    x_fit = np.linspace(0,360,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=360: ', p[len(p)-1]
    #12 hour
    x_fit = np.linspace(0,720,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=720: ', p[len(p)-1]
    #24 hour
    x_fit = np.linspace(0,1440,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=1440: ', p[len(p)-1]
    #48 hour
    x_fit = np.linspace(0,2880,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=2880: ', p[len(p)-1]
    
    x_fit = np.linspace(0,40,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'Verschiebung: ', sigma_fit_2[1], 'Steigung: ', sigma_fit_2[0]
  if (dycoms != 0): 
    if (fitting == 1):
      print 'sigma at x=40: ', p[len(p)-1]
      ax.plot(x_fit,p ,linestyle='--', color=color_set[3], label='Fitting', linewidth=l_w_2)
      

  if (dycoms == 0):
    #DATA RE200
    cf=0
    shape= np.shape(all_interval3) 
    time_length=shape[1]
    
    data3_3= np.zeros(100)
    interval3= np.zeros(100)
    sigma_vector= np.zeros(time_length)
    #print sigma_vector[9]

    c= np.zeros(time_length)
  
    mean_fits200=np.zeros(50)
    for k in np.arange(sp+cf,time_length):
      data3_3[:] = all_data3_3[:,k]
      interval3[:] = all_interval3[:,k]
  
      log_data= np.zeros(100)  
      log_interval= np.zeros(100) 
     
      for i in np.arange(len(data3_3)):
        if (data3_3[i] != 0):
          log_data[i] = np.log(data3_3[i])
        elif (data3_3[i] == 0):
          log_data[i]=data3_3[i]
      j=1
      max_val=max(log_data)   
      max_val_pos=len(log_data)+1 
      for i in np.arange(len(log_data)):
        if ( log_data[i] == max_val):
          max_val_pos=i
        if (i > max_val_pos):
          if (log_data[i] <= 0):
            end_pos=i
            break

      mean_fits200[k]=log_data[s_point]

      z = np.polyfit(interval3[s_point:end_pos+1], log_data[s_point:end_pos+1], 2)    
      
      sigma_square=(1/(-2*z[0]))
      sigma_vector[k]= np.sqrt(sigma_square)
     
    sigma_fit = np.polyfit(time_real_3[sp+cf:time_length], sigma_vector[sp+cf:time_length], 1)
    #print 'sigma_fit', sigma_fit 
    #LIQUID AFTER SPECIFIED TIME  
    #30 min
    x_fit = np.linspace(0,30,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=30: ', p[len(p)-1]
    #40 min
    x_fit = np.linspace(0,40,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=40: ', p[len(p)-1]
    #40 min
    x_fit = np.linspace(0,41,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=41: ', p[len(p)-1]
    #50 min
    x_fit = np.linspace(0,50,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=50: ', p[len(p)-1]
    #1 hour
    x_fit = np.linspace(0,60,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=60: ', p[len(p)-1]
    #2 hour
    x_fit = np.linspace(0,120,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=120: ', p[len(p)-1]
    #6 hour
    x_fit = np.linspace(0,360,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=360: ', p[len(p)-1]
    #12 hour
    x_fit = np.linspace(0,720,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=720: ', p[len(p)-1]
    #24 hour
    x_fit = np.linspace(0,1440,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=1440: ', p[len(p)-1]
    #48 hour
    x_fit = np.linspace(0,2880,10000)
    p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
    print 'sigma at x=2880: ', p[len(p)-1]
  
    x_fit = np.linspace(0,40,10000)
    p =  sigma_fit[0]*x_fit + sigma_fit[1] 
    print 'Verschiebung: ', sigma_fit[1], 'Steigung: ', sigma_fit[0]
  
    ax.plot(time_real_3[sp+cf:time_length],sigma_vector[sp+cf:time_length] , color=color_set[5],marker='.',linestyle='None',markersize=m_s,  label=names3[3])
    if (fitting == 1):
      print 'sigma at x=40: ', p[len(p)-1]
      ax.plot(x_fit,p , color=color_set[5],linestyle='--', linewidth=l_w_2, label='Fitting')
    

  #GENERAL PLOT SETTINGS
#  if(dycoms == 0):
#    plt.title(r'VERDI - Growth of $\sigma$ in time', fontsize=size_title)#,fontdict=font)
#  else:
#    plt.title(r'DYCOMS-II - Growth of $\sigma$ in time', fontsize=size_title)#,fontdict=font)

  plt.xlabel('t [min]')#, fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  plt.ylabel(r'\textbf{$\sigma$}', fontsize=90)#, fontsize=size_axes)#,fontdict=font)
  #plt.xlim(0,40)
  if (fitting == 1):
    plt.ylim(0,0.35)
    plt.xlim(0,25)
  else:
    plt.ylim(0,0.35)
    plt.xlim(2,22)
  plt.legend(loc=2, frameon=False)  
  
  plt.show()
  plt.clf()

  fig, ax = ppl.subplots()
  if(dycoms == 0):
    print 'after plot', time_real_3 , sp+cf, time_length
    print 'first time step', time_real_3[sp+cf]
    print mean_fits200
    print 'first', mean_fits200[sp+cf], 'at point', sp+cf
  

  if(dycoms == 0):
    ax.plot(time_real_3[sp+cf:time_length],(mean_fits200[sp+cf:time_length]/mean_fits200[sp+cf]), color=color_set[5],linestyle='--',linewidth=l_w_2, label='Droplet number')
  else:
    ax.plot(time_real_2[sp+cf:time_length_re400],(mean_fits400[sp+cf:time_length_re400]/mean_fits400[sp+cf]), color=color_set[5],linestyle='--',linewidth=l_w_2, label='Droplet number')
   
  plt.xlabel('t [min]')#, fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  plt.ylabel(r'$N_{1.35}(t) / N_{1.35}(t_{0})$')#, fontsize=size_axes)#,fontdict=font)
  #ax.set_yscale('symlog')
  #plt.ylim(0.98,1.02)
  #plt.legend(loc=1, frameon=False)

  plt.show()



########################################################################
#Fitting
########################################################################
def plot_fitting(interval3, data3_1, data3_2, data3_3):
    
  #COLORS FOR FIGURES
  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors

  #SCALE DATA
  data3_3=data3_3*50/18*0.92
  #ax.plot(interval3,data3_3,color=color_set_2[8],linewidth=l_w_1, label=names3[3])

  
  
  #!!!!!!!!!!!!!
  #Fitting
  #!!!!!!!!!!!!!
  log_data= np.zeros(100)  
  log_interval= np.zeros(100) 

  for i in np.arange(len(data3_3)):
    if (data3_3[i] != 0):
      log_data[i] = np.log(data3_3[i])
    elif (data3_3[i] == 0):
      log_data[i]=data3_3[i]
  j=1
  max_val=max(log_data)   
  max_val_pos=len(log_data)+1 
  for i in np.arange(len(log_data)):
    if ( log_data[i] == max_val):
      max_val_pos=i
    if (i > max_val_pos):
      if (log_data[i] <= 0):
        end_pos=i
        break
        
  begin_pos=s_point
  print 'mean is set to', interval3[begin_pos] 
  z = np.polyfit(interval3[begin_pos:end_pos+1], log_data[begin_pos:end_pos+1], 2)    
  print 'polyfit',z
  p = np.poly1d(z)
  ax.plot(interval3[begin_pos:end_pos+1], log_data[begin_pos:end_pos+1], marker='D', color=color_set[5], label='Fitting points' )
  ax.plot(interval3, log_data, '-', color=color_set_2[8],linewidth=l_w_1, label='Lagrange' )

  mean=z[1]/(-2*z[0])
  sigma_square=(1/(-2*z[0]))

  #!!!!!!!!
  #VERDI  CAREFULL OLD VALUE FOR SIGAM EXTRAPOLATION
  #!!!!!!!!
  sigma_extrapolation=0.8**2
  a=-1/(2*sigma_extrapolation)
  mean_extrapolation=z[1]/(-2*a)
  
  x = np.linspace(0,mean+6,1000)
  print 'mean and sigma_square', mean, sigma_square 
  y_log=( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
  y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
  y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
  
  ax.plot(x,y_log , color=color_set[2], label='Gaussian fit', linestyle='--', linewidth=l_w_2)
  
  #PLOT PROPERTIES
  plt.xlabel(r'$M/M_r$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  plt.ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
  plt.legend(loc=1, frameon=False)  
  
  plt.xlim(0,4)
  plt.ylim(0,20)
  plt.show()

########################################################################
#several time steps of one simulation
########################################################################
def several_times(all_interval3, all_data3_3,
                  names3, p_title3, time_real_1,time_real_2,time_real_3,
                  delta_s,t_real, time_data, dycoms, fitting, s_point):

  #COLORS FOR FIGURES
  fig, ax = plt.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
  #color_set_2 = brewer2mpl.get_map('Reds', 'sequential', 9).mpl_colors
  color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
  
  #SCALE DATA
  if (dycoms == 0):
    all_data3_3=all_data3_3*50/18*0.92
  else:
    all_data3_3=all_data3_3*30/18*1.75

  shape= np.shape(all_interval3) 
  time_length=shape[1]

  print time_length


  #EXPLICIT PLOT OF DIFFERENT TIME STEPS
  k=0 #VERDI
#  k=10
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x=str(time_buffer)+ ' min'
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[0],linewidth=l_w_1, label=name_x)
  k=3 #VERDI
#  k=10
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x=str(time_buffer)+ ' min'
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[1],linewidth=l_w_1, label=name_x)
  k=8 #VERDI
#  k=14
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x=str(time_buffer)+ ' min'
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[3],linewidth=l_w_1, label=name_x)
  k=13 #VERDI
#  k=20
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x=str(time_buffer)+ ' min'
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[5],linewidth=l_w_1, label=name_x)
#  k=22 #VERDI
  k=22
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x=str(time_buffer)+ ' min'
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[7],linewidth=l_w_1, label=name_x)
#  k=35 #VERDI
  k=35
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x=str(time_buffer)+ ' min'
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[9],linewidth=l_w_1, label=name_x)


  #PLOT PROPERTIES
  ax.set_yscale('symlog')
  ax.set_xlabel(r'$M/M_r$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  ax.set_ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
  ax.set_xticks([0.1,0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]) 
  ax.set_xlim(0.1,3)
  ax.set_ylim([10,10**8])
  
  ax2 = ax.twiny()
  ax2.set_xlabel(r"Radius [$\mu m$]", fontsize=size_axes)
  if (dycoms==0):
    tick_locs = [0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]
    tick_lbls = [8.2,10.3,11.8,13,14,14.9,15.7,16.4]
  else:
    tick_locs = [0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]
    tick_lbls = [8.9,11,12.8,14,15.2,16.1,17,17.7]
    
  ax2.set_xticks(tick_locs)
  ax2.set_xticklabels(tick_lbls)
  ax2.set_xlim(0.1,3)
  ax.legend(loc=0, frameon=False)
  
  plt.legend(loc=1, frameon=False)  


  plt.show()


########################################################################
#several fittings  
########################################################################
def several_fits(all_interval3, all_data3_3,
                  names3, p_title3, time_real_1,time_real_2,time_real_3,
                  delta_s,t_real, time_data, dycoms, fitting, s_point):


  #SETUP COLORS FOR PLOTTING
  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
  #color_set_2 = brewer2mpl.get_map('Reds', 'sequential', 9).mpl_colors
  color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
  
  #scale data  
  if (dycoms == 0):
    all_data3_3=all_data3_3*50/18*0.92
  else:
    all_data3_3=all_data3_3*30/18*1.75

  #DECIDE ABOUT PLOTTING STEPS
  time_real_data=np.zeros(len(time_data))
  for i in np.arange(len(time_data)): 
    time_real_data[i]=round(time_data[i]*t_real/60,2)
  if (dycoms==0):  
    steps=[9, 14, 22, 35]
  else:
    steps=[10, 20, 28, 35]
  c=1 #for color code

  #CONSTRUCT DATA FROM WHERE TO FIT (TAIL) AND PLOT DIFFERENT STEPS
  for k in steps:
    label_name='t=' + str(time_real_data[k]) + ' [min]'
    ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[c],linewidth=l_w_1, label=label_name)

    log_data= np.zeros(100)  
    log_interval= np.zeros(100) 
    for i in np.arange(len(all_data3_3[:,k])):
      if (all_data3_3[i,k] != 0):
        log_data[i] = np.log(all_data3_3[i,k])
      elif (all_data3_3[i,k] == 0):
        log_data[i]=all_data3_3[i,k]
    j=1
    max_val=max(log_data)   
    max_val_pos=len(log_data)+1 
    for i in np.arange(len(log_data)):
      if ( log_data[i] == max_val):
        max_val_pos=i
      if (i > max_val_pos):
        if (log_data[i] <= 0):
          end_pos=i
          break
          
    #CONSTRUCT FITS FOR SIMULATION STEPS
    z = np.polyfit(all_interval3[s_point:end_pos+1,k], log_data[s_point:end_pos+1], 2)    
    print 'point where fitting starts', all_interval3[s_point,k], np.exp(log_data[s_point])
    print 'polyfit',z
    p = np.poly1d(z)

    mean=z[1]/(-2*z[0])
    sigma_square=(1/(-2*z[0]))
   
    x = np.linspace(0,mean+6,1000)
    print 'mean and sigma_square', mean, sigma_square 
    y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )

    print x[210]
    ax.plot(x[0:len(x)],y[0:len(y)] , color=color_set[c], linestyle='--', linewidth=l_w_2)

    c=c+2 #for color code


  #PLOTTING PROPERTIES
  ax.set_yscale('symlog')
  plt.xlabel(r'$M/M_r$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  plt.ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
  if(dycoms==0):
    plt.xlim(1.4,2.7)
  else:
    plt.xlim(1.4,2.3)
  plt.ylim([10,5*10**6])
  plt.legend(loc=1, frameon=False)  


  plt.show()



########################################################################
#several fittings plus flight data 
########################################################################
def several_times_and_flight(all_interval3, all_data3_3,
                  names3, p_title3, time_real_1,time_real_2,time_real_3,
                  delta_s,t_real, time_data, dycoms, fitting, s_point, 
                  interval_flight, data_flight,data3_3, interval3):

  #setup colors
  fig, ax1  = plt.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
  #color_set_2 = brewer2mpl.get_map('Reds', 'sequential', 9).mpl_colors
  color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
  

  shape= np.shape(all_interval3) 
  time_length=shape[1]

  #scale data  
  all_data3_3=all_data3_3*50/18*0.92

  #sum of all particles
  sum_all_data3_3 = np.zeros(time_length) 
  for i in np.arange(time_length):
    sum_all_data3_3[i]=np.sum(all_data3_3[:,i])
    sum_all_data3_3[i]=sum_all_data3_3[i]-all_data3_3[0,i]

  ########################################################################
  #Plot the flight data
  ########################################################################
  data_flight=data_flight*2.25*10**7#alberto
  #data_flight=data_flight*5.0*10**7
  #ax1.plot(interval_flight,data_flight, color=color_set[9],marker='.',linestyle='None',markersize=m_s+9 , label='Flight measurements')
  #alberto
  #ax1.plot(interval_flight,data_flight, color=color_set[9],marker='.',linestyle='None',markersize=m_s+9 )
  ax1.plot(interval_flight,data_flight, color=color_set[9],marker='.',linestyle='None',markersize=m_s+9 , label='Flight measurements')

  ########################################################################
  #Plot the data+fit
  ########################################################################
  print 'AHAHAHA', all_data3_3.shape
  time_real_data=np.zeros(len(time_data))
  for i in np.arange(len(time_data)): 
    time_real_data[i]=round(time_data[i]*t_real/60,2)
  print 'real time',time_real_data
  #steps=np.array([12,23, 35])
  fit_start=15
  #steps= np.arange(fit_start,36)
  steps= np.arange(fit_start,100)
  print 'here steps', steps
  c=1
  l=0
  b_new = np.zeros(len(steps)) 
  a_new = np.zeros(len(steps)) 
  N_integrate = np.zeros(len(steps)) 
  sigma_square_new = np.zeros(len(steps)) 
  for k in steps:
    time_real_data[k]=round(time_real_data[k],0)
    label_name='t=' + str(int(time_real_data[k])) + ' min'
    #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[c],linewidth=l_w_1, label='Simulation ' + label_name)
    #alberto
    #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[c],linewidth=l_w_1)
    if (k==fit_start):
      #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[1],linewidth=l_w_1)
      ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[1],linewidth=l_w_1, label='Simulation ' + label_name)
    elif (k==35):
      #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[1],linewidth=l_w_1)
      ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[1],linewidth=l_w_1, label='Simulation ' + label_name)
    elif (k==55):
      #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[3],linewidth=l_w_1)
      ax1.plot(all_interval3[:,k]/1.065,all_data3_3[:,k],color=color_set[3],linewidth=l_w_1, label='Simulation ' + label_name)
    elif (k==79):
      #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[5],linewidth=l_w_1)
      ax1.plot(all_interval3[:,k]/1.08,all_data3_3[:,k],color=color_set[5],linewidth=l_w_1, label='Simulation ' + label_name)
    elif (k==99):
      #ax1.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[9],linewidth=l_w_1)
      ax1.plot(all_interval3[:,k]/1.108,all_data3_3[:,k],color=color_set[9],linewidth=l_w_1, label='Simulation ' + label_name)
    log_data= np.zeros(100)  
    log_interval= np.zeros(100) 
    for i in np.arange(len(all_data3_3[:,k])):
      if (all_data3_3[i,k] != 0):
        log_data[i] = np.log(all_data3_3[i,k])
      elif (all_data3_3[i,k] == 0):
        log_data[i]=all_data3_3[i,k]
    j=1
    max_val=max(log_data)   
    max_val_pos=len(log_data)+1 
    for i in np.arange(len(log_data)):
      if ( log_data[i] == max_val):
        max_val_pos=i
      if (i > max_val_pos):
        if (log_data[i] <= 0):
          end_pos=i
          break
          

    #POLYNOMIAL FIT       
    z = np.polyfit(all_interval3[s_point:end_pos+1,k], log_data[s_point:end_pos+1], 2)    
    p = np.poly1d(z)

    mean=z[1]/(-2*z[0])
    sigma_square=(1/(-2*z[0]))
   
    x = np.linspace(1.75,mean+6,1000) #alberto
    y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )

    if (k==fit_start):
      ax1.plot(x[0:len(x)],y[0:len(y)] , color=color_set[1], linestyle='--', linewidth=l_w_2)
    elif (k==35):
      ax1.plot(x[0:len(x)],y[0:len(y)] , color=color_set[1], linestyle='--', linewidth=l_w_2)
    c=c+2 #for the color code


    #CURVE FITTIN

    c_fixed=13.75
    x_zero=1.6
    def pol_func(x,a,b):
      return a*(x-x_zero)**2+b*(x-x_zero)+c_fixed
      #return a*(x-x_zero)**2+b*(x-x_zero)+c
      #return a*(x)**2+b*(x)+c

    

    fitpars, covmat = so.curve_fit(pol_func,all_interval3[s_point:end_pos+1,k], log_data[s_point:end_pos+1])
   
    mean_new=fitpars[1]/(-2*fitpars[0])
    sigma_square_calc=(1/(-2*fitpars[0]))
    
    #NEW Y WITH x=x-x_zero
    y_new=np.exp( (c_fixed+fitpars[1]**2/(4*-fitpars[0]))-((((x-x_zero)-mean_new)**2)/(2*sigma_square_calc)) )
    print 'CURVE FIT fitpars', fitpars
    
    #GET/CALCULATE FIT PARAMETERS
    a_new[l]=fitpars[0]
    b_new[l]=fitpars[1]
    sigma_square_new[l]=-1/(2*fitpars[0])
    
    aa=a_new[l]
    bb=b_new[l]
    
    #CALCULATE THE AMOUNT OF DROPLETS IN THE TAIL
    def exp_pol_func(x):
      return np.exp(aa*(x-x_zero)**2+bb*(x-x_zero)+c_fixed)

    N_integrate2=scipy.integrate.quad(exp_pol_func, x_zero,10)
    N_integrate[l] = N_integrate2[0]/sum_all_data3_3[l+fit_start]
    
    #COUNT STEP +1
    l=l+1



  #############################################
  #LINEAR FIT FOR a AND FOR b
  #############################################
  def lin_func(x,a,b):  #linear fit
    return a*(x)+b

  def pol2_func(x,a,b,c): #polynomial fit
    return a*(x)**2+b*x+c

  def tanh_func(x,a,b,c): #hyperbolicus tangential fit
    return c+a*np.tanh(x+b)

  def sqrt_func(x,a,b,c): #root fit
    return c+a*np.sqrt(x+b)

  def asympt_func(x,a,b,c): #asymptotic fit
    return c+b/x+a/(x**2)
  
  #fitpars_a_new, covmat_2 = so.curve_fit(lin_func,steps,a_new)
  fitpars_a_new, covmat_2 = so.curve_fit(asympt_func,steps,a_new)
  #fitpars_a_new, covmat_2 = so.curve_fit(tanh_func,steps,a_new)
  #fitpars_a_new, covmat_2 = so.curve_fit(sqrt_func,steps,a_new)
  #fitpars_a_new, covmat_2 = so.curve_fit(pol2_func,steps,a_new)
  fitpars_b_new, covmat_3 = so.curve_fit(lin_func,steps,b_new)
  fitpars_sigma_square_new, covmat_3 = so.curve_fit(lin_func,steps,sigma_square_new)
  time_part=np.arange(0,len(time_real_3))
  fitpars_time, covmat_3 = so.curve_fit(lin_func,time_part,time_real_3)

  ######################################################################
  #GENERAL EXTRAPOLATION
  ######################################################################
  #USING ACTUAL FIT FOR time
  x = np.linspace(5,90,100)
  
  time_extrapol=fitpars_time[0]*x+fitpars_time[1] 
  steps_time=fitpars_time[0]*steps+fitpars_time[1] 
  
  
  #USING ACTUAL FIT FOR b 
  test_b  = fitpars_b_new[0]*x+fitpars_b_new[1]
  
  #USING ACTUAL FIT FOR a 
  #a_fit = fitpars_a_new[0]*x+fitpars_a_new[1]
  a_fit = fitpars_a_new[0]*(1.0/x**2)+fitpars_a_new[1]*(1.0/x)+c_fixed
  #a_fit = fitpars_a_new[2]+fitpars_a_new[0]*np.tanh(x+fitpars_a_new[1])
  #a_fit = fitpars_a_new[2]+fitpars_a_new[0]*np.sqrt(x+fitpars_a_new[1])
  #a_fit = fitpars_a_new[0]*x**2+fitpars_a_new[1]*x + fitpars_a_new[2]
  
  #USING FIT FOR SIGMA_SQUARE
  sigma_square_new_fit  = fitpars_sigma_square_new[0]*x+fitpars_sigma_square_new[1]
  


  ######################################################################
  #SEVERAL STEPS FOR USING THE EXTRAPOLATION
  ######################################################################
  #SEVERAL TIME STEPS
  several_x = np.arange(10,900,20) #from 10,20,30 ... 180,190
  several_times=fitpars_time[0]*several_x+fitpars_time[1] 
  
  
  several_test_b = fitpars_b_new[0]*several_x+fitpars_b_new[1]

  #several_a = fitpars_a_new[0]*several_x+fitpars_a_new[1]
  several_a = fitpars_a_new[0]*(1.0/several_x**2)+fitpars_a_new[1]*(1.0/several_x)+fitpars_a_new[2]
  #several_a = fitpars_a_new[2]+fitpars_a_new[0]*np.tanh(several_x+fitpars_a_new[1])
  #several_a = fitpars_a_new[2]+fitpars_a_new[0]*np.sqrt(several_x+fitpars_a_new[1])
  #several_a = fitpars_a_new[0]*several_x**2+fitpars_a_new[1]*several_x +fitpars_a_new[2]
 
  several_sigma_square_new = fitpars_sigma_square_new[0]*several_x+fitpars_sigma_square_new[1]
  
   
  print 'several times', several_times
  print 'several_sigma_new', several_sigma_square_new
  

  ######################################################################
  #SOLVE EQUATION FOR B NUMERICAL
  ######################################################################
  b_solved = np.zeros(len(several_x)) 
  a_sigma = np.zeros(len(several_x)) #a calculated from sigma 
  for m in np.arange(len(several_x)):
    a_sigma[m]=-1/(2*several_sigma_square_new[m])
    k_const=0.00075
    k_const=0.002
    def func_for_b(b_solve):
      return(np.exp(-b_solve**2/(4*a_sigma[m])+c_fixed)*np.sqrt(np.pi)*(1+scipy.special.erf(b_solve/(2*np.sqrt(-a_sigma[m])))))/(2*np.sqrt(-a_sigma[m]))-k_const*np.mean(sum_all_data3_3)
    b_initial_guess=-3
    b_solved[m]= so.fsolve(func_for_b,b_initial_guess) 
  
  print 'the mean of all droplets', np.mean(sum_all_data3_3) 
  #FIRST NEW EXTRAPOLATION
  m=7 #decide which time step 
  x_plot = np.linspace(1.5,6,100) #alberto
  print 'FIT IS AT TIMESTEP', several_times[m]
  #using new interpretation of b
  new_y_extrapolation_2=np.exp(c_fixed+(b_solved[m])*(x_plot-x_zero)-(1/(2*several_sigma_square_new[m])*(x_plot-x_zero)**2))

  ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[6], label=r'Extrapol t$\,\approx\,$70 min ',  linestyle='--', linewidth=l_w_2)
  #ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[7],  linestyle='--', linewidth=l_w_2)
  
  #SECOND NEW EXTRAPOLATION
  m=44 #decide which time step 
  x_plot = np.linspace(1.5,6,100) #alberto
  print 'FIT IS AT TIMESTEP', several_times[m]
  #using new interpretation of b
  new_y_extrapolation_2=np.exp(c_fixed+(b_solved[m])*(x_plot-x_zero)-(1/(2*several_sigma_square_new[m])*(x_plot-x_zero)**2))

  ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[7], label=r'Extrapol t$\,\approx\,$400 min ',  linestyle='--', linewidth=l_w_2)
  #ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[7],  linestyle='--', linewidth=l_w_2)
  

  ######################################################################
  #WRITE FILE WITH EXTRAPOLATION
  ######################################################################

  extra_steps = np.arange(1.6,5,0.05)
  steps_y_extrapolation=np.exp(c_fixed+(b_solved[m])*(extra_steps-x_zero)-(1/(2*several_sigma_square_new[m])*(extra_steps-x_zero)**2))
  
  #print interval3[32] # point at which interval is at 1.6
  #print all_data3_3[0:32,35]
  
  write_interval=interval3
  write_mass= np.concatenate((all_data3_3[0:32,35],steps_y_extrapolation))
  
  #save scaled real data
  f = open('scaled_particle_pdf2000','w')
  for i in range(0,100):
    f.write('%4s %5s\n' %(write_interval[i], all_data3_3[i,19]))
  f.close()


  #f = open('extrapol_471min','w')
  #for i in range(0,100):
  #  f.write('%4s %5s\n' %(write_interval[i], write_mass[i]))
  #f.close()

  ########################################################################
  #PLOT PROPERTIES
  ########################################################################
  begin_pos=s_point
  print 'mean is set to', interval3[begin_pos]


  #GRID LINES
  axes = plt.gca()
  axes.grid(True)

  ax1.set_yscale('symlog')
  #ax1.set_xlabel(r'$M/M_r$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  #alberto
  #ax1.set_xlabel('Droplet mass', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  ax1.set_xlabel(r'$M/M_r$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  ax1.set_ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
  ax1.set_xlim(0.8,4)#alberto
  ax1.set_xlim(0.1,4)#alberto
  ax1.set_ylim([10**2,10**8])
  #ax1.set_ylim([0,10**8])
  
  #Hide the right and top spines
  #ax1.spines['right'].set_visible(False)
  #ax1.spines['top'].set_visible(False)
  #Only show ticks on the left and bottom spines
  #ax1.yaxis.set_ticks_position('left')
  #ax1.xaxis.set_ticks_position('bottom')


   
#  ax12 = ax1.twiny()
#  ax12.set_xlabel(r"Radius [$\mu m$]", fontsize=size_axes)
  if (dycoms==0):
    tick_locs = [0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]
    tick_lbls = [8.2,10.3,11.8,13,14,14.9,15.7,16.4]
  else:
    tick_locs = [0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]
    tick_lbls = [8.9,11,12.8,14,15.2,16.1,17,17.7]
    
#  ax12.set_xticks(tick_locs)
#  ax12.set_xticklabels(tick_lbls)
#  ax12.set_xlim(0.1,3)
  ax1.legend(loc=0, frameon=False)
  
  plt.legend(loc=1, frameon=False)  


#  ########################################################################
#  #plot a with time
#  ########################################################################
#
#  fig, ax2 = ppl.subplots()
#  plt.title('fit parameter a')
#  ax2.set_yscale('symlog')
#
#  ax2.plot(write_interval,write_mass , color=color_set[9], label=r'Extrapolation t$\,\approx\,$70 min ',  linestyle='--', linewidth=l_w_2)
#  ax2.plot(steps_time,a_new, color=color_set[5],marker='.',linestyle='None',markersize=m_s+9 )
##  ax2.plot(time_extrapol,a_fit , color=color_set[5],linestyle='--', linewidth=l_w_2)
#
#
#  ########################################################################
#  #plot b with time
#  ########################################################################
#
#  fig, ax3 = ppl.subplots()
#
#  plt.title('amount of particles in tail')
#
#  ax3.plot(steps_time,N_integrate, color=color_set[3],marker='.',linestyle='None',markersize=m_s+9 )
##  ax3.plot(time_extrapol,test_b , color=color_set[3],linestyle='--', linewidth=l_w_2)
#
#
  ########################################################################
  #plot sigma_square with time
  ########################################################################
  fig, ax4 = ppl.subplots()

  plt.title('fit parameter sigma square')
  ax4.plot(steps_time,sigma_square_new, color=color_set[1],marker='.',linestyle='None',markersize=m_s+9 )
  ax4.plot(time_extrapol,sigma_square_new_fit , color=color_set[7],linestyle='--', linewidth=l_w_2)

#
#
#  ########################################################################
#  #plot m_max with time
#  ########################################################################
#
#  fig, ax5 = ppl.subplots()
#
#  plt.title('new interpretation of b')
#
#  ax5.plot(several_times,b_solved, color=color_set[1],marker='.',linestyle='None',markersize=m_s+9 )
  











  plt.show()
