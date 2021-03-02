# =============================================================================
# Projecting a complex body onto a plane*
# 
# *Can only work with planes along XY/YZ/XZ axes
# *Only tested on YZ so far
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def YZplane(): # some of this is hard-coded in - will need to play with more
    # generate YZ plane stuffs
    X = 0
    ys = np.linspace(-30, 30, 100)
    zs = np.linspace(-30, 30, 100)
    Y, Z = np.meshgrid(ys, zs)
    origin = np.zeros(3) # origin [0,0,0]
    norm = np.array([1,0,0]) # normal unit vector [1, 0, 0]
    return X, Y, Z, origin, norm

# plane projection method for body composing of a 3xN array of XYZ coordinates
def projectBody(body, origin, normal):
    projection = np.zeros(body.shape) # initialize array
    distances = np.zeros([projection.shape[0], 1]) # also for distances to plane
    for i in range(body.shape[0]): # calculate projection
        point = body[i]
        v = point - origin
        dist = v[0]*normal[0] + v[1]*normal[1] + v[2]*normal[2]
        projection[i] = point - dist*normal # projection of point onto plane
        distances[i] = dist # distance from point to plane
    projection = np.hstack((projection, distances))
    return projection

# make a 3xN XYZ coord array for a line
def makeLine(x, y, z, lineOrigin):
    xCoords = np.linspace(0, x, 100)
    yCoords = np.linspace(0, y, 100)
    zCoords = np.linspace(0, z, 100)
    line = np.transpose(np.stack((xCoords, yCoords, zCoords))) # store line
    line = line[:] + lineOrigin # translate to line's origin
    return line

# compact test spiral body generator
def makeSpiral(spiralOrigin):
    # generating theta, x, y, z data for spiral shape
    theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    zCoords = np.linspace(-5, 5, 100)
    radius = zCoords**2 + 1
    xCoords = radius * np.sin(theta)
    yCoords = radius * np.cos(theta)
    spiral = np.transpose(np.stack((xCoords, yCoords, zCoords))) # store spiral
    spiral = spiral[:] + spiralOrigin # translate to spiral's origin
    return spiral

# script main here, for easily collabsable code
def main():
    # generate plane stuff
    X, Y, Z, origin, norm = YZplane()
    
    # generate the body
    # body = makeLine(10, 5, -20, lineOrigin=np.array([30, 0, 0])) # for line
    body = makeSpiral(spiralOrigin=np.array([30, 0, 0])) # for spiral
    
    # generate a project (can use line or spiral as of now)
    projection = projectBody(body, origin, norm)
    
    #plotting plane
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.tight_layout()
    ax.plot_surface(X, Y, Z, alpha = 0.3)
    
    # plotting originals & projections
    ax.plot(body[:,0], body[:,1], body[:,2])
    plt.plot(projection[:,0], projection[:,1], projection[:,2], 'b--')
    plt.plot(origin[0], origin[1], origin[2], 'r+')
    ax.legend(['Original','Projected', 'Plane Origin'])
    
    # uncomment/alter to change viewing angle
    # ax.view_init(elev=0,azim=0) # head-on to plane
    # ax.view_init(elev=0,azim=-90) # parallel to plane
    # ax.view_init(elev=90,azim=0) # above plane
    
    plt.show() # display figures at end
main()