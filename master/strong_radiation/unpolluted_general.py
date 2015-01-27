#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import scipy
import scipy.stats
import scipy.stats as ss
import os
import math
from pylab import *                  
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
from matplotlib import rcParams



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

#    if (only_last !=1):
#      #ax.plot(interval1,data1_3, color=color_set_2[8],linewidth=l_w_1, label=names1[3])
#      ax.plot(interval1,data1_3, color=color_set[1],linewidth=l_w_1, label=names1[3])

    if (dycoms ==0):     
      data2_1=data2_1*30/18*1.9
      data2_2=data2_2*30/18*1.9
      data2_3=data2_3*30/18*1.9
    else: 
      data2_1=data2_1*30/18*1.75
      data2_2=data2_2*30/18*1.75
      data2_3=data2_3*30/18*1.75
    ax.plot(interval2,data2_1, color='red',linestyle='-', linewidth=l_w_1,label=names2[1])
    ax.plot(interval2,data2_2, color='black',linestyle='-', linewidth=l_w_1, label=names2[2])
#    if (dycoms==1):
#      if (only_last !=1):
#        #ax.plot(interval2,data2_3, color=color_set_2[6],linewidth=l_w_1, label=names2[3])
#        ax.plot(interval2,data2_3, color=color_set[3],linewidth=l_w_1, label=names2[3])
#      else:  
#        ax.plot(interval2,data2_3, color=color_set[1],linewidth=l_w_1, label=names2[3])
#    else:
#     # ax.plot(interval2,data2_3, color=color_set_2[6],linewidth=l_w_1, label=names2[3])
#      if (only_last !=1):
#        ax.plot(interval2,data2_3, color=color_set[3],linewidth=l_w_1, label=names2[3])
#    if (dycoms==0):
#      data3_1=data3_1*50/18 # add the scaling factor
#      data3_2=data3_2*50/18
#      data3_3=data3_3*50/18*0.92
##     ax.plot(interval3,data3_1, color='black',linestyle=':',linewidth=l_w_1, label=names3[1])
##     ax.plot(interval3,data3_2, color='red',linestyle=':',linewidth=l_w_1,  label=names3[2])
#      #ax.plot(interval3,data3_3,color=color_set_2[4],linewidth=l_w_1, label=names3[3])
#      if (only_last !=1):
#        ax.plot(interval3,data3_3,color=color_set[5],linewidth=l_w_1, label=names3[3])
#      else:
#        ax.plot(interval3,data3_3,color=color_set[1],linewidth=l_w_1, label=names3[3])
  
  
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
      z = np.polyfit(interval3[begin_pos:end_pos+1], log_data[begin_pos:end_pos+1], 2)    
      print 'polyfit',z
      p = np.poly1d(z)
      #ax.plot(interval3[begin_pos:end_pos+1], np.exp(log_data[begin_pos:end_pos+1]), '.', color=color_set[5],linewidth=l_w_1, label='Fitting points' )
  
      mean=z[1]/(-2*z[0])
      sigma_square=(1/(-2*z[0]))
      
      #VERDI  
      if( flight ==0):
        sigma_extrapolation=0.523**2  #after 40 min
      else:  
        sigma_extrapolation=0.654**2  #after 50 min
      #sigma_extrapolation=0.784**2  #after 60 min
      a=-1/(2*sigma_extrapolation)
      mean_extrapolation=z[1]/(-2*a)
      
      x = np.linspace(0,mean+6,1000)
      print 'mean and sigma_square', mean, sigma_square 
      y_log=( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
      
      #STATISTICS
      #skewness=0
      #for o in np.arange(len(x)):
      #  skewness=skewness +((x[0]-mean)/np.sqrt(sigma_square))**3
      #skewness=skewness/len(x)
      #print 'skewness', skewness
  
      if (flight != 1):
        if (fitting == 1):
          ax.plot(x,y , color=color_set_3[0], label='Gaussian fit', linestyle='--', linewidth=l_w_2)
      if (extrapolation == 1):
        if( flight ==0):
          ax.plot(x,y_extrapolation , color=color_set[5], label='Extrapolation t=40', linestyle='--', linewidth=l_w_2)
          if(extrapolation_2==1):    
            #extrapolation for all times
            growing=[0.91, 1.82, 5.48, 10.97, 21.95]
            for k in np.arange(len(growing)):
              sigma_extrapolation=growing[k]**2
              print sigma_extrapolation 
              x = np.linspace(0,mean+115,1000)
              y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
              ax.plot(x,y_extrapolation , color=color_set[k],  linestyle='--',linewidth=l_w_2)
        else:
          ax.plot(x,y_extrapolation , color=color_set[5], label='Extrapolation t=50', linestyle='--', linewidth=l_w_2)
  
      data_flight=data_flight *5.5*10**7
      
      if (flight == 1):
        ax.plot(interval_flight,data_flight, color=color_set[9],linestyle='-', linewidth=3, label='Flight measurements')
 
      
    else:
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
      sigma_extrapolation=0.514**2
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
          growing=[0.77, 1.54, 4.6, 9.27, 18.5]
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
      if(extrapolation_2==1):    
        plt.xlim(0.9,115)
    elif(fitting == 1):
      plt.xlim(0.9,2.6)
    else:
      plt.xticks([0.1,0.5,1,1.5,2.0,2.5,3.0,3.5,4.0])
      plt.xticks([0.1,0.2,0.4,0.6,0.8,1,1.2,1.4,1.6,1.8])
      plt.xlim(0.1,2.6)
      plt.xlim(0.1,1.8)
    plt.ylim([10,10**8])
    plt.legend(loc=1, frameon=False)  
  
    plt.show()

########################################################################
#plotting sigma in time for extrapolation
########################################################################
def extrapolation_sigma(all_interval1, all_data1_3, all_interval2, all_data2_3,
                        all_interval3, all_data3_3,
                        names3, p_title3, time_real_1,time_real_2,time_real_3,
                        delta_s,t_real, dycoms, fitting, s_point):

  close='all'
  
  #print 'start fitting at' ,all_data2_3[21]

  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors

  #DATA RE800
  shape= np.shape(all_interval1) 
  time_length=shape[1]
  
  data1_3= np.zeros(100)
  interval1= np.zeros(100)
  sigma_vector_1= np.zeros(time_length)

  for k in np.arange(time_length):
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
 
  sigma_fit_1 = np.polyfit(time_real_1, sigma_vector_1, 1)
  
  ax.plot(time_real_1,sigma_vector_1 , color=color_set[1],linewidth=l_w_1,  label='Re800')
  x_fit = np.linspace(0,60,1000)
  p = sigma_fit_1[0]*x_fit + sigma_fit_1[1] 
#  if (dycoms != 0): 
#    ax.plot(x_fit,p ,linestyle='--', color=color_set[2], label='Fiting', linewidth=l_w_1)


  #DATA RE400
  shape= np.shape(all_interval2) 
  time_length=shape[1]
  
  data2_3= np.zeros(100)
  interval2= np.zeros(100)
  sigma_vector_2= np.zeros(time_length)

  for k in np.arange(time_length):
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
   
  
    z = np.polyfit(interval2[s_point:end_pos+1], log_data[s_point:end_pos+1], 2)    
    
    sigma_square=(1/(-2*z[0]))
    sigma_vector_2[k]= np.sqrt(sigma_square)
 
  sigma_fit_2 = np.polyfit(time_real_2, sigma_vector_2, 1)
  ax.plot(time_real_2,sigma_vector_2 , color=color_set[3],linewidth=l_w_1,  label='Re400')
  
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
    shape= np.shape(all_interval3) 
    time_length=shape[1]
    
    data3_3= np.zeros(100)
    interval3= np.zeros(100)
    sigma_vector= np.zeros(time_length)
    print sigma_vector[9]

    c= np.zeros(time_length)
  
    for k in np.arange(time_length):
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
     
      z = np.polyfit(interval3[s_point:end_pos+1], log_data[s_point:end_pos+1], 2)    
      
      sigma_square=(1/(-2*z[0]))
      sigma_vector[k]= np.sqrt(sigma_square)
   
    sigma_fit = np.polyfit(time_real_3, sigma_vector, 1)
    #print 'sigma_fit', sigma_fit 
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
    p =  sigma_fit[0]*x_fit + sigma_fit[1] 
    print 'Verschiebung: ', sigma_fit[1], 'Steigung: ', sigma_fit[0]
  
    ax.plot(time_real_3,sigma_vector , color=color_set[5],linewidth=l_w_1,  label='Re200')
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
    plt.ylim(0)
  else:
    plt.ylim(0,0.3)
    plt.xlim(0,25)
  plt.legend(loc=2, frameon=False)  
  
  plt.show()


########################################################################
#Fitting
########################################################################
def plot_fitting(interval3, data3_1, data3_2, data3_3):
    
  
  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors


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
        
  begin_pos=25
  print 'mean is set to', interval3[begin_pos] 
  z = np.polyfit(interval3[begin_pos:end_pos+1], log_data[begin_pos:end_pos+1], 2)    
  print 'polyfit',z
  p = np.poly1d(z)
  ax.plot(interval3[begin_pos:end_pos+1], log_data[begin_pos:end_pos+1], marker='D', color=color_set[5], label='Fitting points' )
  ax.plot(interval3, log_data, '-', color=color_set_2[8],linewidth=l_w_1, label='Lagrange' )

  mean=z[1]/(-2*z[0])
  sigma_square=(1/(-2*z[0]))
  
  #VERDI  
  sigma_extrapolation=0.8**2
  a=-1/(2*sigma_extrapolation)
  mean_extrapolation=z[1]/(-2*a)
  
  x = np.linspace(0,mean+6,1000)
  print 'mean and sigma_square', mean, sigma_square 
  y_log=( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
  y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
  y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
  
  ax.plot(x,y_log , color=color_set[2], label='Gaussian fit', linestyle='--', linewidth=l_w_2)
  

  plt.xlabel('Liquid', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
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


  fig, ax = ppl.subplots()
  color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
  color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
  #color_set_2 = brewer2mpl.get_map('Reds', 'sequential', 9).mpl_colors
  color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
  

  shape= np.shape(all_interval3) 
  time_length=shape[1]

  print time_length

   
  k=2
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x='t='+str(time_buffer)
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[1],linewidth=l_w_1, label=name_x)
  k=6
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x='t='+str(time_buffer)
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[3],linewidth=l_w_1, label=name_x)
  k=12
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x='t='+str(time_buffer)
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[5],linewidth=l_w_1, label=name_x)
  k=15
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x='t='+str(time_buffer)
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[7],linewidth=l_w_1, label=name_x)
  k=32
  time_buffer=round(time_data[k]*t_real/60,2)
  print 'real time t3',time_buffer
  name_x='t='+str(time_buffer)
  ax.plot(all_interval3[:,k],all_data3_3[:,k],color=color_set[9],linewidth=l_w_1, label=name_x)



  ax.set_yscale('symlog')
  plt.xlabel('Liquid', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  plt.ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
  plt.xlim(0,3)
  plt.ylim([10,10**8])
  plt.legend(loc=1, frameon=False)  


  plt.show()
