from sympy import *
import numpy as np
from math import*
import processing

def linearKFDDD(uvaAccelero, sUAccelero, uLightH, sULightHI, uTrue, sUTrueI):

    uEst = np.zeros(3)		# u estimated (=u predicted)
    sUEst = np.zeros((3,3))	# and the matrix u of covariances associated
    K = np.zeros((3,3))	# Kalman Gain
    tempMat = np.zeros((3,3))	# Temporary matrix used to easly compute K
    #sUTrue = np.zeros((3,3))	# Matrix of covariances of sUTrueI (I stand for input)
    #sULightH = np.zeros((3,3)) # matrix sULightH covariances
    I = np.eye(3)	        # Identity matrix
    dt = 1/120                   # Time period

    # PREDICTION (which normally follows a mathematical law, but here the prediction is given by IMU)
    # Also there is the construction of covariances matrix of sUEst

    uAccelero = uvaAccelero[0]
    vAccelero = uvaAccelero[1]
    aAccelero = uvaAccelero[2]

    uEst = uAccelero + dt * vAccelero + 1/2 * aAccelero * dt**2
    # Matrix of covariances of sUTrueI (I stand for input)
    sUEst = [[np.abs(sUAccelero[0]),0                    ,0                    ],
             [0                    ,np.abs(sUAccelero[1]),0                    ],
             [0                    ,0                    ,np.abs(sUAccelero[2])]]

    # Construction of sUTrue an sULightH, the covariances matrix from sUTrueI
    # Matrix of covariances of sUTrueI (I stand for input)
    sUTrue = [[np.abs(sUTrueI[0]),0                 ,0                 ],
              [0                 ,np.abs(sUTrueI[1]),0                 ],
              [0                 ,0                 ,np.abs(sUTrueI[2])]]

    # Matrix sULightH covariances
    sULightH = [[np.abs(sULightHI[0]),0                   ,0                   ],
                [0                   ,np.abs(sULightHI[1]),0                   ],
                [0                   ,0                   ,np.abs(sULightHI[2])]]

    #UPDATE

    # Calculus of Kalman gain K
    for i in range(3):
        for j in range(3):
            K[i][j] = sUEst[i][j] + sULightH[i][j]
    K = sUEst * np.linalg.inv(K)

    for i in range(3):
        uTrue[i] = uEst[i] + (K[i][0]*(uLightH[0] - uEst[0]) + K[i][1]*(uLightH[1] - uEst[1]) + K[i][2]*(uLightH[2] - uEst[2]) )
    # Calculus of sUTrue

    for i in range(3):
        for j in range(3):
            tempMat[i][j] = I[i][j] - K[i][j]
    sUTrue = tempMat.dot(sUTrue)



    return [uTrue, [sUTrue[0][0], sUTrue[1][1], sUTrue[2][2]]]
