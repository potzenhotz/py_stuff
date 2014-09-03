# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 18:23:07 2013

@author: Potzenhotz
"""
#import struct
import os
import numpy as np
#import pylab as py
#import matplotlib as plt
import matplotlib.pyplot as plt

#a   =   np.array([1,2,3])
#print py.shape(a)
#print "Hello";
#str =   raw_input("enter your name:");
print "cwd:", os.getcwd()


def print_data(x):
    print x+x
    y=x+x 
    return y
def get_hist(x,bins,save_name):
    plt.hist(x, bins,normed=True)
    plt.title("Particle positions")
    plt.xlabel("Position")
    plt.ylabel("Number")
    #plt.savefig('foo.png')   
    #save_path=('/Users/Potzenhotz/python/figures/'+str(save_name))
    #print save_path
    #plt.savefig(save_path,format='png')
    #plt.close(1)
  
def my_range(start, end, step):
    while start <= end:
        yield start
        start += step

  
"""
def save_figure(name,save=None):
    if (save == 1):
        savepath=(path+'Figures/'+str(name)+'.pdf')
        plt.savefig(savepath,format='png',bbox_inches='tight',pad_inchs=0.45)
        print 'FIGURE at:'+savepath+' created!'
        plt.close(1)
    else:
        plt.show()
"""

#buf = binfile.read(file_size)
#psize = struct.unpack('<i4',buf[0:4])

#p1 = struct.unpack('<d',buf[5:13])
#p1[2] = struct.unpack('d',buf[13:21])
#p1[3] = struct.unpack('d',buf[21:29])w
#fname   =   np.array([])
#fname   =   list()
def read_data(path, particle_pos, particle_number):
    fname   =   ['']
    #path    =   'data/particle.'
    particle_pos    =   []
    for i in my_range(0,100,10):
        fname= path + str(i) + '.' + str(1)
        print fname
    #print fname[1]
    
    
        binfile = open(fname,"rb")
        file_size = os.path.getsize(fname)
        """
        header
        """
        binfile.seek(0,0)
        particle_number = np.fromfile(binfile, dtype = np.dtype('>i4'), count = 1)
        """
        read actual bin file
        """
        #particle_number =   particle_number - 999000
        print particle_number
        position =4
        no_of_doubles = particle_number
        # move to position in file
        binfile.seek(position,0)
        #num._data = np.fromfile(binfile, dtype = np.dtype('int32'), count = 1)
        # straight to numpy data (no buffering) 
        #particle_pos[i] = np.fromfile(binfile, dtype = np.dtype('>f8'), count = no_of_doubles)
        particle_pos.append(np.fromfile(binfile, dtype = np.dtype('>f8'), count = no_of_doubles))
            
        binfile.close()
#print particle_pos[0][0]    # erstes element im ersten element
#print particle_pos[0]       # kompletter vector des ersten elements

read_data('data/particle.', particle_pos, particle_number)

z1=print_data(np.mean(particle_pos[0]))

get_hist(particle_pos[0][1:1000000],40,'hist_particle')


