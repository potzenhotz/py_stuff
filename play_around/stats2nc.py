##
# read statistics from ASCII files and put them in netCDF
# Chiel van Heerwaarden, 2012
##
# Added avg4s statistics, Thomas Keitzl, 2013
##

import gzip
import netCDF4
from pylab import *

def avg2dict(avgpath, tstart, tend, tstep, jmax):
  print(avgpath, tstart, tend, tstep, jmax)

  # specify the number of vertical profs and time variables
  headerprof = 199
  headertime = 14
  headerprof_1s = 35
  headertime_1s = 9 
  headerprof_3s = 35
  headertime_3s = 9 
  headerprof_4s = 35
  headertime_4s = 9 
  headerprof_5s = 39
  headertime_5s = 9 
  headerprof_6s = 39
  headertime_6s = 9 
  
  # specify the length of the header
  headerlength    = 21
  headerlength_1s = 8
  headerlength_3s = 8
  headerlength_4s = 8
  headerlength_5s = 8
  headerlength_6s = 8
  
  ###########################################################
  
  ntimes = (tend - tstart) / tstep + 1
  headertotal    = headerprof    + headertime
  headertotal_1s = headerprof_1s + headertime_1s
  headertotal_3s = headerprof_3s + headertime_3s
  headertotal_4s = headerprof_4s + headertime_4s
  headertotal_5s = headerprof_5s + headertime_5s
  headertotal_6s = headerprof_6s + headertime_6s
 
  for t in range(ntimes):
    filenum = tstart + t*tstep
  
    # first, process the avg file
    f = gzip.open('{}/avg{}.gz'.format(avgpath,filenum),'r')
   
    # retrieve the physical time
    datastring = f.readline()
    time = datastring.split()[2]
    print('Time avg   = ', time, filenum)
  
    # process the groups items in the header
    for i in range(headerlength-2):
      dummy = f.readline()
   
    # read the variable labels
    datastring = f.readline()
    if(filenum == tstart):
      header = datastring.split()
  
      avg = {}
  
      avg['Time'] = zeros(ntimes)
      for n in range(headerprof):
        avg[header[n]] = zeros((ntimes, jmax))
      for n in range(headerprof, headertotal):
        avg[header[n]] = zeros(ntimes)
  
    # process the data
    # first store the time
    avg['Time'][t] = time
  
    for i in range(jmax):
      datastring = f.readline()
      data = datastring.split()
  
      # process the vertical profiles
      for n in range(headerprof):
        avg[header[n]][t,i] = data[n]
  
      # process the time series
      if(len(data) == headertotal):
        for n in range(headerprof, headertotal):
          avg[header[n]][t] = data[n]
  
    f.close()
  
    ########################################################
    # second, process the avg1s file
    f = gzip.open('{}/avg1s{}.gz'.format(avgpath,filenum),'r')
   
    # retrieve the physical time
    datastring = f.readline()
    time = datastring.split()[2]
    print('Time avg1s = ', time, filenum)
  
    # process the groups items in the header
    for i in range(headerlength_1s-2):
      dummy = f.readline()
   
    # read the variable labels
    datastring = f.readline()
    if(filenum == tstart):
      header_1s = datastring.split()
  
      avg1s = {}
  
      avg1s['Time'] = zeros(ntimes)
      for n in range(headerprof_1s):
        avg1s[header_1s[n]] = zeros((ntimes, jmax))
      for n in range(headerprof_1s, headertotal_1s):
        avg1s[header_1s[n]] = zeros(ntimes)
  
    # process the data
    # first store the time
    avg1s['Time'][t] = time
  
    for i in range(jmax):
      datastring = f.readline()
      data = datastring.split()
  
      # process the vertical profiles
      for n in range(headerprof_1s):
        avg1s[header_1s[n]][t,i] = data[n]
  
      # process the time series
      if(len(data) == headertotal_1s):
        for n in range(headerprof_1s, headertotal_1s):
          avg1s[header_1s[n]][t] = data[n]
  
    f.close()

    ########################################################
    # second, process the avg3s file
    f = gzip.open('{}/avg3s{}.gz'.format(avgpath,filenum),'r')
   
    # retrieve the physical time
    datastring = f.readline()
    time = datastring.split()[2]
    print('Time avg3s = ', time, filenum)
  
    # process the groups items in the header
    for i in range(headerlength_3s-2):
      dummy = f.readline()
   
    # read the variable labels
    datastring = f.readline()
    if(filenum == tstart):
      header_3s = datastring.split()
  
      avg3s = {}
  
      avg3s['Time'] = zeros(ntimes)
      for n in range(headerprof_3s):
        avg3s[header_3s[n]] = zeros((ntimes, jmax))
      for n in range(headerprof_3s, headertotal_3s):
        avg3s[header_3s[n]] = zeros(ntimes)
  
    # process the data
    # first store the time
    avg3s['Time'][t] = time
  
    for i in range(jmax):
      datastring = f.readline()
      data = datastring.split()
  
      # process the vertical profiles
      for n in range(headerprof_3s):
        avg3s[header_3s[n]][t,i] = data[n]
  
      # process the time series
      if(len(data) == headertotal_3s):
        for n in range(headerprof_3s, headertotal_3s):
          avg3s[header_3s[n]][t] = data[n]
  
    f.close()


    ########################################################
    # third, process the avg4s file
    f = gzip.open('{}/avg4s{}.gz'.format(avgpath,filenum),'r')
   
    # retrieve the physical time
    datastring = f.readline()
    time = datastring.split()[2]
    print('Time avg4s = ', time, filenum)
  
    # process the groups items in the header
    for i in range(headerlength_4s-2):
      dummy = f.readline()
   
    # read the variable labels
    datastring = f.readline()
    if(filenum == tstart):
      header_4s = datastring.split()
      avg4s = {}
  
      avg4s['Time'] = zeros(ntimes)
      for n in range(headerprof_4s):
        avg4s[header_4s[n]] = zeros((ntimes, jmax))
      for n in range(headerprof_4s, headertotal_4s):
        avg4s[header_4s[n]] = zeros(ntimes)
  
    # process the data
    # first store the time
    avg4s['Time'][t] = time
 

    for i in range(jmax+1):  #jmax+1 due to single line of alberto
      datastring = f.readline()
      data = datastring.split()
