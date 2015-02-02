#!/usr/bin/python2.7
#
# script to process DNS statistics
# Chiel van Heerwaarden, 2011
#
# Added input functionality, Thomas Keitzl, 2013
#
# Works for python/2.7-cdat
# Works for python/2.7-ve2

import sys
import numpy as np
import unpolluted_general
import matplotlib.pyplot as plt
from matplotlib import rcParams

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)

#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
#rc('text', usetex=True)
#font = {'size'   : 18}
#matplotlib.rc('font', **font)

########################################################################
#Setup data path
########################################################################


dycoms=0
compare=1
extrapolation=0
extrapolation_2=0
fitting=0
flight=0
only_last=0
s_point=32 #start point of fitting normal 27 for alberto 35
several_times=0
several_times_and_flight=1
several_fits=0

stratification=1

if (dycoms==0):
  #data_path_1 = '/home/zmaw/u300202/python/master/data_ar_re800/'  
  #data_path_1 = '/home/zmaw/u300202/python/master/data_ar_re800_rescale/'  
  #data_path_2 = '/home/zmaw/u300202/python/master/data_ar_re400_stretch_rescale/'  
  #data_path_3 = '/home/zmaw/u300202/python/master/data_ar_re200_stretch/'  
  #data_path_1 = '/home/zmaw/u300202/python/master/general/data_ar_re800_general/'  
  data_path_1 = 'data_ar_re800_general/'  
  #data_path_2 = '/home/zmaw/u300202/python/master/general/data_ar_re400_stretch_general/'  
  data_path_2 = 'data_ar_re400_stretch_general/'  
  if (stratification==0):
    data_path_3 = 'data_ar_re200_stretch_general/'  
    #data_path_3 = '/home/zmaw/u300202/python/master/general/data_ar_re200_stretch_general/'  
  else:
    data_path_3 = 'data_ar_re200_stretch_general_strat/'  
    #data_path_3 = '/home/zmaw/u300202/python/master/general/data_ar_re200_stretch_general_strat/'  
  data_path_4= 'flight_data/'
  #data_path_4= '/home/zmaw/u300202/python/master/general/flight_data/'

else:
#  data_path_1 = '/home/zmaw/u300202/python/master/data_dy_re800/'  
#  data_path_2 = '/home/zmaw/u300202/python/master/data_dy_re400_stretch/'  
  data_path_1 = '/home/zmaw/u300202/python/master/general/data_dy_re800_general/'  
  data_path_2 = '/home/zmaw/u300202/python/master/general/data_dy_re400_stretch_general/'  
 


########################################################################
#Setup global values
########################################################################
if (dycoms==0):
  tstart_1  = 100
  tend_1    = 3100 #Arctic
  tstep_1   = 100
else:
  tstart_1  = 100
  tend_1    = 3500  #Dycoms
  tstep_1   = 100

if (dycoms==0):
  tstart_2  = 100   
  tend_2    = 3600 
  tstep_2   = 100
else:
  tstart_2  = 100
  tend_2    = 3600
  tstep_2   = 100
  
tstart_3  = 100
#tstart_3  = 200
if (stratification==0):
  tend_3    = 3600
else:
  tend_3    = 10000
tstep_3   = 100

nbins   = 100
style   = 0

if (dycoms==0):
  plt_ts_1        = 2900 #plot_timestep
  #plt_ts_1        = 1500 #plot_timestep
  plt_ts_2        = 1700 #plot_timestep
  #plt_ts_2        = 900 #plot_timestep
  plt_ts_3        = 900 #plot_timestep
  #plt_ts_3        = 500 #plot_timestep
  if (only_last ==1):
    plt_ts_3        = 3300 #plot_timestep
else:
  plt_ts_1        = 3200 #plot_timestep
#  plt_ts_1        = 1000 #plot_timestep
  plt_ts_2        = 2000 #plot_timestep
#  plt_ts_2        = 600 #plot_timestep
#  plt_ts_2        = 300 #plot_timestep
  if (only_last ==1):
    plt_ts_2        = 3600 #plot_timestep
    plt_ts_2        = 2000 #plot_timestep
  plt_ts_3        = 900 #plot_timestep


plt_ts_1=(plt_ts_1-tstart_1)/tstep_1 
plt_ts_2=(plt_ts_2-tstart_2)/tstep_2 
plt_ts_3=(plt_ts_3-tstart_3)/tstep_3 

