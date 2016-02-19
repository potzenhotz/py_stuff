#!/usr/bin/python

import numpy as np

limit = 1000
below_limit = limit-1
n_multiples = 2
multipels = np.zeros(n_multiples)
limit_divide_multipels = np.zeros(n_multiples)
#n_for=2

multipels[0]=3
multipels[1]=5
print ('Used multipels:',multipels)


limit_divide_multipels = np.trunc(below_limit/multipels)
print ("limits of division",limit_divide_multipels)
sum_of_multiples=np.zeros(np.sum(limit_divide_multipels))
j=0
for i in range(1,int(limit_divide_multipels[0]+1)):  #range geht nur bis n
  sum_of_multiples[j]=multipels[0]*i
  j=j+1
 
for i in range(1,int(limit_divide_multipels[1])+1):  #range geht nur bis n
  sum_of_multiples[j]=multipels[1]*i
  j=j+1

#set is used to remove duplicates
result_sum_of_multiples = sum(set(sum_of_multiples))

print (result_sum_of_multiples)
print (type(multipels))