#      print len(data)
       
      if (i < 256): 
        # process the vertical profiles
        for n in range(headerprof_4s):
#          print 'here1',n, i, t
          avg4s[header_4s[n]][t,i] = data[n]
    
        # process the time series
        if(len(data) == headertotal_4s):
#          print 'here11',n, i 
          for n in range(headerprof_4s, headertotal_4s):
            avg4s[header_4s[n]][t] = data[n]
      elif (i ==256):
        print 'hallo'
      elif( i > 256):
        i=i-1
        # process the vertical profiles
        for n in range(headerprof_4s):
#          print 'here2',n, i 
          avg4s[header_4s[n]][t,i] = data[n]
    
        # process the time series
        if(len(data) == headertotal_4s):
          for n in range(headerprof_4s, headertotal_4s):
#            print 'here22',n, i, t
            avg4s[header_4s[n]][t] = data[n]
#        i=i+1 

    f.close()

    ########################################################
    # fourth, process the avgr5s file
    f = gzip.open('{}/avg5s{}.gz'.format(avgpath,filenum),'r')
   
    # retrieve the physical time
    datastring = f.readline()
    time = datastring.split()[2]
    print('Time avg5s = ', time, filenum)
  
    # process the groups items in the header
    for i in range(headerlength_5s-2):
      dummy = f.readline()
   
    # read the variable labels
    datastring = f.readline()
    if(filenum == tstart):
      header_5s = datastring.split()
  
      avg5s = {}
  
      avg5s['Time'] = zeros(ntimes)
      for n in range(headerprof_5s):
        avg5s[header_5s[n]] = zeros((ntimes, jmax))
      for n in range(headerprof_5s, headertotal_5s):
        avg5s[header_5s[n]] = zeros(ntimes)
  
    # process the data
    # first store the time
    avg5s['Time'][t] = time
  
    for i in range(jmax):
      datastring = f.readline()
      data = datastring.split()
  
      # process the vertical profiles
      for n in range(headerprof_5s):
        avg5s[header_5s[n]][t,i] = data[n]
  
      # process the time series
      if(len(data) == headertotal_5s):
        for n in range(headerprof_5s, headertotal_5s):
          avg5s[header_5s[n]][t] = data[n]
  
    f.close()

    ########################################################
    # fourth, process the avgr6s file
    f = gzip.open('{}/avg6s{}.gz'.format(avgpath,filenum),'r')
   
    # retrieve the physical time
    datastring = f.readline()
    time = datastring.split()[2]
    print('Time avg6s = ', time, filenum)
  
    # process the groups items in the header
    for i in range(headerlength_6s-2):
      dummy = f.readline()
   
    # read the variable labels
    datastring = f.readline()
    if(filenum == tstart):
      header_6s = datastring.split()
  
      avg6s = {}
  
      avg6s['Time'] = zeros(ntimes)
      for n in range(headerprof_6s):
        avg6s[header_6s[n]] = zeros((ntimes, jmax))
      for n in range(headerprof_6s, headertotal_6s):
        avg6s[header_6s[n]] = zeros(ntimes)
  
    # process the data
    # first store the time
    avg6s['Time'][t] = time
  
    for i in range(jmax):
      datastring = f.readline()
      data = datastring.split()
  
      # process the vertical profiles
      for n in range(headerprof_6s):
        avg6s[header_6s[n]][t,i] = data[n]
  
      # process the time series
      if(len(data) == headertotal_6s):
        for n in range(headerprof_6s, headertotal_6s):
          avg6s[header_6s[n]][t] = data[n]
  
    f.close()




  return (avg, avg1s, avg3s, avg4s, avg5s, avg6s)

