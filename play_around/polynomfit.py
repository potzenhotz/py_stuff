
import matplotlib.pyplot as plt
import numpy as np


y = np.array([0.0, 1.0, 3.0, 6.0,  3.0,  1.0, 0.0])
x = np.array([0.0, 0.2, 0.4, 0.6, 0.8,1.0 ,1.2])



z = np.polyfit(x, y, 4)
print z
p = np.poly1d(z)
xp = np.linspace(0, 1.2, 100)
plt.plot(x, y, '.', xp, p(xp), '-')

plt.show()
