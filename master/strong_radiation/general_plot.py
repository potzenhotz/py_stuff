#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.mlab as mlab
import scipy
import scipy.stats
import scipy.stats as ss
import os
import math
from pylab import *                  
import prettyplotlib as ppl
from prettyplotlib import brewer2mpl
from matplotlib import rcParams

#rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = ['Times']
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Helvetica']
#rcParams['font.weight'] = 'light'
rcParams['text.usetex'] = True

rcParams['axes.labelsize'] = 38
rcParams['xtick.labelsize'] = 34
rcParams['ytick.labelsize'] = 34
rcParams['legend.fontsize'] = 30
size_title=30
size_axes=34

#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
#rc('text', usetex=True)
#font = {'size'   : 18}
#matplotlib.rc('font', **font)
rcParams['axes.linewidth'] = 1.5

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
    l_t=t+(tstart/tstep)
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
#    data2_3=data2_3*30/18
    ax.plot(interval2,data2_1, color='black',linestyle='--', label=names2[1])
    ax.plot(interval2,data2_2, color='red',linestyle='--',  label=names2[2])
    ax.plot(interval2,data2_3, color='blue',linestyle='--', label=names2[3])
    
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
                      interval3, data3_1, data3_2, data3_3,
                      interval_flight, data_flight,
                      names1, style, p_title1, names2, p_title2, names3, p_title3,dycoms):

  close='all'
  if ( style == 0): 


    fig, ax = ppl.subplots()
    color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
    color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
    
    
    
#    ax.plot(interval1,data1_1, color='black', label=names1[1])
#    ax.plot(interval1,data1_2, color='red',  label=names1[2])
#    ax.plot(interval1,data1_3, color='blue',linestyle='-', label=names1[3])
    ax.plot(interval1,data1_3, color=color_set_2[4],linewidth=2, label=names1[3])

    data2_1=data2_1*30/18 # add the scaling factor
    data2_2=data2_2*30/18
    if (dycoms ==0):     
      data2_3=data2_3*30/18*1.9
    else: 
      data2_3=data2_3*30/18*2
#    ax.plot(interval2,data2_1, color='black',linestyle='--', label=names2[1])
#    ax.plot(interval2,data2_2, color='red',linestyle='--',  label=names2[2])
    ax.plot(interval2,data2_3, color=color_set_2[6],linewidth=2, label=names2[3])
    if (dycoms==0):
      data3_1=data3_1*50/18 # add the scaling factor
      data3_2=data3_2*50/18
      data3_3=data3_3*50/18*0.92
#     ax.plot(interval3,data3_1, color='black',linestyle=':',linewidth=2, label=names3[1])
#     ax.plot(interval3,data3_2, color='red',linestyle=':',linewidth=2,  label=names3[2])
      ax.plot(interval3,data3_3,color=color_set_2[8],linewidth=2, label=names3[3])

########################################################################
#playground
########################################################################
#    print interval1[0:34]
#    print data1_3[0:34]
#    size=1000000
#    dist_names = ['alpha', 'beta', 'arcsine',
#                  'weibull_min', 'weibull_max', 'rayleigh']
#    
#    for dist_name in dist_names:
#        dist = getattr(scipy.stats, dist_name)
#        param = dist.fit(data1_3[23:34])
#        pdf_fitted = dist.pdf(interval1[23:34], *param[:-2], loc=param[-2], scale=param[-1]) * size
#        ax.plot(pdf_fitted, label=dist_name)
#    plt.legend(loc='upper left')

#    beg=26
#    end=beg+34
#    beg_l=beg+1
#    end_l=beg_l+15
#    mirror=np.zeros(50)
#    dummy=np.zeros(16)
#    dummy[0:15]=data3_3[beg_l:end_l]
#    dummy=dummy[::-1]
#    mirror[0:16]=dummy[0:16]
#    mirror[16:50]=data3_3[beg:end]
    
#    integral_data= np.zeros(1)  
#    for i in np.arange(23,len(data3_3)):
#      integral_data=integral_data+data3_3[i]*0.05
      

