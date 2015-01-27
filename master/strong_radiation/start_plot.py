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
import general_plot
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

#data_path = '/home/zmaw/u300202/python/master/data_ar_re800/'  
#data_path = '/home/zmaw/u300202/python/master/data_ar_re400_stretch/'  
data_path = '/home/zmaw/u300202/python/master/data_ar_re200_stretch/'  

#data_path = '/home/zmaw/u300202/python/master/data_dy_re800/'  
#data_path = '/home/zmaw/u300202/python/master/data_dy_re400_stretch/'  

########################################################################
#Setup global values
########################################################################
tstart  = 100
tend    = 3600
tstep   = 100
nbins   = 100
style   = 0

plt_ts        = 3600 #plot_timestep
#p_title_part  = 'ARCTIC Re=800'
p_title_part  = 'ARCTIC Re=200'
#p_title_part  = 'ARCTIC Re=400 '
p_title_part_2  = ' timestep='
p_title       = p_title_part+p_title_part_2+str((plt_ts+1)*100)

plot_type=0

def check_general():
    global plot_type 
    print 'Plot type=0 displays certain timestep'
    print 'Plot type=1 displays the liquid groth in time'
    print 'Plot type=2 displays multiple timesteps'
    print 'Plot type=3 saves plots '
    q=raw_input('Plot type='+str(plot_type)+' ? [Y/n]')
    if(q=='n' or q=='N'):
        plot_type=int(raw_input('Plot type : '))
        check_general()
    return
check_general()

time_data=np.zeros(100)
time_data = general_plot.read_timedata(data_path, time_data)

if (plot_type == 0):
  
  ########################################################################
  #Check all global variables 
  ########################################################################
  def check():
      global tstart, tstep, tend, nbins
      q=raw_input('Do ['+str(tstart)+':'+str(tstep)+':'+str(tend)+'] with nbins=' +str(nbins)+' ? [Y/n]')
      if(q=='n' or q=='N'):
          tstart=int(raw_input('Start at: '))
          tend  =int(raw_input('End at  : '))
          tstep =int(raw_input('Steps   : '))
          nbins =int(raw_input('Number of bins   : '))
          check()
      return
  check()
  
  def check_style():
      global  style
      print 'Style=0 displays a line plot!'
      print 'Style=1 displays a bar plot!'
      q=raw_input('Stylo mylo = '+str(style)+' ? [Y/n]')
      if(q=='n' or q=='N'):
          style =int(raw_input('Which style   : '))
          check_style()
      return
  check_style()
  
  def check_plt_ts():
      global  plt_ts, tstart, tstep
      q=raw_input('Plot timestep (first is 0) = '+str(plt_ts)+' ? [Y/n]')
      if(q=='n' or q=='N'):
          plt_ts =int(raw_input('Which timestep should we plot (first is 0) : '))
          check_plt_ts()
      return
  check_plt_ts()
  plt_ts=(plt_ts-tstart)/tstep
  
  def check_p_title_part():
      global  p_title_part
      q=raw_input('Title of the plot = '+str(p_title_part)+' ? [Y/n]')
      if(q=='n' or q=='N'):
          p_title_part =str(raw_input('Which title you favour my Highness: '))
          check_p_title_part()
      return
  check_p_title_part()
  p_title     = p_title_part+p_title_part_2+str(plt_ts*100+tstart)
  save_title  = p_title_part+'_'+str((plt_ts+1)*100)
  
  ########################################################################
  #Start plotting 
  ########################################################################
  print 'Doing ['+str(tstart)+':'+str(tstep)+':'+str(tend)+'] with nbins='+str(nbins)+' !'
  print 'Followed by style='+str(style)+' and plot timestep='+str(plt_ts)+' !'
  [interval, eulerian, l_diff, l_nodiff] = general_plot.read_data(data_path, tstart, tend, tstep, nbins)
  
  names = {}
  names[1]='Liquid'
  names[2]='l_diff'
  names[3]='l_nodiff'
  general_plot.plot_data(interval[:,plt_ts], eulerian[:,plt_ts], l_diff[:,plt_ts], l_nodiff[:,plt_ts], 
                           names, style, p_title)


