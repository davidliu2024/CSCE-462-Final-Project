import numpy as np
import math as m

def findDistance(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    dist = np.sqrt(dx**2 - dy**2)
    if m.isnan(dist):
        dist = 0
    return dist

def findVelocity(a, b, t):
    d = findDistance(a, b)
    return d / t