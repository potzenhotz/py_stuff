
import gzip
import netCDF4
from pylab import *



def avg2dict(avgpath, tstart, tend, tstep, jmax):
  print(avgpath, tstart, tend, tstep, jmax)

  # specify the number of vertical profs and time variables
  headerprof = 199
  headertime = 14

  
  # specify the length of the header
  headerlength    = 21
 
  ###########################################################
  
  ntimes = (tend - tstart) / tstep + 1
  headertotal    = headerprof    + headertime

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
 
  return (hist)
