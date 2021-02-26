import numpy as np
import matplotlib.pyplot as plt

def generateProjectionPlane():
    ''' Simple function to generate static plane for projection on XZ axes'''
    xs = np.linspace(-10, 10, 100)
    zs = np.linspace(-10, 10, 100)
    X, Z = np.meshgrid(xs, zs)
    Y = 0
    
    v1 = np.array([1,0,0])
    v2 = np.array([0,0,1])
    
    return X, Y, Z, v1, v2

# generating plane & respective normal vectors
X, Y, Z, v1, v2 = generateProjectionPlane()

#plotting plane
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(X, Y, Z, alpha = 0.3)
plt.tight_layout()

# generating vector (u) and it's projection (proj)
u = np.array([2,5,8]) # vector in question
n = np.cross(v1, v2) # vector orthogonal to plane (XZ for this application)
n_norm = np.sqrt(sum(n**2)) # normal of n
proj = u-(np.dot(u, n)/n_norm**2)*n  # calculating projection

# creating line for original vector (blue)
lineX = np.linspace(0, u[0], 100) # x-coords
lineY = np.linspace(0, u[1], 100) # y-coords
lineZ = np.linspace(0, u[2], 100) # z-coords
line = np.stack((lineX, lineY, lineZ)) # collected data

# creating line for projected vector (red)
projX = np.linspace(0, proj[0], 100) # x-coords
projY = np.linspace(0, proj[1], 100) # y-coords
projZ = np.linspace(0, proj[2], 100) # z-coords
proj = np.stack((projX, projY, projZ)) # collected data

# plotting lines
ax.plot3D(line[0], line[1], line[2], c='b') # original vector
ax.plot3D(proj[0], proj[1], proj[2], c = 'r') # projected vector

# uncomment/alter to change viewing angle
#ax.view_init(elev=0,azim=90)