#    approx_var_1= np.zeros(1)  
#    approx_var_2= np.zeros(1)  
#    j=0
#    for i in np.arange(21,len(data3_3)):
#      if (approx_var_2 < 1 ):
#        approx_var_1=approx_var_1+ data3_3[i]*0.05 
#        #approx_var_2=approx_var_1 -integral_data*2*0.3413
#        approx_var_2=approx_var_1 -np.std(mirror)
#        j=j+1
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
            
  
      z = np.polyfit(interval3[24:end_pos+1], log_data[24:end_pos+1], 2)    
      print 'polyfit',z
      p = np.poly1d(z)
      #ax.plot(interval3[24:end_pos+1], np.exp(log_data[24:end_pos+1]), '.', color=color_set[4], label='Fiting points' )
  
      mean=z[1]/(-2*z[0])
      sigma_square=(1/(-2*z[0]))
      
      sigma_extrapolation=0.8**2
      a=-1/(2*sigma_extrapolation)
      mean_extrapolation=z[1]/(-2*a)
      
      x = np.linspace(0,mean+6,1000)
      print 'mean and sigma_square', mean, sigma_square 
      #y= (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) 
      y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
      
      #STATISTICS
      skewness=0
      for o in np.arange(len(x)):
        skewness=skewness +((x[0]-mean)/np.sqrt(sigma_square))**3
      skewness=skewness/len(x)
      print 'skewness', skewness
  
      ax.plot(x,y , color=color_set[2], label='Gaussian fit', linestyle='--', linewidth=2)
      ax.plot(x,y_extrapolation , color=color_set[5], label='Gaussian extrapolation t=60', linestyle='--', linewidth=2)
  
      data_flight=data_flight *5*10**7
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
            
       
      z = np.polyfit(interval2[24:end_pos+1], log_data[24:end_pos+1], 2)    
      print 'polyfit',z
      p = np.poly1d(z)
     #ax.plot(interval3[24:end_pos+1], np.exp(log_data[24:end_pos+1]), '.', color=color_set[4], label='Fiting points' )
  
      mean=z[1]/(-2*z[0])
      sigma_square=(1/(-2*z[0]))
      
      sigma_extrapolation=0.8**2
      a=-1/(2*sigma_extrapolation)
      mean_extrapolation=z[1]/(-2*a)
      
      x = np.linspace(0,mean+6,1000)
      print 'mean and sigma_square', mean, sigma_square 
      #y= (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) 
      y=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_square)) )
      y_extrapolation=np.exp( (z[2]+z[1]**2/(4*-z[0]))-(((x-mean)**2)/(2*sigma_extrapolation)) )
      
      ax.plot(x,y , color=color_set[3], label='Gaussian fit', linestyle='--', linewidth=2)
#      ax.plot(x,y_extrapolation , color=color_set[5], label='Gaussian extrapolation t=60', linestyle='--', linewidth=2)
    

#    ax.plot(interval1[beg-16:beg+34],mirror, color='red')


#    mean = 1.24
#    variance = 0.009
#    variance_arb = 0.001
#    sigma = np.sqrt(variance)
#    x = np.linspace(-3,5,1000)
#    y = mlab.normpdf(x,mean,sigma)
#    y = y*20000*(variance_arb/variance)
#    ax.plot(x,y, color='magenta')
########################################################################
#playground end
########################################################################

    #axes = plt.gca()
    #axes.grid(True)

    ax.set_yscale('symlog')
    #ax.set_title(p_title3)#,fontdict=font)
