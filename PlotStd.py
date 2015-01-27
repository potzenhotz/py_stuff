# Standart Python Plot Skript fuer Lukas
# NC-File Kompatibilitaet
from netCDF4 import Dataset

# MatLab Funktionaliaet
from pylab import *                  

# Latex Support und Optik
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
font = {'size'   : 18}
matplotlib.rc('font', **font)
rcParams['axes.linewidth'] = 1.5

# Interaktiven Modus aktivieren
ion() 
import sys

# Daten Laden
skalar = Dataset('avg3s.nc','r')
skalar2 = Dataset('avg5s.nc','r')
skalar3 = Dataset('avg6s.nc','r')
flow  = Dataset('avg.nc','r')


# Plotten
fig = figure()
ax  = fig.add_subplot(111)
ax.plot(skalar.variables['y'],skalar.variables['rS'][1],label='Eulerian Liquid')
ax.plot(skalar2.variables['y'],skalar2.variables['rS'][1],label='Lagrange Liquid')
ax.plot(skalar3.variables['y'],skalar3.variables['rS'][1],label='Lagrange Liquid nodiffusion')
title('First plot', fontdict=font)
xlabel('Y', fontdict=font)
#ylabel(r'$\hat{z}$', fontdict=font) #das r hier markiert, dass jetz latex code kommt
ylabel('Liquid', fontdict=font) #das r hier markiert, dass jetz latex code kommt
#xscale('log')
#xlim([0.001,1])
#ylim([-0.5,2])
legend(loc=3, prop={'size':11})
