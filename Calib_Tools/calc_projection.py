# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 11:56:40 2018

@author: P. Wolf

title: calc_projection
"""
#%% Imports
import numpy as np
from copy import deepcopy

#%% main functions
def viewmtx(az,el,phi,target):
    
    if phi>0:
        d = np.sqrt(2)/2/np.tan(phi*np.pi/360)
    else:
        phi = 0
    
    # Make sure data is in the correct range.
    el = (((el+180)%360)+360%360)-180
    if el>90:
      el = 180-el
      az = az + 180
    elif el<-90:
      el = -180-el
      az = az + 180
    
    az = (az%360)+360%360
    
    #Convert from degrees to radians.
    az = az*np.pi/180
    el = el*np.pi/180
    
    if 'target' not in locals():
        target = 0.5 + np.sqrt(3)/2*np.asarray([[np.cos(el)*np.sin(az), -np.cos(el)*np.cos(az), np.sin(el)]])
        
    # View transformation matrix:
    # Formed by composing two rotations:
    #    1) Rotate about the z axis -AZ radians
    #    2) Rotate about the x axis (EL-pi/2) radians
    
    T = np.asarray([[np.cos(az), np.sin(az), 0, 0],
            [-np.sin(el)*np.sin(az), np.sin(el)*np.cos(az), np.cos(el), 0],
            [np.cos(el)*np.sin(az), -np.cos(el)*np.cos(az), np.sin(el), 0],
            [0, 0, 0, 1]])
    
    # Default focal length.
    f = d
    
    # Transformation to move origin of object coordinate system to TARGET
    eye = np.identity(4)
    temp1 = eye[:,0:3]
    temp2 = np.dot(T, np.append(-target,1))
    temp2 = temp2.reshape(4,1)
    O1 = np.append(temp1[:,:], temp2[:,:], axis=1)
    
    # Perspective transformation
    P = np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, -1/f, d/f]])
    
    # The perspective transformation above works because the graphics
    # system divides by the homogenous length, w, before mapping to the screen.
    # If the homegeous vector is given by V = [x,y,z,w] then the transformed
    # point is U = [x/w y/w].
    
    # Using f = d places the image plane through the origin of the object 
    # coordinate system, thus projecting the object onto this plane.  Note only
    # the x and y coordinates are used to draw the object in the graphics window.
    
    # Form total transformation
    return np.dot(P, np.dot(O1, T))

def calc_projection(input_3D,azimuth,elevation,angle,center):
    temp_in = deepcopy(input_3D)
    input_3D[:,1] = temp_in[:,2]
    input_3D[:,2] = temp_in[:,1]
    
    a = viewmtx(azimuth,elevation,angle,center);
    
    m = np.size(input_3D,0)
    
    x4d = np.vstack((input_3D[:,0], input_3D[:,1], input_3D[:,2], np.ones((m,))))
    x2d = np.dot(a, x4d)
    
    x2 = np.zeros((m,1))
    y2 = np.zeros((m,1))
    
    x2 = x2d[0,:]/x2d[3,:]
    y2 = x2d[1,:]/x2d[3,:]
    
    output_2D = np.transpose(np.vstack((x2, y2)))
    return output_2D

#import numpy.matlib as npm
#gt_px = np.ndarray((27,3))
#gt_px[:,0] = 10 * np.hstack((-np.ones((9,)), np.zeros((9,)), np.ones((9,))))
#gt_px[:,1] = 10 * npm.repmat(np.hstack((-np.ones((3,)), np.zeros((3,)), np.ones((3,)))), 1, 3)
#gt_px[:,2] = 10 * npm.repmat(np.asarray([[-1,0,1]]), 1, 9)
#
#gt_px = calc_projection(gt_px,0,0,1,np.asarray([[0, 0, 0]]))

