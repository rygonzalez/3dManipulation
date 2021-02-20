#Developed by Aaron Lozhkin
#2/20/21 - 2D Projection of Vector on Plane

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import time

def orthogonalProjectionMatrix(a, b, c):
    V1 = [1, 0, (-a/c)]
    vector1 = np.array(V1)
    VP = [a, b, c]
    vPerp = np.array(VP)
    vector2 = np.cross(vector1, vPerp)
    C = np.column_stack((vector1, vector2))
    ProjectionMatrix = np.dot(np.dot(C, np.linalg.inv(np.dot(np.transpose(C), C))), np.transpose(C))
    xx, yy = np.meshgrid(range(10), range(10))
    z = (-vPerp[0] * xx - vPerp[1] * yy) * 1. / vPerp[2]
    ax.plot_surface(xx, yy, z, alpha=0.2)
    return ProjectionMatrix

def z_function(x,y):
    return np.sqrt(x**2 + y**2)

x = np.linspace(-5,5,100)
y = np.linspace(-5,5,100)

z = z_function(x,y)

arr = np.stack((x, y, z))

ax = plt.axes(projection="3d")

PW = orthogonalProjectionMatrix(3, -2, 4)

graph = np.dot(PW, arr)

ax.plot3D(arr[0,:], arr[1,:], arr[2,:])
ax.plot3D(graph[0,:], graph[1,:], graph[2,:])
plt.show()