print plt_ts_1, plt_ts_2 

p_title_part_1  = 'VERDI'
#p_title_part_1  = 'DYCOMS_II'
#p_title_part_2  = 'ARCTIC Re=400'
p_title_part_2  = 'DYCOMS_II Re=400'
p_title_part_t  = ' - Time: '

#p_title_1 = p_title_part_1+p_title_part_t+str((plt_ts_1+1)*100)
#p_title_2 = p_title_part_2+p_title_part_t+str((plt_ts_2+1)*100)
#p_title_3 = p_title_part_2+p_title_part_t+str((plt_ts_2+1)*100)

plot_type=0


time_data_1=np.zeros(100)
time_data_2=np.zeros(100)
time_data_3=np.zeros(100)
time_data_1 = unpolluted_general.read_timedata(data_path_1, time_data_1)
time_data_2 = unpolluted_general.read_timedata(data_path_2, time_data_2)
if (dycoms==0):
  time_data_3 = unpolluted_general.read_timedata(data_path_3, time_data_3)
  print 'LALALALA', len(time_data_3)
if (plot_type == 0):
  

  ########################################################################
  #Calculate real time
  ########################################################################
  if (dycoms==0):
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
  
    Ri=1/0.0351
    D=-0.11
    chi_s=0.2
    C_2=0.29
    delta_s=(Ri*(D+chi_s))/(C_2*(1-chi_s))
    print 'verdi delta_s', delta_s
  
  else:   
    #DYCOMS
    t_lambda=15
    t_F=70
    t_gravity=9.81
    t_rho_c=1.130
    t_cp=1022
    t_T_c=284.15
    B=t_F*t_gravity/(t_rho_c*t_cp*t_T_c)
    t_real=((t_lambda**2)/B)**(0.3333333)
    u_0=(B*t_lambda)**(0.333333)
    print 'dycoms t_o is:' ,t_real
    print 'dycoms B_o is:' ,B
    print 'dycoms U_o is:' ,u_0
  

    Ri=40
    D=0.031
    chi_s=0.09
    C_2=0.4745
    delta_s=(Ri*(D+chi_s))/(C_2*(1-chi_s))
    print 'dycoms delta_s', delta_s
 

   
  time_real_1=np.zeros(len(time_data_1))
  for i in np.arange(len(time_data_1)):
    time_real_1[i]=round(time_data_1[i]*t_real/60,2)
  time_real_2=np.zeros(len(time_data_2))
  for i in np.arange(len(time_data_2)):
    time_real_2[i]=round(time_data_2[i]*t_real/60,2)
  if (dycoms==0):
    time_real_3=np.zeros(len(time_data_3))
    for i in np.arange(len(time_data_3)):
      time_real_3[i]=round(time_data_3[i]*t_real/60,2)
 
    time_buffer_3=round(time_data_3[plt_ts_3]*t_real/60,2)
    p_title_3     = p_title_part_1+p_title_part_t+str(time_buffer_3)+' [min]'
    print 'real time t3',p_title_3
 
  print 'time data',time_data_1[plt_ts_1], time_data_2[plt_ts_2]
  p_title_1     = p_title_part_1+p_title_part_t+str(time_data_1[plt_ts_1]*t_real/60)
  p_title_2     = p_title_part_1+p_title_part_t+str(time_data_2[plt_ts_2]*t_real/60)
  print 'real time t1 t2', p_title_1, p_title_2
  
