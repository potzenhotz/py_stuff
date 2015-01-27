#Standart Python Plot Skript fuer Lukas
from netCDF4 import Dataset # NC-File Kompatibilitaet
from pylab import *         # MatLab Funktionaliaet
ion()                       # Interaktiven Modus aktivieren
import sys                  # variable browsing

# Daten Laden
skalar = Dataset('avg4s.nc','r')
skalar2 = Dataset('avg5s.nc','r')
flow  = Dataset('avg.nc','r')

# Plotten
fig = figure()
ax  = fig.add_subplot(111)

#print skalar.variables ;

xAxis=skalar.variables['y']
yAxis=skalar.variables['rS'][0]
xAxis2=skalar2.variables['y']
yAxis2=skalar2.variables['rS'][0]


ax.plot(xAxis,yAxis)
ax.plot(xAxis2,yAxis2)

# Beschriftung
title('Hello World')
xlabel('x')
ylabel('Skalar1')

