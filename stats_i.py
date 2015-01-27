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
import stats2nc

#print 'Number of arguments:', len(sys.argv), 'arguments.'
#print 'Argument List:', str(sys.argv)


# specify the time steps and the number of grid points
#try:
#    path_chi = str(sys.argv[1])
#except Exception:
#    print 'Give a path to the avg*.gz files'
#    sys.exit()
path_chi = '/home/zmaw/u300202/python/plot_test'  

#std values
tstart = 100
tend   = 700
tstep  = 100
jmax   = 512

#input
def check():
    global tstart, tstep, tend, jmax
    q=raw_input('Do ['+str(tstart)+':'+str(tstep)+':'+str(tend)+'] for jmax='+str(jmax)+' ? [Y/n]')
    if(q=='n' or q=='N'):
        tstart=int(raw_input('Start at: '))
        tend  =int(raw_input('End at  : '))
        tstep =int(raw_input('Steps   : '))
        jmax  =int(raw_input('jmax    : '))
        check()
    return

check()

print 'Doing '+str(tstart)+':'+str(tstep)+':'+str(tend)+'] for jmax='+str(jmax)+' !'
[avg, avg1s, avg3s, avg4s, avg5s, avg6s] = stats2nc.avg2dict(path_chi, tstart, tend, tstep, jmax)
stats2nc.dict2nc(avg,   "avg")
stats2nc.dict2nc(avg1s, "avg1s")
stats2nc.dict2nc(avg3s, "avg3s")
stats2nc.dict2nc(avg4s, "avg4s")
stats2nc.dict2nc(avg5s, "avg5s")
stats2nc.dict2nc(avg6s, "avg6s")

del(avg, avg1s, avg3s, avg4s, avg5s, avg6s)
