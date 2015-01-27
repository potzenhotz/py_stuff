#!/usr/bin/python

import numpy
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
from scipy.stats import norm

fname='test.txt'  #name of file

data = numpy.loadtxt(fname) # read file into data

mylist = numpy.arange(0,1.1,0.1)  # create list for xlim

mu = numpy.mean(data) #mean of data
sigma = numpy.std(data) # standard deviation of data

#(mu, sigma)= norm.fit(data)

n_bins=30 # how many bins


n, bins, patches = plt.hist(data,n_bins, normed=0, facecolor='green', alpha=0.8)
#normed still not understood
#alpha value is opacity of color

n_mu = numpy.mean(n) #mean of data
n_sigma = numpy.std(n) # standard deviation of data
y = mlab.normpdf(bins,mu,sigma)  # fitted line



plt.plot(bins)#,n,'r--')  # if fitted line should be visible
plt.xlim(0,1)
plt.xticks(mylist)
plt.xlabel('Y Direction', fontsize=20)
plt.ylabel('Amount of Particles', fontsize=20)


#plt.subplots_adjust(left=0.15)
plt.show()