#    if (dycoms ==0):     
#      plt.title(p_title3, fontsize=size_title)#,fontdict=font)
#    else:
#      plt.title(p_title2, fontsize=size_title)#,fontdict=font)
    plt.xlabel('Liquid', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
    plt.ylabel('Amount of particles', fontsize=size_axes)#,fontdict=font)
    plt.xlim(0,4)
    plt.ylim([10,10**8])
    plt.legend(loc=1, frameon=False)  
    
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
#plotting sigma in time for extrapolation
########################################################################

    
def extrapolation_sigma(all_interval1, all_data1_3, all_interval2, all_data2_3,
                        all_interval3, all_data3_3,
                        names3, p_title3, time_real_1,time_real_2,time_real_3,delta_s,t_real, dycoms):

  close='all'
 
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
   
  
    z = np.polyfit(interval1[24:end_pos+1], log_data[24:end_pos+1], 2)    
    
    sigma_square=(1/(-2*z[0]))
    sigma_vector_1[k]= np.sqrt(sigma_square)
 
  sigma_fit_1 = np.polyfit(time_real_1, sigma_vector_1, 1)
  
  ax.plot(time_real_1,sigma_vector_1 , color=color_set[3],linewidth=2,  label='Data Re800')
  x_fit = np.linspace(0,60,1000)
  p = sigma_fit_1[0]*x_fit + sigma_fit_1[1] 
  #p = sigma_fit_2[0]*x_fit**2 + sigma_fit_2[1]*x_fit + sigma_fit_2[2] 
#  if (dycoms != 0): 
#    ax.plot(x_fit,p ,linestyle='--', color=color_set[2], label='Fiting', linewidth=2)


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
   
  
    z = np.polyfit(interval2[24:end_pos+1], log_data[24:end_pos+1], 2)    
    
    sigma_square=(1/(-2*z[0]))
    sigma_vector_2[k]= np.sqrt(sigma_square)
 
  sigma_fit_2 = np.polyfit(time_real_2, sigma_vector_2, 1)
  
  ax.plot(time_real_2,sigma_vector_2 , color=color_set[5],linewidth=2,  label='Data Re400')
  
  x_fit = np.linspace(0,60,1000)
  p = sigma_fit_2[0]*x_fit + sigma_fit_2[1] 
  #p = sigma_fit_2[0]*x_fit**2 + sigma_fit_2[1]*x_fit + sigma_fit_2[2] 
#  if (dycoms != 0): 
#    ax.plot(x_fit,p ,linestyle='--', color=color_set[4], label='Fitting', linewidth=2)

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
     
      z = np.polyfit(interval3[24:end_pos+1], log_data[24:end_pos+1], 2)    
      
      sigma_square=(1/(-2*z[0]))
      sigma_vector[k]= np.sqrt(sigma_square)
   
    sigma_fit = np.polyfit(time_real_3, sigma_vector, 1)
    print 'sigma_fit', sigma_fit 
  
    x_fit = np.linspace(0,60,1000)
    #p = sigma_fit[0]*x_fit**2 + sigma_fit[1]*x_fit + sigma_fit[2] 
    p =  sigma_fit[0]*x_fit + sigma_fit[1] 
  
    ax.plot(time_real_3,sigma_vector , color=color_set[1],linewidth=2,  label='Data Re200')
    ax.plot(x_fit,p , color=color_set[0],linestyle='--', linewidth=2, label='Fitting')
    
    tau=t_real/delta_s
    print len(time_real_3), len(sigma_vector)
    for l in np.arange(len(time_real_3)):
      c[l] = sigma_vector[l]*tau/time_real_3[l]
    print np.mean(c), sigma_fit[0]
    #p_test=np.mean(c)*x_fit
    #ax.plot(x_fit,p_test ,color=color_set[9],linewidth=2,  label='bla')

  #GENERAL PLOT SETTINGS
#  if(dycoms == 0):
#    plt.title(r'VERDI - Growth of $\sigma$ in time', fontsize=size_title)#,fontdict=font)
#  else:
#    plt.title(r'DYCOMS-II - Growth of $\sigma$ in time', fontsize=size_title)#,fontdict=font)

  plt.xlabel('t [min]')#, fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  plt.ylabel(r'\textbf{$\sigma$}')#, fontsize=size_axes)#,fontdict=font)
  #plt.xlim(0,4)
  plt.ylim(0)
  plt.legend(loc=2, frameon=False)  
  
  plt.show()

 

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

