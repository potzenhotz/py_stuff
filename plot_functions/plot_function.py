#!/usr/bin/env python
import matplotlib.pyplot as plt

def plot_func(x, y, title):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(x,y)
    plt.title(title)

    plt.show()
    
def plot_func_2(x_1, y_1, x_2, y_2, title, folder):
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.plot(x_1,y_1)
    ax.plot(x_2,y_2)
    plt.title(title)
    
    plt.savefig(folder + title +'.png')
    #plt.show()
    plt.clf()
    plt.close()
    

