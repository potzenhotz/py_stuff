import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab




mean = 0
variance = 1
sigma = np.sqrt(variance)
x = np.linspace(-3,3,100)
y=mlab.normpdf(x,mean,sigma)
integral=0
for i in np.arange(100):
  integral=integral+0.06*y[i]

plt.plot(x,y, color='red')


mean = 0
variance = 0.5
sigma = np.sqrt(variance)
x = np.linspace(-3,3,100)
y=mlab.normpdf(x,mean,sigma)
integral_2=0
for i in np.arange(100):
  integral_2=integral_2+0.06*y[i]
print integral, integral_2
y=y*integral/integral_2
plt.plot(x,y, color='green')


plt.show()
