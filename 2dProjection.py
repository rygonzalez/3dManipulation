#Developed by Aaron Lozhkin - Modified by Ryan
#2/25/21 - 2D Projection of Vector on Plane

import matplotlib.pyplot as plt
import numpy as np

def orthogonalProjectionMatrix(a, b, c):
    '''
    takes a vector as input and returns an orthogonal plane, as well as a 
    line that is projected on said plane
    '''
    # generating our initial constructive data
    vPerp = np.array([a, b, c]) # storing input vector
    vector1 = np.array([1, 0, (-a/c)]) # defining perpendicular vector (v1)
    vector2 = np.cross(vector1, vPerp)  # defining orthogonal vector (v2)
    C = np.column_stack((vector1, vector2)) # combining v1 & v2
    
    # creating projected line's coordinate matrix 
    projectedLine = np.dot(
        np.dot(C, np.linalg.inv(np.dot(np.transpose(C), C))), np.transpose(C))
    
    # creating the plane to be projected upon
    planeX, planeY = np.meshgrid(range(-5, 6), range(-5, 6)) # choose size of plane here
    planeZ = (-vPerp[0] * planeX - vPerp[1] * planeY) / vPerp[2] #calculates based off X & Y 
    projectionPlane = [planeX, planeY, planeZ]
    return projectedLine, projectionPlane

# generating our original line
lineX = np.linspace(-10, 10, 100) # x-coords
lineY = np.linspace(-10, 10, 100) # y-coords
lineZ = np.hypot(lineX, lineY) # z-coords
line = np.stack((lineX, lineY, lineZ)) 

# generating line projection & projection plane
projectedLine, plane = orthogonalProjectionMatrix(0, 0, 1) # calculates proj & plane
lineProjection = np.dot(projectedLine, line) # final line projection calcs

print(lineProjection[0])

# plotting various components
ax = plt.axes(projection="3d")
ax.plot3D(line[0], line[1], line[2], c='b') # original line
ax.plot3D(lineProjection[0], lineProjection[1], lineProjection[2], c='r') # projected line
ax.plot_surface(plane[0], plane[1], plane[2], alpha=0.5, color='g') # projection plane
plt.show()