
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack
from prettyplotlib import brewer2mpl
from matplotlib import rcParams
from scipy.interpolate import interp1d
#import prettyplotlib as ppl
 
########################################################################
#Setup plot enviroment 
########################################################################
#rcParams['font.family'] = 'serif'
#rcParams['font.serif'] = ['New Centrury Schoolbook']
#rcParams['font.family'] = 'sans-serif'
#rcParams['font.sans-serif'] = ['Helvetica']
#rcParams['font.weight'] = 'light'
rcParams['text.usetex'] = True

rcParams['axes.labelsize'] = 48
rcParams['xtick.labelsize'] = 48
rcParams['ytick.labelsize'] = 48
rcParams['legend.fontsize'] = 38
size_title=30
size_axes=58
l_w_1=6.5
l_w_2=35 #for markers

#rc('font',**{'family':'serif','serif':['Palatino']})
#rc('font',**{'family':'sans-serif','sans-serif':['Helvetica Neue']})
#rc('text', usetex=True)
#font = {'size'   : 18}
#matplotlib.rc('font', **font)
rcParams['axes.linewidth'] = 2.5
rcParams['axes.linewidth'] = 3.0
rcParams.update({'figure.autolayout':True})

########################################################################
#Some calculations for VERDI case for real time
########################################################################
#VERDI 
t_lambda=15
t_F=60
t_gravity=9.81
t_rho_c=1.164
t_cp=1022
t_T_c=268.15
B=t_F*t_gravity/(t_rho_c*t_cp*t_T_c)
t_real=((t_lambda**2)/B)**(0.3333333)
u_0=(B*t_lambda)**(0.333333)
print 'verdi t_o is:' ,t_real
print 'verdi B_o is:' ,B
print 'verdi U_o is:' ,u_0


########################################################################
#Algorithm for smothing data
########################################################################

