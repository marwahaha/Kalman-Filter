#!/usr/bin/python
# Compute the position of a Lighthouse given
# sensor readings in a known configuration.

from sympy import *
from sympy import solve_poly_system
from math import pi
from math import *
from sys import stdin
import numpy as np
from reception import *
import time
import Position_LH

port = serial_init()
base, axis, centroids, accelerations = parse_data(port)
#print(parse_data(port))

# Period of measurement
T = 1/120.

# Initialization of IMU
accelerationX = np.zeros(2)
accelerationY = np.zeros(2)
accelerationZ = np.zeros(2)

velocityX = np.zeros(2)
velocityY = np.zeros(2)
velocityZ = np.zeros(2)

"""
positionX = np.zeros(2)
positionY = np.zeros(2)
positionZ = np.zeros(2)
"""
if (base == 0 and axis == 0) :
    h10 = centroids[0] * pi / 8333
    h13 = centroids[3] * pi / 8333
    
if (base == 0 and axis == 1) :
    v10 = centroids[0] * pi / 8333
    v13 = centroids[3] * pi / 8333
    
if (base == 1 and axis == 0) :
    h20 = centroids[0] * pi / 8333
    h23 = centroids[3] * pi / 8333

if (base == 1 and axis == 1) :
    v20 = centroids[0] * pi / 8333
    v23 = centroids[3] * pi / 8333

I_init = Position_LH.Pos( (h10+h13) / 2, (v10+v13) / 2, (h20+h23) / 2, (v20+v23) / 2)

positionX, positionY, positionZ = I_init

def position(accel):
    
    accelerationX[1] = + accel[1]
    accelerationY[1] = - accel[0]
    accelerationZ[1] = - accel[2] + 9.81

    # First integration
    velocityX[1] = velocityX[0] + accelerationX[0] * T
    velocityY[1] = velocityY[0] + accelerationY[0] * T
    velocityZ[1] = velocityZ[0] + accelerationZ[0] * T
    # Second integration
    positionX[1] = positionX[0] + velocityX[0] * T
    positionY[1] = positionY[0] + velocityY[0] * T
    positionZ[1] = positionZ[0] + velocityZ[0] * T
    
    return positionX[1]
    
    # Update previous values
    accelerationX[0] = accelerationX[1]
    accelerationY[0] = accelerationY[1]
    accelerationZ[0] = accelerationZ[1]
    velocityX[0] = velocityX[1]
    velocityY[0] = velocityY[1]
    velocityZ[0] = velocityZ[1]
    positionX[0] = positionX[1]
    positionY[0] = positionY[1]
    positionZ[0] = positionZ[1]


#while 1 :
    #print(parse_data(port))
    #base, axis, centroids, accelerations = parse_data(port)
    
    #print(accelerations)
    
    #position(accelerations)
    #print(position(accelerations))    
    
    """
    accelerationX[1] = + accelerations[1]
    accelerationY[1] = - accelerations[0]
    accelerationZ[1] = - accelerations[2] + 9.81

    # First integration
    velocityX[1] = velocityX[0] + accelerationX[0] * 1/120
    velocityY[1] = velocityY[0] + accelerationY[0] * 1/120
    velocityZ[1] = velocityZ[0] + accelerationZ[0] * 1/120
    # Second integration
    positionX[1] = positionX[0] + velocityX[0] * 1/120
    positionY[1] = positionY[0] + velocityY[0] * 1/120
    positionZ[1] = positionZ[0] + velocityZ[0] * 1/120
    
    print(positionX[1], "  ,  ", positionY[1], "  ,  ", positionZ[1])
    
    # Update previous values
    accelerationX[0] = accelerationX[1]
    accelerationY[0] = accelerationY[1]
    accelerationZ[0] = accelerationZ[1]
    velocityX[0] = velocityX[1]
    velocityY[0] = velocityY[1]
    velocityZ[0] = velocityZ[1]
    positionX[0] = positionX[1]
    positionY[0] = positionY[1]
    positionZ[0] = positionZ[1]
    """
    
    #if time.clock() >= 5 :
        #break
    
    #print("time = ",time.clock()," s" )
    #print(time.clock())