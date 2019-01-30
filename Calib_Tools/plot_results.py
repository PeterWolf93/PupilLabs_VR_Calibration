# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 10:52:39 2018

@author: P. Wolf

title: plot_results
"""
#%% Imports
import matplotlib.pyplot as plt
import numpy as np

#%% close all old plots
plt.close('all')
plt.rc('axes', axisbelow=True)

#%% Main Functions
#%% calculate limits for eye_data plots
def calc_lims_eye_data(eye_data):
    tmin = 0
    tmax = np.ceil(np.max(eye_data[:,0,0]))
    
    xmax = np.max(np.hstack((eye_data[:,3,0], eye_data[:,3,1])))*1.1
    ymax = np.max(np.hstack((eye_data[:,4,0], eye_data[:,4,1])))*1.1
    
    xmin = abs(np.min(np.hstack((eye_data[:,3,0], eye_data[:,3,1]))))*0.9
    ymin = abs(np.min(np.hstack((eye_data[:,4,0], eye_data[:,4,1]))))*0.9
    
    allmin = min(xmin, ymin)
    allmax = max(xmax, ymax)
    return tmin, tmax, allmin, allmax

#%% calculate limits for gt plots
def calc_lims_gt(gt):
    mingt = -abs(np.min(gt))*1.2
    maxgt = np.max(gt)*1.2
    return mingt, maxgt
    
    
#%% plot uncalibrated data
def plot_mask(mask_ind, eye_data, masked_eye_data, save_plot):
    f1 = plt.figure(1, figsize=(16,9))
    
    tmin, tmax, allmin, allmax = calc_lims_eye_data(eye_data)
    
    start = int(mask_ind[mask_ind[:,2]==1,0])
    start_mask = np.where(masked_eye_data[:,0,0] > eye_data[start,0,0])[0][0]
    if start <= 0:
        start = 1
    else:
        start = start - 10
    tstart = eye_data[start,0,0]
    
    stop = int(mask_ind[mask_ind[:,2]==np.max(mask_ind[:,3]),1])
    stop_mask = np.where(masked_eye_data[:,0,0] > eye_data[stop,0,0])[0][0]
    if stop > np.size(eye_data, 0):
        stop = np.size(eye_data, 0)
    else:
        stop = stop + 10
    tstop = eye_data[stop,0,0]
        
    title_list = ['left', 'right']
    for i in range(2):
        plt.subplot(2,3,3*i+1)
        plt.title(title_list[i])
        plt.xlim(tstart, tstop)
        plt.ylim(allmin, allmax)
        plt.xlabel('t in s')
        plt.ylabel('x in a.u.')
        plt.grid(linestyle='dashed')
        plt.plot(eye_data[start:stop,0,i], eye_data[start:stop,3,i], c='b')
        plt.scatter(masked_eye_data[start_mask:stop_mask,0,i], 
                 masked_eye_data[start_mask:stop_mask,3,i], c='r',marker='o')
        
        plt.subplot(2,3,3*i+2)
        plt.title(title_list[i])
        plt.xlim(tstart, tstop)
        plt.ylim(allmin, allmax)
        plt.xlabel('t in s')
        plt.ylabel('y in a.u.')
        plt.grid(linestyle='dashed')
        plt.plot(eye_data[start:stop,0,i], eye_data[start:stop,4,i], c='b')
        plt.scatter(masked_eye_data[start_mask:stop_mask,0,i], 
                 masked_eye_data[start_mask:stop_mask,4,i], c='r',marker='o')
        
        plt.subplot(2,3,3*i+3)
        plt.title(title_list[i])
        plt.xlim(allmin, allmax)
        plt.ylim(allmin, allmax)
        plt.xlabel('x in a.u.')
        plt.ylabel('y in a.u.')
        plt.grid(linestyle='dashed')
        plt.plot(eye_data[start:stop,3,i], eye_data[start:stop,4,i], c='b')
        plt.scatter(masked_eye_data[start_mask:stop_mask,3,i], 
                 masked_eye_data[start_mask:stop_mask,4,i], c='r',marker='o')
        
    f1.show()
    if save_plot == 1:
        f1.savefig('Pictures\\Mask.png', dpi = 500)
    
#%% plot calibrated 2D grid
def plot_Grid_2D(cal_grid, gt, save_plot):
    f2 = plt.figure(2, figsize=(16,9))
    
    mingt, maxgt = calc_lims_gt(gt)
    
    plt.title('Calibrated Grid')
    plt.xlim(mingt, maxgt)
    plt.ylim(mingt, maxgt)
    plt.xlabel('x in °')
    plt.ylabel('y in °')
    plt.grid(linestyle='dashed')
    
    plt.scatter(gt[:,0],gt[:,1], c='k', marker='o')
    plt.scatter(cal_grid[:,0,0],cal_grid[:,1,0], c='b' ,marker='x')
    plt.scatter(cal_grid[:,0,1],cal_grid[:,1,1], c='r', marker='+')
    plt.scatter(cal_grid[:,0,2],cal_grid[:,1,2], c='g', marker='d')
    plt.legend(['gt','L','R','av'])
    
    f2.show()
    if save_plot == 1:
        f2.savefig('Pictures\\Grid2D.png', dpi = 500)

#%% plot calibrated 3D grid
def plot_Grid_3D(cal_grid, gt, mean_or_all, save_plot):
    f3 = plt.figure(3)
    ax = f3.add_subplot(111, projection='3d')
    
    mingt, maxgt = calc_lims_gt(gt)
    
    color_list = ['b','r','g']
    marker_list = ['x','+','d']
    label_list = ['left','right','average']
    ax.scatter(gt[:,0],gt[:,1],gt[:,2],c='k',marker='o',label='gt')
    
    if mean_or_all == 1:
        ax.scatter(cal_grid[:,0,2],cal_grid[:,1,2],cal_grid[:,2,2],
                   c=color_list[2],marker=marker_list[2],label=label_list[2])
    elif mean_or_all == 2:
        for i in range(0,3):
            ax.scatter(cal_grid[:,0,i],cal_grid[:,1,i],cal_grid[:,2,i],
                       c=color_list[i],marker=marker_list[i],label=label_list[i])
    
    for i in range(np.size(gt,0)):
        ax.plot([gt[i,0], cal_grid[i,0,2]],[gt[i,1], cal_grid[i,1,2]],
                [gt[i,2], cal_grid[i,2,2]],c='c',linestyle=':')
    
    
    plt.legend()
    plt.title('Calibrated Grid')
    plt.xlim(mingt, maxgt)
    plt.ylim(mingt, maxgt)
    ax.set_zlim(mingt, maxgt)
    plt.xlabel('x in °')
    plt.ylabel('y in °')
    ax.set_zlabel('z in a.u.')
    plt.grid(linestyle='dashed')
    
    f3.show()
    if save_plot == 1:
        f3.savefig('Pictures\\Grid3D.png', dpi = 500)
    
#%% plot calibrated eye_data (val_eye_data)
def plot_calib(masked_val_eye_data, val_eye_data, gt, cal_grid, save_plot):
    f4 = plt.figure(4, figsize=(16,9))
    
    tmin, tmax, allmin, allmax = calc_lims_eye_data(val_eye_data)
    mingt, maxgt = calc_lims_gt(gt)
        
    title_list = ['left', 'right']
    for i in range(2):
        plt.subplot(2,3,3*i+1)
        plt.title(title_list[i])
        plt.xlim(tmin, tmax)
        plt.ylim(mingt, maxgt)
        plt.xlabel('t in s')
        plt.ylabel('x in a.u.')
        plt.grid(linestyle='dashed')
        plt.plot(val_eye_data[:,0,i], val_eye_data[:,3,i], c='b')
        plt.scatter(masked_val_eye_data[:,0,i], masked_val_eye_data[:,3,i], c='r',marker='o')
        
        plt.subplot(2,3,3*i+2)
        plt.title(title_list[i])
        plt.xlim(tmin, tmax)
        plt.ylim(mingt, maxgt)
        plt.xlabel('t in s')
        plt.ylabel('y in a.u.')
        plt.grid(linestyle='dashed')
        plt.plot(val_eye_data[:,0,i], val_eye_data[:,4,i], c='b')
        plt.scatter(masked_val_eye_data[:,0,i], masked_val_eye_data[:,4,i], c='r',marker='o')
        
        plt.subplot(2,3,3*i+3)
        plt.title(title_list[i])
        plt.xlim(mingt, maxgt)
        plt.ylim(mingt, maxgt)
        plt.xlabel('x in a.u.')
        plt.ylabel('y in a.u.')
        plt.grid(linestyle='dashed')
        plt.plot(val_eye_data[:,3,i], val_eye_data[:,4,i], c='b')
        plt.scatter(masked_val_eye_data[:,3,i], masked_val_eye_data[:,4,i], c='r',marker='o')
        plt.scatter(gt[:,0],gt[:,1],c='k',marker='o')
        
    f4.show()
    if save_plot == 1:
        f4.savefig('Pictures\\val_eye.png', dpi = 500)
            
def plot_stream(val_eye_data, gt):
    plt.ion()
    f5 = plt.figure(5, figsize=(8,4))
    
    tmin, tmax, allmin, allmax = calc_lims_eye_data(val_eye_data)
    mingt, maxgt = calc_lims_gt(gt)
    
    plt.xlim(tmin, tmax)
    plt.ylim(mingt, maxgt)
    plt.xlabel('t in s')
    plt.ylabel('x in a.u.')
    
    x = val_eye_data[:,3,0]
    y = val_eye_data[:,4,0]    
    
    ax = f5.add_subplot(111)
    line1, = ax.plot(x, y, 'b-')
    
    for time in range(np.size(x)):
        line1.set_ydata(np.sin(x + time))
        f5.canvas.draw()
        f5.canvas.flush_events()