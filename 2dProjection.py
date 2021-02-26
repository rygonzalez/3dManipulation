#Developed by Aaron Lozhkin - Modified by Ryan
#2/25/21 - 2D Projection of Vector on Plane

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np

def orthogonalProjectionMatrix(a, b, c): # struggling to determine how first block of math works
    # generating & collecting our data
    vector1 = np.array([1, 0, (-a/c)]) # why is this chosen. Don't understand math
    vPerp = np.array([a, b, c]) # are we defining our perpendicular line?
    vector2 = np.cross(vector1, vPerp)
    C = np.column_stack((vector1, vector2))
    
    # creating matrix of the projection of our line upon the 
    ProjectionMatrix = np.dot(
        np.dot(C, np.linalg.inv(np.dot(np.transpose(C), C))), np.transpose(C))
    
    # creating the plane to be projected upon
    planeX, planeY = np.meshgrid(range(-5, 6), range(-5, 6)) # choose size of plane here
    planeZ = (-vPerp[0] * planeX - vPerp[1] * planeY) / vPerp[2] #calculates based off X & Y 
    projectionPlane = [planeX, planeY, planeZ]
    return ProjectionMatrix, projectionPlane

# generating our original line (blue)
lineX = np.linspace(0, 1, 100) # x-coords
lineY = np.linspace(0, 1, 100) # y-coords
lineZ = np.hypot(lineX, lineY) # z-coords
line = np.stack((lineX, lineY, lineZ)) 

print(line)

# generating line projection (orange) & projection plane
projectedLine, plane = orthogonalProjectionMatrix(0, 0, 1) # calculates proj & plane - does this take the origin?
projection = np.dot(projectedLine, line) # final line projection calcs

# plotting various components
ax = plt.axes(projection="3d")
ax.plot3D([0,1], [0,1], [0,1]) # original line
ax.plot3D(projection[0], projection[1], projection[2]) # projected line
ax.plot_surface(plane[0], plane[1], plane[2], alpha=0.2) # projection plane
plt.show()