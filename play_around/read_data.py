#read data

import numpy as np

flocation ='data'
fname = 'avg100'
fentire = flocation + '/' + fname

file = open(fentire,'r')




for i, line in enumerate(file):
  if i==20:
    header_raw=line

file.close()

header_raw=header_raw.strip()

header=header_raw.split()

data_raw=np.loadtxt('data/avg100', skiprows=21)

for i in range(0,data_raw.shape[1]):
  vars()[header[i]+ '_' + fname]= data_raw[:,i]


