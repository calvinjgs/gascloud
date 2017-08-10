# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 16:14:13 2016

@author: Calvin Calvin

Visualizes and animates the gascloud simulation.
Takes a .npy generated from gascloud_sim.py

"""


import numpy as np
import time
import sys
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import argparse

def anim_step(t, data, scat):
    scat._offsets3d = (data[t,:,0], data[t,:,1], data[t,:,2])
    return scat,



def plot3D(t_0, t_f, data):
    # Attaching 3D axis to the figure
    fig = plt.figure()
    ax = p3.Axes3D(fig)
    scat = ax.scatter3D(data[t_0,:,0], data[t_0,:,1], data[t_0,:,2],s=100)
    # Setting the axes properties
    lims = 20
    ax.set_xlim3d([-lims, lims])
    ax.set_xlabel('X')
    
    ax.set_ylim3d([-lims, lims])
    ax.set_ylabel('Y')
    
    ax.set_zlim3d([-lims, lims])
    ax.set_zlabel('Z')
    
    ani = animation.FuncAnimation(fig, anim_step, frames=range(t_0, t_f, 10), fargs=(data, scat),interval=10)
    plt.show()


def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="gas cloud .npy file to animate (include .npy)", default="gascloud_data.npy", type=str)
    parser.add_argument("-ti", help="initial iteration", default=0, type=int)
    parser.add_argument("-tf", help="final iteration", type=int)


    args = parser.parse_args()

    data = np.load(args.file)
    if not args.tf: args.tf = len(data)
    plot3D(args.ti, len(data), data)


# this is for in case I feel like revisiting these plots again
#==============================================================================
# 
#     #plot stuff
#     fig = 1
# 
# 
#     plt.figure(fig)
#     fig = fig + 1
#     plt.plot(pos0, vel0, 'r')
#     plt.title("phase space")
#     plt.xlabel("position")
#     plt.ylabel("velocity")
#     plt.show()
# 
#     plt.figure(fig)
#     fig = fig + 1
#     for p in range(np.size(data,1)):
#         plt.plot(data[:,p,0],data[:,p,1])
#     plt.title("x-y position")
#     plt.xlabel("position x")
#     plt.ylabel("position y")
#     plt.show()
# 
# 
#     plt.figure(fig)
#     fig = fig + 1
#     plt.plot(t, data[:,0,0], 'r', t, data[:,1,0], 'b')
#     plt.title("position time")
#     plt.xlabel("time")
#     plt.ylabel("position x")
#     plt.show()
# 
#     plt.figure(fig)
#     fig = fig + 1
#     plt.plot(t, data[:,0,6], 'r', t, data[:,1,6], 'b')
#     plt.title("acceleration time")
#     plt.xlabel("time")
#     plt.ylabel("acceleration x")
#     plt.show()
# 
# 
#
#==============================================================================
    


if __name__ == "__main__":
    __main__()
