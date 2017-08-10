**gascloud simulation**
gascloud_sim.py simulates particles attracted to eachother by an *r*^(-2) force (i.e. gravity) and subject to a frictional force proportional to the velocity.
Builds a data array with shape (*I*, *N*, *9*).
*I = tmax/dt* is number of iterations.
*N* is number of particles.
at *data*[*i*, *n*], we have an array of properties associated.
with particle *n* at iteration *i*. These properties are:
the position components *x*, *y*, *z*.
the velocity components *vx*, *vy*, *vz*.
the acceleration components *ax*, *ay*, *az*.
so *data*[*i*, *n*] = [*x, y, z, vx, vy, vz, ax, ay, az*].
The positions are randomly decided with maximum distance *R* from origin.
The velocities are randomly decided componentwise between *-K* and *K*.

Can be saved to a .npy file for use with gascloud_anim.py
```
usage: gascloud_sim.py [-h] [-N N] [-R R] [-K K] [-tmax TMAX] [-dt DT]
                       [-s SAVE]

optional arguments:
  -h, --help            show this help message and exit
  -N N                  Numer of particles.
  -R R                  Maximum radius from origin.
  -K K                  Magnitude of initial kinetic energy per particle/
  -tmax TMAX            Maximum time to simulate.
  -dt DT                Time step increase.
  -s SAVE, --save SAVE  save as .npy file.
```
All arguments are optional, default values are
```
N = 10
R = 20 distance units
K = 0.1 energy units
tmax = 1000 time units
dt = 0.1 time units
s = "gascloud_data"
```
So running
```
python gascloud_sim.py
```
will run the simulation with all the default values. These arguments may change to
positional ones in later versions to make running the command without any arguments
more useful.

**gascloud animation**
gascloud_anim.py visualizes and animates the gascloud simulation.
It takes a .npy generated from gascloud_sim.py
```
usage: gascloud_anim.py [-h] [-f FILE] [-ti TI] [-tf TF]

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  gas cloud .npy file to animate (include .npy)
  -ti TI                initial iteration
  -tf TF                final iteration
 ```

 All arguments are optional, default values are
 ```
 f = "gascloud_data.npy"
 ti = 0
 tf = tmax (the entire dataset)
```


___
The progress bar in gascloud_sim.py is taken from an answer on [this stackoverflow question](https://stackoverflow.com/questions/3160699/python-progress-bar).

