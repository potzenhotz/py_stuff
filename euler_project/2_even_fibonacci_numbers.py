#!/usr/bin/python

import numpy as np


n=1
n_plus=2
n_plusplus=0
i=1
while n_plusplus < 4000000:
  n_plusplus=n_plus+n
  n=n_plus
  n_plus=n_plusplus
  i=i+1

n=1
n_plus=2
fib_numbers = np.zeros(i-2)
for j in np.arange(i-2):
  fib_numbers[j]=n_plus+n 
  n=n_plus
  n_plus=fib_numbers[j]

even_fib_numbers=np.zeros(len(fib_numbers))
even_fib_numbers[0]=2
j=1
for i in np.arange(len(fib_numbers)):
  if (fib_numbers[i] % 2 == 0):
    print 'even valued terms:', fib_numbers[i]
    even_fib_numbers[j]=fib_numbers[i]
    j=j+1

print sum(even_fib_numbers)

