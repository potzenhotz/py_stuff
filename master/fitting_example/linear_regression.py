

import numpy as np
import matplotlib.pyplot as plt



x_raw = [55, 79, 99, 144, 166, 188]
y_raw = [0.07, 0.15, 0.2, 0.33, 0.38, 0.42]

for i in range(0,len(x_raw)-1):
  diff=y_raw[i+1] - y_raw[i]


print diff

#def interpolation(x,diff):
#  y = x*diff
#  return[y]

x_data = [20.5, 40 ,60 ,80, 100, 120, 140, 160, 180, 200]

#y_data = interpolation(x_data, diff)

fig, ax = plt.subplots()

ax.plot(x_raw,y_raw)
#ax.plot(x_data,y_data)


plt.show() 
