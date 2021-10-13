# =============================================================================
# Projecting a complex body onto a plane*
# 
# *Can only work with planes along XY/YZ/XZ axes
# *Only tested on YZ so far
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def YZplane(planeRange, resolution): # some of this is hard-coded in - will need to play with more
    # generate YZ plane stuffs
    X = 0
    ys = np.linspace(-planeRange, planeRange, resolution)
    zs = np.linspace(-planeRange, planeRange, resolution)
    Y, Z = np.meshgrid(ys, zs)
    origin = np.zeros(3) # origin [0,0,0]
    norm = np.array([1,0,0]) # normal unit vector [1, 0, 0]
    return X, Y, Z, origin, norm

# plane projection method for body composing of a 3xN array of XYZ coordinates
def projectBody(body, origin, normal):
    projection = np.zeros(body.shape) # initialize array
    distance = np.zeros(body.shape[0])
    for i in range(body.shape[0]): # calculate projection
        point = body[i]
        v = point - origin
        dist = v[0]*normal[0] + v[1]*normal[1] + v[2]*normal[2]
        projection[i] = point - dist*normal # projection of point onto plane
        distance[i] = dist
    projection = projection * 10
    projection = np.round(projection, 0)
    projection = projection / 10
    return projection, distance

# make a 3xN XYZ coord array for a line
def makeLine(x, y, z, lineOrigin, resolution):
    xCoords = np.linspace(0, x, resolution)
    yCoords = np.linspace(0, y, resolution)
    zCoords = np.linspace(0, z, resolution)
    line = np.transpose(np.stack((xCoords, yCoords, zCoords))) # store line
    line = line[:] + lineOrigin # translate to line's origin
    return line

# # compact test spiral body generator
# def makeSpiral(spiralOrigin, planeRange):
    # # generating theta, x, y, z data for spiral shape
    # theta = np.linspace(-4 * np.pi, 4 * np.pi, 100)
    # zCoords = np.linspace(-planeRange, planeRange, 100)
    # radius = zCoords**2 + 1
    # xCoords = radius * np.sin(theta)
    # yCoords = radius * np.cos(theta)
    # spiral = np.transpose(np.stack((xCoords, yCoords, zCoords))) # store spiral
    # spiral = spiral[:] + spiralOrigin # translate to spiral's origin
    # return spiral

def makeSpiral(y, z, origin):
    y = np.cos(y)*y
    z = np.sin(z)*z
    x = z + y
    spiral = np.transpose(np.stack((x, y, z))) # store spiral
    spiral = spiral[:] + origin # translate to spiral's origin
    return spiral

def getTangentSlopes(body): # assumes tangents[0] = tangents[1]
    tangents = np.zeros(body.shape)
    for i in range(1, body.shape[0]):
        tangents[i] = body[i] - body [i-1]
    tangents[0] = tangents[1]
    return tangents    

# returns the angles between a vector(s) and the normal of a plane
def checkAngles(tangents, planeNorm, degrees=False):
    angles = np.zeros([tangents.shape[0], 1])
    n = planeNorm
    for i in range(angles.shape[0]):
        v = tangents[i] / np.linalg.norm(tangents[i])
        angles[i] = np.arccos(np.dot(v,n) / (np.linalg.norm(v) * np.linalg.norm(n)))
    if degrees:
        angles = np.degrees(angles)
    return angles

def plotProjectionPlane(planeX, planeY, planeZ, body, projection, origin):
    #plotting plane
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    plt.tight_layout()
    ax.plot_surface(planeX, planeY, planeZ, alpha=0.3)
    
    # plotting originals & projections
    ax.plot(body[:,0], body[:,1], body[:,2])
    plt.plot(projection[:,0], projection[:,1], projection[:,2], 'b--')
    plt.plot(origin[0], origin[1], origin[2], 'r+')
    ax.legend(['Original','Projected', 'Plane Origin'])
    
    
    ax.plot_surface(planeX+4, planeY, planeZ, alpha=0.5)
    ax.plot_surface(planeX+6, planeY, planeZ, alpha=0.5)   
    
    # uncomment/alter to change viewing angle
    # ax.view_init(elev=0,azim=0) # head-on to plane
    # ax.view_init(elev=0,azim=-90) # parallel to plane
    # ax.view_init(elev=90,azim=0) # above plane
    
    plt.show() # display figures at end

def plotResponseMap(x, y, angles, projection, distance, resolution):
    x = np.trunc(x*10**2)/(10**2)
    y = np.trunc(y*10**2)/(10**2)
    X, Y = np.meshgrid(x, y)
    Z = np.zeros(X.shape)
    strength = np.multiply((angles-90), 1/((np.reshape(distance, [resolution,1]))**2)) # make sure you're in degrees
    A = np.transpose(np.stack((projection[:,1], projection[:,2], strength[:,0])))
    
    A = np.trunc(A*10**2)/(10**2)
    
    for i in range(x.shape[0]):
        for j in range(y.shape[0]):
            for k in range(A.shape[0]):
                # if np.isclose(A[k,0], x[i], atol=0.303) and np.isclose(A[k,1], y[k], atol=0.303):
                # print(A[k,0], x[i])
                if A[k,0] == x[i] and A[k,1] == y[j]:
                    # print(True)
                    Z[i,j] = A[k,2]
                        #  Z[i,j] = 50000

    fig = plt.figure()
    ax = plt.axes(projection='3d')
    # ax = ax.scatter(A[:,0], A[:,1], A[:,2])
    ax.contour3D(X, Y, Z, 50, cmap='binary')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z');
    ax.view_init(elev=0,azim=0)

# script main here
def main():
    # variables here
    planeRange = 10
    resolution = 201
    y = np.linspace(-planeRange, planeRange, resolution)
    z = np.linspace(-planeRange, planeRange, resolution)
    
    # print(y)
    
    # generate plane stuff
    planeX, planeY, planeZ, origin, norm = YZplane(planeRange, resolution)
    # generate the body
    spiralOrigin = np.array([30,0,0])
    body = makeSpiral(y, z, spiralOrigin) 
    # body = makeLine(10,10,10,spiralOrigin, resolution)
    # generate a projection (can use line or spiral as of now)
    projection, distance = projectBody(body, origin, norm)
    # plot projection
    plotProjectionPlane(planeX, planeY, planeZ, body, projection, origin) 
    
    # generate angle response
    tangents = getTangentSlopes(body)
    angles = checkAngles(tangents, norm, degrees=True)
    plotResponseMap(y, z, angles, projection, distance, resolution)
    
main()