#  p_title_1     = p_title_part_1+p_title_part_t+str(time_data_1[plt_ts_1])
#  p_title_2     = p_title_part_1+p_title_part_t+str(time_data_2[plt_ts_2])
#  p_title_3     = p_title_part_1+p_title_part_t+str(time_data_3[plt_ts_3])
#  p_title_2     = p_title_part_2+p_title_part_t+str(plt_ts_2*100+tstart_2)
  save_title_1  = p_title_part_1+'_'+str((plt_ts_1+1)*100)
  save_title_2  = p_title_part_2+'_'+str((plt_ts_2+1)*100)
  ########################################################################
  #Start plotting 
  ########################################################################
  [interval_1, eulerian_1, l_diff_1, l_nodiff_1] = unpolluted_general.read_data(data_path_1, tstart_1, tend_1, tstep_1, nbins)
  [interval_2, eulerian_2, l_diff_2, l_nodiff_2] = unpolluted_general.read_data(data_path_2, tstart_2, tend_2, tstep_2, nbins)
  if (dycoms==0):
    [interval_3, eulerian_3, l_diff_3, l_nodiff_3] = unpolluted_general.read_data(data_path_3, tstart_3, tend_3, tstep_3, nbins)
  else:
    interval_3 =np.zeros([100,100])
    eulerian_3 = np.zeros([100,100])
    l_diff_3 = np.zeros([100,100])
    l_nodiff_3 = np.zeros([100,100])
    time_real_3 = 0  
    #p_title_3 = 'Same resolution t=' + str(round(time_data_1[plt_ts_1]*t_real/60,2))
    p_title_3 = 'test' 
    
  
  interval_4= np.zeros(nbins)
  flight_data= np.zeros(nbins)
  if (dycoms==0):
    data_name=data_path_4 + 'data.txt' 
    interval_4, flight_data = np.loadtxt(data_name, unpack=True) # read file into data:
  
  names_1 = {}
  names_1[1]='Eulerian Re800'
  names_1[2]='Lagrange Re800'
  #names_1[3]='Lagrange no diffusion Re=800'
  names_1[3]=r'$Re_0 800$'
  names_2 = {}
  names_2[1]='Eulerian'
  names_2[2]='Lagrange'
  names_2[3]=r'$Re_0 400$'
  names_3 = {}
  names_3[1]='Eulerian Re=200'
  names_3[2]='Lagrange Re=200'
  names_3[3]=r'$Re_0 200$'
  

  if (several_fits==0):    
    if (several_times==0):    
      if (several_times_and_flight==0):    
        if (compare==1):
          unpolluted_general.plot_data_compare_2(interval_1[:,plt_ts_1], eulerian_1[:,plt_ts_1], l_diff_1[:,plt_ts_1], l_nodiff_1[:,plt_ts_1],
                                        interval_2[:,plt_ts_2], eulerian_2[:,plt_ts_2], l_diff_2[:,plt_ts_2], l_nodiff_2[:,plt_ts_2],
                                        interval_3[:,plt_ts_3], eulerian_3[:,plt_ts_3], l_diff_3[:,plt_ts_3], l_nodiff_3[:,plt_ts_3],
                                        interval_4,flight_data,
                                        names_1, style, p_title_1, names_2, p_title_2,names_3 ,p_title_3, 
                                        dycoms,extrapolation,extrapolation_2, fitting,flight, only_last, s_point )
        else:
          unpolluted_general.extrapolation_sigma(interval_1, l_nodiff_1,
                                        interval_2,l_nodiff_2,
                                        interval_3,l_nodiff_3,
                                        names_1,names_2,names_3,p_title_3,time_real_1, time_real_2, time_real_3,
                                        delta_s,t_real, dycoms,fitting, s_point)
      else:
       unpolluted_general.several_times_and_flight(interval_3,l_nodiff_3,
                                     names_3,p_title_3,time_real_1, time_real_2, time_real_3,
                                     delta_s,t_real,time_data_3, dycoms,fitting, s_point, 
                                      interval_4,flight_data, l_nodiff_3[:,plt_ts_3], interval_3[:,plt_ts_3])
    else: 
  #  unpolluted_general.plot_fitting(interval_3[:,plt_ts_3], eulerian_3[:,plt_ts_3], l_diff_3[:,plt_ts_3], l_nodiff_3[:,plt_ts_3])
  
     if (dycoms==1):
       unpolluted_general.several_times(interval_2,l_nodiff_2,
                                     names_2,p_title_2,time_real_1, time_real_2, time_real_3,
                                     delta_s,t_real,time_data_2, dycoms,fitting, s_point)
     else:
       unpolluted_general.several_times(interval_3,l_nodiff_3,
                                     names_3,p_title_3,time_real_1, time_real_2, time_real_3,
                                     delta_s,t_real,time_data_3, dycoms,fitting, s_point)
  

  if(several_fits == 1):
    if(dycoms==1):
      unpolluted_general.several_fits(interval_2,l_nodiff_2,
                                    names_2,p_title_2,time_real_1, time_real_2, time_real_3,
                                    delta_s,t_real,time_data_2, dycoms,fitting, s_point)
    else:
     unpolluted_general.several_fits(interval_3,l_nodiff_3,
                                   names_3,p_title_3,time_real_1, time_real_2, time_real_3,
                                   delta_s,t_real,time_data_3, dycoms,fitting, s_point)

