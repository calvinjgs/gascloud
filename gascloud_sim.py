# -*- coding: utf-8 -*-
"""
Created on Mon Oct 03 10:41:44 2016

@author: Calvin Calvin

Simulates particles attracted by gravity, and affected by friction.
Builds a data array with shape (I, N, 9)
I = tmax/dt is number of iterations
N is number of particles
at data[i, n], we have an array of properties associated
with particle n at iteration i. These properties are
the position components x, y, z.
the velocity components vx, vy, vz.
the acceleration components ax, ay, az.
so data[i, n] = [x, y, z, vx, vy, vz, ax, ay, az]
The positions are randomly decided with maximum distance R from origin
The velocities are randomly decided componentwise between -K and K.

Can be saved to a .npy file for use with gascloud_anim.py
"""


import numpy as np
import sys
import argparse


TOO_CLOSE = 1e0


#build_data_array
#builds the data array as an ndarray with shape (I, N, 9)
#I = tmax/dt is number of iterations
#N is number of particles
#at data[i, n], we have an array of properties associated
#with particle n at iteration i. These properties are
#the position components x, y, z.
#the velocity components vx, vy, vz.
#the acceleration components ax, ay, az.
#so data[i, n] = [x, y, z, vx, vy, vz, ax, ay, az]
#The positions are randomly decided with maximum distance R from origin
#The velocities are randomly decided componentwise between -K and K.
def build_data_array(N, I, R, K):
    particles = np.zeros((I, N, 9))
    theta = np.random.rand(N)*np.pi
    phi = np.random.rand(N)*2*np.pi
    r = np.random.rand(N)*R
    for i in range(N):
        x = r[i]*np.cos(phi[i])*np.sin(theta[i])
        y = r[i]*np.sin(phi[i])*np.sin(theta[i])
        z = r[i]*np.cos(theta[i])
        vx, vy, vz = (np.random.rand(3) - 0.5)*K
        particles[0, i] = np.array([x, y, z, vx, vy, vz, np.nan, np.nan, np.nan])
    return particles

#particle-particle measurements
#p1 and p2 have shape (9,)
def r(p1, p2):
    return np.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)
def dx(p1, p2):
    return p2[0] - p1[0]
def dy(p1, p2):
    return p2[1] - p1[1]
def dz(p1, p2):
    return p2[2] - p1[2]
def dv(p1, p2):
    return p2[3:6] - p1[3:6]

#friction-like force
#linear velocity dependance, with inv. sq. r dependance
def friction(p1, p2):
    c = 5e-3
    rr = r(p1, p2)
    if rr > TOO_CLOSE and rr < TOO_CLOSE*2:
        dv = p2[3:6] - p1[3:6]
        return c*dv/rr**2
    else:
        return np.array((0,0,0))

#gravity-like attractive force
#inv. sq. r dependance
def gravacc(p1, p2):
    k = 1e-1
    rr = r(p1, p2)
    is_close_x = abs(dx(p1,p2)) < TOO_CLOSE
    is_close_y = abs(dy(p1,p2)) < TOO_CLOSE
    is_close_z = abs(dz(p1,p2)) < TOO_CLOSE
    dir_x, dir_y, dir_z = (0,0,0)    
    if not is_close_x:
        dir_x = dx(p1,p2)/abs(dx(p1,p2))
    if not is_close_y:
        dir_y = dy(p1,p2)/abs(dy(p1,p2))
    if not is_close_z:
        dir_z = dz(p1,p2)/abs(dz(p1,p2))

    acc_const = 0
    if not rr < TOO_CLOSE:
        acc_const = (k/(rr)**2)
    acc_dir = np.array([dir_x, dir_y, dir_z])
    acc = acc_const*acc_dir
    return acc

#fill in data of current iteration using data from previous iteration
def tick(prev, curr, dt):
    N_parts = len(curr)
    for i in range(N_parts):
        p_i = curr[i]#particle to update
        acc = 0 #acceleration on particle i
        #sum up accelerations due to other particles not i.        
        for j in range(N_parts):
            if i != j:
                p_j = prev[j] #particle to contribute to particle i
                acc = acc + gravacc(p_i, p_j) + friction(p_i, p_j)
        #update the current time iteration using previous
        #iteration data and acc
        pos = prev[i,0:3] + acc*dt
        vel = curr[i,3:6] + pos*dt
        curr[i] = np.concatenate((pos, vel, acc))
    return curr


#run tick, filling up the data.
def simulate(data, t, dt, file=""):
    for j in range(1,len(t)):
        prev = data[j - 1]
        curr = data[j]
        data_j = tick(prev, curr, dt)
        data[j] = data_j
        prog = float(j)/float(len(t))
        update_progress(prog)
    update_progress(1)
    if (file != ""): np.save(file, data)
    return data


# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1:.2f}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()



def __main__():
    parser = argparse.ArgumentParser()
    parser.add_argument("-N", help="Number of particles.", default=10, type=int)
    parser.add_argument("-R", help="Maximum radius from origin.", default=20, type=float)
    parser.add_argument("-K", help="Magnitude of initial kinetic energy per particle/", default=0.1, type=float)
    parser.add_argument("-tmax", help="Maximum time to simulate.", default=1e3, type=float)
    parser.add_argument("-dt", help="Time step increase.", default=1e-1, type=float)
    parser.add_argument("-s", "--save", help="save as .npy file.", default=str("gascloud_data"), type=str)
    #add param file input argument
    args = parser.parse_args()
    iterations = args.tmax/args.dt
    particles = build_data_array(args.N, iterations, args.R, args.K)
    t = np.arange(0, args.tmax, args.dt)
    data = simulate(particles, t, args.dt)
    pars = np.array([float(args.N), args.R, args.K, args.tmax, args.dt])
    np.savez(args.save, data=data, pars=pars)





if __name__ == "__main__":
    __main__()