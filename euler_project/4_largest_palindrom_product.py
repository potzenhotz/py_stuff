#!/usr/bin/python

import numpy as np
import progressbar

progress=progressbar.ProgressBar()

def palindrome(num):
    return str(num) == str(num)[::-1]
product_old=np.zeros(1)

for i in progress(xrange(100,999)):
  for j in xrange(100,999):
    product=i*j
    if (palindrome(product) == True):
      if (product > product_old):
        product_old=product
      
print product_old
