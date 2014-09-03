
import matplotlib.pyplot as plt
import numpy as np
from random import randrange
from random import randint
#import sciphy.stats as ss

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#create random normal distribution
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#idea1 put longer sampling
#idea2 distribute drunken guys over a certain region


resolution=10000
mu, sigma = 0, 1 # mean and standard deviation
s = np.random.normal(mu, sigma, resolution)

n_drunken_guys = 100000.0
walking_time = 1000.0
drunken_guy = np.zeros(n_drunken_guys)
health = np.zeros(n_drunken_guys)


for j in np.arange(n_drunken_guys):
  left_right=randrange(-100,101,1)
  drunken_guy[j]=left_right

on=1
if (on == 1):  
  for j in np.arange(n_drunken_guys):
    for i in np.arange(walking_time):
      #left_right=randrange(-1,2,2)
      rnd_number=randint(0,resolution-1)
      #print rnd_number
      #drunken_guy[j]=left_right*s[rnd_number]
      drunken_guy[j]=drunken_guy[j] + s[rnd_number]
      if (drunken_guy[j] < 10 and drunken_guy[j] > (-10)):
        health[j]=health[j]+1

print drunken_guy[5]
print health[5]
print np.std(drunken_guy)
health=health/walking_time


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#PLOT
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if (on == 1):  
  #plt.hist(drunken_guy,30)
  #plt.hist(health,50)
  
  n, bins, rest= plt.hist(health,50)
  plt.clf()
  
  bins_2=np.zeros(len(n))
  for i in np.arange(len(n)):
    bins_2[i] = bins[i]

  n=n/n_drunken_guys
  
  plt.bar(bins_2,n, width=bins_2[1]-bins[0])
  #plt.plot(bins_2,n)
  #plt.xlim(0,1)


#count, bins, ignored = plt.hist(s, 50, normed=True)
#plt.plot(bins, 1/(sigma * np.sqrt(2 * np.pi)) *np.exp( - (bins - mu)**2 / (2 * sigma**2) ),
#         linewidth=2, color='r')
plt.show()