elif(plot_type == 1):

  
  ########################################################################
  #Growth in time plot
  ########################################################################
  def check():
     global tstart, tstep, tend, nbins
     q=raw_input('Do ['+str(tstart)+':'+str(tstep)+':'+str(tend)+'] with nbins=' +str(nbins)+' ? [Y/n]')
     if(q=='n' or q=='N'):
         tstart=int(raw_input('Start at: '))
         tend  =int(raw_input('End at  : '))
         tstep =int(raw_input('Steps   : '))
         nbins =int(raw_input('Number of bins   : '))
         check()
     return
  check()
  
  names = {}
  names[1]='Liquid'
  names[2]='l_diff'
  names[3]='l_nodiff'
 
  [interval, eulerian, l_diff, l_nodiff] = general_plot.read_data(data_path, tstart, tend, tstep, nbins)
  
  general_plot.plot_data_time(interval[:,:], eulerian[:,:], l_diff[:,:], l_nodiff[:,:], 
                           names, style, nbins, tstart, tend, tstep, p_title_part, time_data)


elif(plot_type == 2):

  
  ########################################################################
  #Multiple plots
  ########################################################################
  def check():
     global tstart, tstep, tend, nbins
     q=raw_input('Do ['+str(tstart)+':'+str(tstep)+':'+str(tend)+'] with nbins=' +str(nbins)+' ? [Y/n]')
     if(q=='n' or q=='N'):
         tstart=int(raw_input('Start at: '))
         tend  =int(raw_input('End at  : '))
         tstep =int(raw_input('Steps   : '))
         nbins =int(raw_input('Number of bins   : '))
         check()
     return
  check()
  
  names = {}
  names[1]='Liquid'
  names[2]='l_diff'
  names[3]='l_nodiff'
 
  [interval, eulerian, l_diff, l_nodiff] = general_plot.read_data(data_path, tstart, tend, tstep, nbins)
  
  general_plot.plot_data_several(interval[:,:], eulerian[:,:], l_diff[:,:], l_nodiff[:,:], 
                           names, style, nbins, tstart, tend, tstep, p_title)




elif(plot_type == 3):

  ########################################################################
  #Save plot
  ########################################################################
  def check():
    global tstart, tstep, tend, nbins
    q=raw_input('Do ['+str(tstart)+':'+str(tstep)+':'+str(tend)+'] with nbins=' +str(nbins)+' ? [Y/n]')
    if(q=='n' or q=='N'):
        tstart=int(raw_input('Start at: '))
        tend  =int(raw_input('End at  : '))
        tstep =int(raw_input('Steps   : '))
        nbins =int(raw_input('Number of bins   : '))
        check()
    return
  check()
  
  names = {}
  names[1]='Liquid'
  names[2]='l_diff'
  names[3]='l_nodiff'
 
  [interval, eulerian, l_diff, l_nodiff] = general_plot.read_data(data_path, tstart, tend, tstep, nbins)

  
  save_start  = tstart
  save_end    = tend
  
  def check_save_plt():
      global  save_start, save_end
      q=raw_input('Do '+str(save_start)+':'+str(save_end)+ ' ? [Y/n]')
      if(q=='n' or q=='N'):
          save_start =int(raw_input('Start of save : '))
          save_end =int(raw_input('End of save : '))
          check_save_plt()
      return
  check_save_plt()
  
  format='png'
   
  ntimes=(save_end-save_start)/100+1
  for i in np.arange(ntimes): 
    plt_ts=i
    save_title  = p_title_part+'_'+str(plt_ts*100+tstart)
    p_title  = p_title_part+' timestep='+str(time_data[i])
    close='all'
    general_plot.save_plot_data(interval[:,plt_ts], eulerian[:,plt_ts], l_diff[:,plt_ts], l_nodiff[:,plt_ts],\
                           names, style, p_title, save_title, format)
  
  
  




del(interval, eulerian, l_diff, l_nodiff)
