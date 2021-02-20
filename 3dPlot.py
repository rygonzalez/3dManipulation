#Developed by Aaron Lozhkin
#2/20/21 - 3D Transformations of Vectors

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import time

def z_function(x,y):
    return np.sin(np.sqrt(x**2 + y**2))

def Scale3D(a,b, c):
    return np.array([[a,0,0],[0,b,0],[0,0,c]])

def Translate3D(a, b, c):
    return np.array([[1,0,0,a],[0,1,0,b],[0,0,1,c]])

def Rotate3D(l,m,n,t):
    return np.array([[
        l*l*(1-np.cos(t)) + np.cos(t), m*l*(1-np.cos(t)) - n*np.sin(t), n*l*(1-np.cos(t)) + m*np.cos(t)
    ],[
        l * m * (1 - np.cos(t)) + n * np.sin(t), m * m * (1 - np.cos(t)) + np.cos(t),  n * m * (1 - np.cos(t)) - l * np.sin(t)
    ],[
        l * n * (1 - np.cos(t)) - m * np.sin(t),  m * n * (1 - np.cos(t)) + l * np.sin(t),  n * n * (1 - np.cos(t)) + np.cos(t)
    ]])

def Scale3dOperator(arr, a, b, c):
    return np.dot(Scale3D(a,b,c), arr)

def Translate3dOperator(arr, a, b, c):
    arrTranslate = np.vstack((arr, np.ones(100)))
    return np.dot(Translate3D(a,b,c), arrTranslate)

def Rotate3dOperator(arr, a, b, c, t):
    return np.dot(Rotate3D(a,b,c,t), arr)

x = np.linspace(-5,5,100)
y = np.linspace(-5,5,100)

z = z_function(x,y)

arr = np.stack((x, y, z))

plt.ion()
fig = plt.figure()
ax = plt.axes(projection="3d")

for i in np.linspace(0, 100, 100):
    fig.canvas.flush_events()
    arr = Translate3dOperator(arr, 1, 1, 1)
    arr = Rotate3dOperator(arr, 1, 0, 0, 45)
    ax.plot3D(arr[0,:], arr[1,:], arr[2,:])
    time.sleep(0.05)
    fig.canvas.draw()

