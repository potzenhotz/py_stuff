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

  #plt.xticks([0.1,0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]) 
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
                  names3, p_title3, time_real_1,time_real_2,time_real_3,
                  delta_s,t_real, time_data,  
                  interval_flight, data_flight,interval_flight_2, 
                  data_flight_2, flight_err_2, data3_3, interval3):

  #setup colors
  fig, ax1  = plt.subplots()
  #fig, ax5  = plt.subplots()
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
  t_sim=time_data[plot_t[:]] #simulation time-step from time_data
  l_c = [0,1,2,3,4,5] # for colors of brewer color scale
  j=0 #counter for colors
  for k in plot_t:
    time_real_data[k]=round(time_real_data[k],0)
    label_name='t=' + str(int(time_real_data[k])) + ' min'
    if (k < t_0 ):
      scale=1.0
    else:
      scale = G*(t_sim[j]-t_0)
    ax1.plot(all_interval3[:,k]-scale,all_data3_3[:,k],color=color_set[l_c[j]],linewidth=l_w_1, label=label_name)
    #ax5.plot(all_interval3[:,k]-scale,np.gradient(np.log(all_data3_3[:,k])),color=color_set[l_c[j]],linewidth=l_w_1, label=label_name)
    j=j+1

 
  #stuff for fits but not sure anymore
  fit_start=15
  steps= np.arange(fit_start,189)
  c=1
  l=0
  b_new = np.zeros(len(steps)) 
  a_new = np.zeros(len(steps)) 
  N_integrate = np.zeros(len(steps)) 
  sigma_square_new = np.zeros(len(steps)) 


  for k in steps:
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

    #PLOT BLUE FITS AS BEFORE
    #if (k==fit_start):
    #  ax1.plot(x[0:len(x)],y[0:len(y)] , color=color_set[1], linestyle='--', linewidth=l_w_2)
    #elif (k==35):
    #  ax1.plot(x[0:len(x)],y[0:len(y)] , color=color_set[1], linestyle='--', linewidth=l_w_2)
    #c=c+2 #for the color code


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
    #print 'CURVE FIT fitpars', fitpars
    
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

  #ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[6], label=r'Extrapol t$\,\approx\,$70 min ',  linestyle='--', linewidth=l_w_2)
  #ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[7],  linestyle='--', linewidth=l_w_2)
  
  #SECOND NEW EXTRAPOLATION
  m=44 #decide which time step 
  x_plot = np.linspace(1.5,6,100) #alberto
  print 'FIT IS AT TIMESTEP', several_times[m]
  #using new interpretation of b
  new_y_extrapolation_2=np.exp(c_fixed+(b_solved[m])*(x_plot-x_zero)-(1/(2*several_sigma_square_new[m])*(x_plot-x_zero)**2))

  #ax1.plot(x_plot,new_y_extrapolation_2 , color=color_set[7], label=r'Extrapol t$\,\approx\,$400 min ',  linestyle='--', linewidth=l_w_2)
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
  #axes = plt.gca()
  #axes.grid(True)

  ax1.set_yscale('symlog') # log y axis
  ax1.set_xlabel(r'$(M -G_ct)/M_r $', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
  ax1.set_ylabel('Amount of cloud droplets', fontsize=size_axes)#,fontdict=font)
  #ax1.set_xlim(0.1,3)
  ax1.set_xlim(0,3.2)
  ax1.set_ylim([10**2,1*10**7])
  
  #Hide the right and top spines
  ax1.spines['right'].set_visible(False)
  ax1.spines['top'].set_visible(False)
  #Only show ticks on the left and bottom spines
  ax1.yaxis.set_ticks_position('left')
  ax1.xaxis.set_ticks_position('bottom')

  ax1.legend(loc=1, frameon=False, numpoints=1) #position of legend

  ##################################
  #RADIUS FOR TOP AXIS
  ##################################   
#  ax12 = ax1.twiny()
#  ax12.set_xlabel(r"Radius [$\mu m$]", fontsize=size_axes)
#  if (dycoms==0):
#    tick_locs = [0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]
#    tick_lbls = [8.2,10.3,11.8,13,14,14.9,15.7,16.4]
#  else:
#    tick_locs = [0.5,1,1.5,2.0,2.5,3.0,3.5,4.0]
#    tick_lbls = [8.9,11,12.8,14,15.2,16.1,17,17.7]
#    
#  ax12.set_xticks(tick_locs)
#  ax12.set_xticklabels(tick_lbls)
#  ax12.set_xlim(0.1,4)

  # CHANGE POSITON OF A LEGEND
  #handles, labels = ax1.get_legend_handles_labels()
  #dummy_legend_h=handles[0]
  #dummy_legend_l=labels[0]
  #handles[0] = handles[len(handles)-1]
  #labels[0] = labels[len(labels)-1]
  #handles[len(handles)-1] = dummy_legend_h
  #labels[len(labels)-1] = dummy_legend_l
  #ax1.legend(handles, labels,loc=1, frameon=False, numpoints=1)
  

  


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
#  fig, ax4 = ppl.subplots()
#
#  plt.title('fit parameter sigma square')
#  ax4.plot(steps_time,sigma_square_new, color=color_set[1],marker='.',linestyle='None',markersize=m_s+9 )
#  ax4.plot(time_extrapol,sigma_square_new_fit , color=color_set[7],linestyle='--', linewidth=l_w_2)

#
#
#  ########################################################################
#  #plot m_max with time
#  ########################################################################
#
#  fig, ax5 = ppl.subplots()
#
#  plt.title('new interpretation of b')
  #ax5.set_xlim(0.1,3.5)
#
#  ax5.plot(several_times,b_solved, color=color_set[1],marker='.',linestyle='None',markersize=m_s+9 )
  




  plt.show()
