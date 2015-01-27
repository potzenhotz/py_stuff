# script to process DNS statistics
# Chiel van Heerwaarden, 2011

import stats2nc

# specify the time steps and the number of grid points
path_hom = '/home/zmaw/u300202/python/plot_test'

tstart = 100
tend   = 700
tstep  = 100
jmax   = 512

[avg, avg1s] = stats2nc.avg2dict(path_hom, tstart, tend, tstep, jmax)
stats2nc.dict2nc(avg,   "avg_hom_hires")
stats2nc.dict2nc(avg1s, "avg1s_hom_hires")
del(avg, avg1s)

#[avg, avg1s] = stats2nc.avg2dict(path_het2, tstart, tend, tstep, jmax)
#stats2nc.dict2nc(avg,   "avg_het2")
#stats2nc.dict2nc(avg1s, "avg1s_het2")
#del(avg, avg1s)
#