#############################################################

def dict2nc(dict, ncname, flag=0):
  # process the dictionaries to netcdf files
  avgnc  = netCDF4.Dataset("{}.nc".format(ncname), "w")

  # retrieve dimensions
  time   = dict["Time"]
  ntimes = time.shape[0]

  y    = dict["Y"]
  jmax = y.shape[1]

  print("Creating netCDF file with ntimes = {} and jmax = {}".format(ntimes, jmax))
  
  # create dimensions in netCDF file
  dim_y = avgnc.createDimension('y', jmax)
  dim_t = avgnc.createDimension('t', ntimes)
  
  # create variables
  var_t = avgnc.createVariable('t','f8',('t',))
  var_y = avgnc.createVariable('y','f8',('y',))

  # store the data
  # first, handle the dimensions
  var_t[:] = dict['Time'][:]
  var_y[:] = dict['Y']   [0,:]

  # now make a loop through all vars.
  dictkeys = dict.keys()

  for i in range(size(dictkeys)):
    varname = dictkeys[i]
    if(not((varname == "Y") or (varname == "Time") or (varname == "I") or (varname == "J"))):
      vardata = dict[varname]
      if(len(vardata.shape) == 2):
        if( (vardata.shape[0] == ntimes) and (vardata.shape[1] == jmax) ):
          print("Storing {} in 2D (t,y) array".format(varname))
          var_name = avgnc.createVariable(varname,'f8',('t','y',))
          var_name[:,:] = vardata
      if(len(vardata.shape) == 1):
        if(vardata.shape[0] == ntimes):
          print("Storing {} in 1D (t) array".format(varname))
          var_name = avgnc.createVariable(varname,'f8',('t',))
          var_name[:] = vardata

  # close the file
  avgnc.close()

