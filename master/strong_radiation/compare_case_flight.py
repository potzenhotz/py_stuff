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
import general_plot_flight as general_plot
import matplotlib.pyplot as plt

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)


# specify the time steps and the number of grid points
#try:
#    path_chi = str(sys.argv[1])
#except Exception:
#    print 'Give a path to the avg*.gz files'
#    sys.exit()
########################################################################
#Setup data path
########################################################################
data_path_1 = '/home/zmaw/u300202/python/master/data_ar_re800/'  
#data_path_2 = '/home/zmaw/u300202/python/master/data_ar_re400_stretch/'  
data_path_2 = '/home/zmaw/u300202/python/master/data_ar_re200_stretch/'  
data_path_2 = '/home/zmaw/u300202/python/master/data_ar_re200_stretch_rescale3/'  

#data_path_1 = '/home/zmaw/u300202/python/master/data_dy_re800/'  
#data_path_2 = '/home/zmaw/u300202/python/master/data_dy_re400/'  
#data_path_2 = '/home/zmaw/u300202/python/master/data_dy_re400_stretch/'  

data_path_3= '/home/zmaw/u300202/python/master/flight_data/'

########################################################################
#Setup global values
########################################################################
tstart_1  = 300
tend_1    = 3100
tstep_1   = 100

tstart_2  = 300
tend_2    = 3600
tstep_2   = 100


nbins   = 100
style   = 0

plt_ts_1        = 3000 #plot_timestep
plt_ts_2        = 3600 #plot_timestep
plt_ts_1=(plt_ts_1-tstart_1)/tstep_1 
plt_ts_2=(plt_ts_2-tstart_2)/tstep_2 

p_title_part_1  = 'ARCTIC'
#p_title_part_1  = 'DYCOMS_II'
#p_title_part_2  = 'ARCTIC Re=400'
p_title_part_2  = 'DYCOMS_II Re=400'
p_title_part_t  = ' Time='

p_title_1 = p_title_part_1+p_title_part_t+str((plt_ts_1+1)*100)
p_title_2 = p_title_part_2+p_title_part_t+str((plt_ts_2+1)*100)

plot_type=0


time_data_1=np.zeros(100)
time_data_2=np.zeros(100)
time_data_1 = general_plot.read_timedata(data_path_1, time_data_1)
time_data_2 = general_plot.read_timedata(data_path_2, time_data_2)

if (plot_type == 0):
  

  p_title_1     = p_title_part_1+p_title_part_t+str(time_data_1[plt_ts_1])
#  p_title_2     = p_title_part_2+p_title_part_t+str(plt_ts_2*100+tstart_2)
  save_title_1  = p_title_part_1+'_'+str((plt_ts_1+1)*100)
  save_title_2  = p_title_part_2+'_'+str((plt_ts_2+1)*100)
  ########################################################################
  #Start plotting 
  ########################################################################
  [interval_1, eulerian_1, l_diff_1, l_nodiff_1] = general_plot.read_data(data_path_1, tstart_1, tend_1, tstep_1, nbins)
  [interval_2, eulerian_2, l_diff_2, l_nodiff_2] = general_plot.read_data(data_path_2, tstart_2, tend_2, tstep_2, nbins)
 
   
  interval_3= np.zeros(nbins)
  flight_data= np.zeros(nbins)
  data_name=data_path_3 + 'data.txt' 
  interval_3, flight_data = np.loadtxt(data_name, unpack=True) # read file into data:
 
  names_1 = {}
  names_1[1]='Liquid Re=800'
  names_1[2]='l_diff Re=800'
  names_1[3]='l_nodiff Re=800'
  names_2 = {}
  names_2[1]='Liquid Re=400'
  names_2[2]='l_diff Re=400'
  names_2[3]='l_nodiff Re=400'

#  general_plot.plot_data_compare(interval_1[:,plt_ts_1], eulerian_1[:,plt_ts_1], l_diff_1[:,plt_ts_1], l_nodiff_1[:,plt_ts_1]\
#                                  , interval_2[:,plt_ts_2], eulerian_2[:,plt_ts_2], l_diff_2[:,plt_ts_2], l_nodiff_2[:,plt_ts_2]\
#                                 ,names_1, style, p_title_1, names_2, p_title_2)



  general_plot.plot_data_compare_2(interval_1[:,plt_ts_1], eulerian_1[:,plt_ts_1], l_diff_1[:,plt_ts_1], l_nodiff_1[:,plt_ts_1]\
                                  , interval_2[:,plt_ts_2], eulerian_2[:,plt_ts_2], l_diff_2[:,plt_ts_2], l_nodiff_2[:,plt_ts_2]\
                                  ,names_1, style, p_title_1, names_2, p_title_2, interval_3,flight_data)




