#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

fname='data/particle_pdf.1000'  #name of file

interval,eulerian,l_diff, l_nodiff = np.loadtxt(fname, unpack=True) # read file into data


print interval
print l_nodiff

width = 0.05
opacity=0.5


p1 = plt.plot(interval,np.log10( eulerian), color='black')
p2 = plt.plot(interval,np.log10( l_diff), color='r')
p2 = plt.plot(interval,np.log10( l_nodiff), color='green')
#plt.legend( (p1[0], p2[0]), ('diff', 'nodiff'))
plt.xlim(min(interval)+1.1, max(interval))

plt.show()
