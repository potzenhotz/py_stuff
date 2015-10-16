#!/usr/bin/python

import numpy as np
from math import sqrt; from itertools import count, islice
import progressbar 
import time
progress = progressbar.ProgressBar()

def isPrime(n):
    if n < 2: return False
    return all(n%i for i in islice(count(2), int(sqrt(n)-1)))

var=600851475143
#print type(var)
#for i in np.arange(var)+1:
for i in progress(xrange(1,var)):
  if (var % i == 0 ):
    #print i
    if (isPrime(i) == True):
      print "######################",i

