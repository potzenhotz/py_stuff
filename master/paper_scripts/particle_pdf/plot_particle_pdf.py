#!/usr/bin/python2.7

import sys
import numpy as np
import functions_for_plot
import matplotlib.pyplot as plt
from matplotlib import rcParams

########################################################################
#Which plot should be produced
########################################################################
compare=0 # =1 if u want to compare different Re numbers

########################################################################
#Setup data path
########################################################################
data_path_1 = 'data_ar_re800_general/'  
data_path_2 = 'data_ar_re400_stretch_general/'  
if (compare==1):
  data_path_3 = 'data_ar_re200_stretch_general/'  
else:
  data_path_3 = 'data_ar_re200_stretch_general_strat/'  
data_path_4= 'flight_data/'


########################################################################
#Setup global values
########################################################################
tstart_1  = 100
tend_1    = 3100 #Arctic
tstep_1   = 100

tstart_2  = 100   
tend_2    = 3600 
tstep_2   = 100
  
tstart_3  = 100
if (compare==1):
  tend_3    = 3600
else:
  tend_3    = 18900
tstep_3   = 100

nbins   = 100
style   = 0

#time step for comparison of Re numbers
plt_ts_1        = 2900  #Re800
plt_ts_2        = 1700  #Re400
plt_ts_3        = 900   #Re200

plt_ts_1=(plt_ts_1-tstart_1)/tstep_1 
plt_ts_2=(plt_ts_2-tstart_2)/tstep_2 
plt_ts_3=(plt_ts_3-tstart_3)/tstep_3 

print plt_ts_1, plt_ts_2 

p_title_part_1  = 'VERDI'
p_title_part_t  = ' - Time: '



time_data_1=np.zeros(100)
time_data_2=np.zeros(100)
time_data_3=np.zeros(300)
time_data_1 = functions_for_plot.read_timedata(data_path_1, time_data_1)
time_data_2 = functions_for_plot.read_timedata(data_path_2, time_data_2)
time_data_3 = functions_for_plot.read_timedata(data_path_3, time_data_3)
print 'Length of time_data_3', len(time_data_3)


########################################################################
#Calculate real time
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

Ri=1/0.0351
D=-0.11
chi_s=0.2
C_2=0.29
delta_s=(Ri*(D+chi_s))/(C_2*(1-chi_s))
print 'verdi delta_s', delta_s


time_real_1=np.zeros(len(time_data_1))
for i in np.arange(len(time_data_1)):
  time_real_1[i]=round(time_data_1[i]*t_real/60,2)
time_real_2=np.zeros(len(time_data_2))
for i in np.arange(len(time_data_2)):
  time_real_2[i]=round(time_data_2[i]*t_real/60,2)
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



########################################################################
#Start plotting 
########################################################################
[interval_1, eulerian_1, l_diff_1, l_nodiff_1] = functions_for_plot.read_data(data_path_1, tstart_1, tend_1, tstep_1, nbins)
[interval_2, eulerian_2, l_diff_2, l_nodiff_2] = functions_for_plot.read_data(data_path_2, tstart_2, tend_2, tstep_2, nbins)
[interval_3, eulerian_3, l_diff_3, l_nodiff_3] = functions_for_plot.read_data(data_path_3, tstart_3, tend_3, tstep_3, nbins)


interval_4= np.zeros(nbins)
flight_data= np.zeros(nbins)
data_name=data_path_4 + 'data.txt' 
interval_4, flight_data = np.loadtxt(data_name, unpack=True) # read file into data:
data_name=data_path_4 + 'data_4s.txt' 
interval_4_2, flight_data_2 , flight_err_2= np.loadtxt(data_name, unpack=True) # read file into data:

names_1 = {}
names_1[1]='Eulerian Re800'
names_1[2]='Lagrange Re800'
names_1[3]=r'$Re_0 800$'
names_2 = {}
names_2[1]='Eulerian'
names_2[2]='Lagrange'
names_2[3]=r'$Re_0 400$'
names_3 = {}
names_3[1]='Eulerian Re=200'
names_3[2]='Lagrange Re=200'
names_3[3]=r'$Re_0 200$'


if (compare==1):
  functions_for_plot.plot_data_compare(interval_1[:,plt_ts_1], eulerian_1[:,plt_ts_1], l_diff_1[:,plt_ts_1], l_nodiff_1[:,plt_ts_1],
                              interval_2[:,plt_ts_2], eulerian_2[:,plt_ts_2], l_diff_2[:,plt_ts_2], l_nodiff_2[:,plt_ts_2],
                              interval_3[:,plt_ts_3], eulerian_3[:,plt_ts_3], l_diff_3[:,plt_ts_3], l_nodiff_3[:,plt_ts_3],
                              names_1, names_2,names_3)
else:
  functions_for_plot.several_times_and_flight(interval_3,l_nodiff_3,
                            t_real,time_data_3,  
                            interval_4,flight_data,interval_4_2, flight_data_2,flight_err_2,
                            l_nodiff_3[:,plt_ts_3], interval_3[:,plt_ts_3])