def savitzky_golay(y, window_size, order, deriv=0, rate=1):
    r"""Smooth (and optionally differentiate) data with a Savitzky-Golay filter.
    The Savitzky-Golay filter removes high frequency noise from data.
    It has the advantage of preserving the original shape and
    features of the signal better than other types of filtering
    approaches, such as moving averages techniques.
    Parameters
    ----------
    y : array_like, shape (N,)
        the values of the time history of the signal.
    window_size : int
        the length of the window. Must be an odd integer number.
    order : int
        the order of the polynomial used in the filtering.
        Must be less then `window_size` - 1.
    deriv: int
        the order of the derivative to compute (default = 0 means only smoothing)
    Returns
    -------
    ys : ndarray, shape (N)
        the smoothed signal (or it's n-th derivative).
    Notes
    -----
    The Savitzky-Golay is a type of low-pass filter, particularly
    suited for smoothing noisy data. The main idea behind this
    approach is to make for each point a least-square fit with a
    polynomial of high order over a odd-sized window centered at
    the point.
    Examples
    --------
    t = np.linspace(-4, 4, 500)
    y = np.exp( -t**2 ) + np.random.normal(0, 0.05, t.shape)
    ysg = savitzky_golay(y, window_size=31, order=4)
    import matplotlib.pyplot as plt
    plt.plot(t, y, label='Noisy signal')
    plt.plot(t, np.exp(-t**2), 'k', lw=1.5, label='Original signal')
    plt.plot(t, ysg, 'r', label='Filtered signal')
    plt.legend()
    plt.show()
    References
    ----------
    .. [1] A. Savitzky, M. J. E. Golay, Smoothing and Differentiation of
       Data by Simplified Least Squares Procedures. Analytical
       Chemistry, 1964, 36 (8), pp 1627-1639.
    .. [2] Numerical Recipes 3rd Edition: The Art of Scientific Computing
       W.H. Press, S.A. Teukolsky, W.T. Vetterling, B.P. Flannery
       Cambridge University Press ISBN-13: 9780521880688
    """
    import numpy as np
    from math import factorial

    try:
        window_size = np.abs(np.int(window_size))
        order = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError("window_size and order have to be of type int")
    if window_size % 2 != 1 or window_size < 1:
        raise TypeError("window_size size must be a positive odd number")
    if window_size < order + 2:
        raise TypeError("window_size is too small for the polynomials order")
    order_range = range(order+1)
    half_window = (window_size -1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * factorial(deriv)
    # pad the signal at the extremes with
    # values taken from the signal itself
    firstvals = y[0] - np.abs( y[1:half_window+1][::-1] - y[0] )
    lastvals = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((firstvals, y, lastvals))
    return np.convolve( m[::-1], y, mode='valid')


def RunningMean(seq,N,M):
    """
     Purpose: Find the mean for the points in a sliding window (fixed size) 
              as it is moved from left to right by one point at a time.
      Inputs:
          seq -- list containing items for which a mean (in a sliding window) is 
                 to be calculated (N items)
            N -- length of sequence     
            M -- number of items in sliding window
      Otputs:
        means -- list of means with size N - M + 1    

    """    
    from collections import deque,Counter
    from itertools import islice  
    # Load deque (d) with first window of seq
    d = deque(seq[0:M])
    means = [np.mean(d)]             # contains mean of first window
    # Now slide the window by one point to the right for each new position (each pass through 
    # the loop). Stop when the item in the right end of the deque contains the last item in seq
    for item in islice(seq,M,N):
        old = d.popleft()            # pop(remove) oldest from left 
        d.append(item)               # push newest in from right
        means.append(np.mean(d))     # mean for current window
    return means  

def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    #including valid will REQUIRE there to be enough datapoints.
    #for example, if you take out valid, it will start @ point one,
    #not having any prior points, so itll be 1+0+0 = 1 /3 = .3333
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

print  np.repeat(1.0, 20)/20

########################################################################
#Load data
########################################################################
nbins=1000
tend=18900
tstart=10100
tstep=100

ntimes = (tend - tstart) / tstep + 1
print "NTIMES IS:", ntimes

interval = np.zeros((nbins,ntimes))
residence_lambda = np.zeros((nbins,ntimes))
residence_base = np.zeros((nbins,ntimes))
i=0

print 'ntimes',ntimes
data_path = 'ar_re200_strat_residence/'

for t in np.arange(ntimes):
  l_t=t+(tstart/tstep)
  step=l_t*tstep
  data_name=data_path + 'residence_pdf.' + np.str(step)   #name of file
  
  interval[:,i],residence_lambda[:,i],residence_base[:,i] = np.loadtxt(data_name, unpack=True) # read file into data
  i=i+1

########################################################################
#Process raw data
########################################################################

#remove the the first interval point
residence_lambda[0,:] = 0
residence_base[0,:] = 0

#remove the not yet mixed particles (at the end)
#len_dummy = residence_lambda.shape
#for j in range(len_dummy[1]):
#  for i in range(len_dummy[0]-1,0,-1):
#    if residence_lambda[i,j] != 0:
#      residence_lambda[i,j] = 0 
#      residence_lambda[i-1,j] = 0 
#      residence_lambda[i-2,j] = 0 
#      break
#  for i in range(len_dummy[0]-1,0,-1):
#    residence_lambda[i,j]=0
#    if residence_lambda[i-1,j] != 0 and residence_lambda[i-1,j] < residence_lambda[i-2,j]:
#      break

########################################################################
#Load and calculate real time
########################################################################
time_data=np.zeros(300) #300 is just a buffer
data_name=data_path + 'times.log' #name of times file
print data_name

#Load data
time_data = np.loadtxt(data_name, unpack=True) 

#Calculate real time
time_real_data=np.zeros(len(time_data))
for i in np.arange(len(time_data)): 
  time_real_data[i]=round(time_data[i]*t_real/60,2)

for k in np.arange(len(time_data)): 
  time_real_data[k]=round(time_real_data[k],0)

print time_real_data.shape

########################################################################
#Scale data
########################################################################
scale_residence_lambda = np.zeros((nbins,ntimes))
scale2_residence_lambda = np.zeros((nbins,ntimes))
scale_residence_base = np.zeros((nbins,ntimes))
total_residence_lambda = np.zeros((ntimes))
total_residence_base = np.zeros((ntimes))

#Calculate the total amount of particles to total_*
#Take a running sum and divide by total number - scaled(i)=sum(pt(0:i)/total
#Then reverse - 1-scaled
for i in range(0,ntimes): 
  total_residence_lambda[i] = np.sum(residence_lambda[:,i])
  total_residence_base[i] = np.sum(residence_base[:,i])
  for j in range(0,nbins):
    scale_residence_lambda[j,i] = np.sum(residence_lambda[0:j,i]) / total_residence_lambda[i]
    scale_residence_base[j,i] = np.sum(residence_base[0:j,i]) / total_residence_base[i]
scale_residence_lambda = 1 - scale_residence_lambda
scale_residence_base = 1 - scale_residence_base

#Second scaling 
for i in range(0,ntimes): 
  scale2_residence_lambda[:,i] = residence_lambda[:,i] / total_residence_lambda[i]
  #scale2_residence_lambda[:,i] = residence_lambda[:,i] / np.max(residence_lambda[:,i])

print 'total amount of droplets at cloud-top', ('{:.2e}'.format(np.mean(total_residence_lambda)))
integral_time=9.1 #calculate with u* and L 
time_steps=interval[1,1]-interval[0,1]  

########################################################################
#Calculate derivative data
########################################################################
diff_residence_lambda = np.zeros((nbins-1,ntimes))
diff2_residence_lambda = np.zeros((nbins-1,ntimes))

x = interval[1:nbins,88]/integral_time
for i in range(0,ntimes): 
  y = np.log(residence_lambda[1:nbins,i])
  window_sg=21
  y_2 = savitzky_golay(y,window_sg,1)

  for j in range(0,nbins-2): 
    diff2_residence_lambda[j,i] = y_2[j+1] -y_2[j]

#Test with only running mean
#less good than svityzky_golay
#window_smoth=30
#smoothed = np.zeros((nbins-window_smoth,ntimes))
#for i in range(0,ntimes): 
##  smoothed_dummy = movingaverage(np.log(residence_lambda[:,i]),window_smoth)
##  for j in range(0,nbins-window_smoth-1): 
##    smoothed[j,i] = smoothed_dummy[j+1] - smoothed_dummy[j]
#  for j in range(0,nbins-1): 
#    #diff_residence_lambda[j,i] = np.log(scale_residence_lambda[j+1,i]) - np.log(scale_residence_lambda[j,i])
#    diff_residence_lambda[j,i] = np.log(residence_lambda[j+1,i]) - np.log(residence_lambda[j,i])
#  smoothed[:,i] = movingaverage(diff_residence_lambda[:,i],window_smoth)


########################################################################
#Plot data
########################################################################
fig, ax = plt.subplots()
color_set = brewer2mpl.get_map('paired', 'qualitative', 12).mpl_colors
color_set_2 = brewer2mpl.get_map('PuBu', 'sequential', 9).mpl_colors
color_set_3 = brewer2mpl.get_map('Dark2', 'qualitative', 8).mpl_colors
color_set_4 = brewer2mpl.get_map('Pastel1', 'qualitative', 9).mpl_colors


t_inter=tstart/tstep
print 't_intermediate',t_inter

#Scaled data to plot
list = [22, 32, 42, 54, 63, 74, 85]
k=0
for i in range(t_inter,len(time_real_data)):
  k=k+1
  #print time_real_data[i],k
l_c = [2, 1, 0, 4, 5, 6, 7]
j=0
for i  in list:
  label_name='t=' + str(int(time_real_data[i+t_inter-1])) + ' min'
  ax.plot(interval[:,44]/integral_time, scale_residence_lambda[:,i], color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2, label='Simulation ' + label_name)
  j=j+1

#PLOT PROPERTIES
plt.legend(loc=1,numpoints=1, frameon=False)
ax.set_yscale('log')

ax.set_xlabel(r'$t/t^*$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
ax.set_ylabel(r'Percentile', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
plt.xlim(0,5)
plt.ylim(10**-5,3)

#Hide the right and top spines
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax.yaxis.set_ticks_position('left')
ax.xaxis.set_ticks_position('bottom')

#Plot horizontal and vertical line:
#ax.plot((x1,x2),(y1,y2))
#ax.plot((0,1),(0.1,0.1), linewidth=l_w_1, color=color_set_4[2], zorder=1)
#ax.plot((0,.75),(0.15,0.15), linewidth=l_w_1, color=color_set_4[2], zorder=10)
#ax.plot((0,.1),(0.75,0.75), linewidth=l_w_1, color=color_set_4[2], zorder=10)
#ax.plot((1,1),(0.00001,0.1), linewidth=l_w_1, color=color_set_4[2], zorder=1)
#ax.plot((.75,.75),(0.00001,0.15), linewidth=l_w_1, color=color_set_4[2], zorder=10)
#ax.plot((.1,.1),(0.00001,0.75), linewidth=l_w_1, color=color_set_4[2], zorder=10)
#ax.plot((0,2.5),(0.001,0.001), linewidth=l_w_1, color=color_set_4[2], zorder=1)
#ax.plot((2.5,2.5),(0.00001,0.001), linewidth=l_w_1, color=color_set_4[2], zorder=1)

########################################################################
#Plot derivative
########################################################################
fig, ax2 = plt.subplots()

#Deriative data to plot
list = [22, 32, 42, 54, 63, 74, 85]
l_c = [2, 1, 0, 4, 5, 6, 7]
j=0
for i  in list:
  label_name='t=' + str(int(time_real_data[i+t_inter-1])) + ' min'
  #ax2.plot(interval[0:nbins-1,44]/integral_time, diff_residence_lambda[:,i]/(time_steps/integral_time),color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2)
  ax2.plot(interval[(window_sg-1)/2:500+(window_sg-1)/2,88]/integral_time, diff2_residence_lambda[0:500,i]/(time_steps/integral_time),color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2)
  j=j+1



plt.xlim(0,5)
plt.ylim(-5,2.5)
#plt.ylim(-5,0.5)
ax2.set_ylabel(r'$d(log(p))/dt$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
ax2.set_xlabel(r'$t/t^*$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt

#Hide the right and top spines
ax2.spines['right'].set_visible(False)
ax2.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax2.yaxis.set_ticks_position('left')
ax2.xaxis.set_ticks_position('bottom')

#Plot horizontal and vertical line:
#ax.plot((x1,x2),(y1,y2))
#ax2.plot((0.75,0.75),(1,4), linewidth=l_w_1, color=color_set_4[2], zorder=1)
#ax2.plot((2.5,2.5),(1,2), linewidth=l_w_1, color=color_set_4[2], zorder=1)

########################################################################
#Plot with second scaling
########################################################################
fig, ax3 = plt.subplots()

#Deriative data to plot
list = [22, 32, 42, 54, 63, 74, 85]
l_c = [2, 1, 0, 4, 5, 6, 7]
j=0
for i  in list:
  label_name='t=' + str(int(time_real_data[i+t_inter-1])) + ' min'
  ax3.plot(interval[:,44]/integral_time, residence_lambda[:,i],color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2)
  #ax3.plot(interval[:,44]/integral_time, smoothed[:,i],color=color_set_3[l_c[j]],marker='.',linestyle='None',markersize=l_w_2)
  j=j+1


plt.xlim(0,5)
#plt.ylim(10**-5,1)
ax3.set_yscale('log')

ax3.set_xlabel(r'$t/t^*$', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt
ax3.set_ylabel(r'Amount of cloud droplets', fontsize=size_axes)#,fontdict=font) #das r hier markiert, dass jetz latex code kommt

#Hide the right and top spines
ax3.spines['right'].set_visible(False)
ax3.spines['top'].set_visible(False)
#Only show ticks on the left and bottom spines
ax3.yaxis.set_ticks_position('left')
ax3.xaxis.set_ticks_position('bottom')

########################################################################
#Show all plots
########################################################################
#plt.show()

