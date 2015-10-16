#!/usr/bin/python

import numpy as np
from math import sqrt; from itertools import count, islice

def isPrime(n):
    if n < 2: return False
    return all(n%i for i in islice(count(2), int(sqrt(n)-1)))

print isPrime(4)
var=600851475143
var=600851475
for i in np.arange(var)+1:
  if (var % i == 0 ):
#    if (isPrime(i) == True):
    print i
