
import matplotlib.pyplot as plt
import numpy as np


x =  np.linspace(-5,5,1000)

y_1=x**2
y_2=x**4
y_3=x**6
#y_4=x**5


plt.plot(x,y_1)
plt.plot(x,y_2)
plt.plot(x,y_3)
#plt.plot(x,y_4)

plt.show()

