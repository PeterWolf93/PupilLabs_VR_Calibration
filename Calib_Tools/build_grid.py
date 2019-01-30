# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:41:00 2018

@author: P. Wolf

title: build_grid
"""
#%% Imports
import numpy as np
from calib_function import calib_function
from valid_function import valid_function

#%% main function
def build_grid(cal_data, val_data, ground_truth, cal_dots, val_dots, cal_form, 
               coeff_num):
    
    # reshape fixation data coressponding do used training dots
    cal_data_reshape = np.ndarray((np.size(cal_dots,0),np.size(ground_truth,0),2))
    cal_data_reshape = cal_data[cal_dots,:,:]
    
    # reshape GT data corresponding do used training dots
    ground_truth_cal_reshape = np.ndarray((np.size(cal_dots,0),np.size(ground_truth,1)))
    ground_truth_cal_reshape = ground_truth[cal_dots,:]
    
    ground_truth_val_reshape = np.ndarray((np.size(val_dots,0),np.size(ground_truth,1)))
    ground_truth_val_reshape = ground_truth[val_dots,:]
    
    # reshape validation data coressponding do used validation dots
    val_data_reshape = np.ndarray((np.size(val_dots,0),np.size(ground_truth,0),2))
    val_data_reshape = val_data[val_dots,:,:]
    
    # calibrate left eye
    cal_coeff_left,cal_form_left = \
        calib_function(cal_data_reshape[:,:,0], ground_truth_cal_reshape, 
                       cal_form, coeff_num);
    cal_grid_left = \
        valid_function(val_data_reshape[:,:,0], cal_coeff_left, cal_form_left)
    # calibrate right eye
    cal_coeff_right,cal_form_right = \
        calib_function(cal_data_reshape[:,:,1], ground_truth_cal_reshape, 
                       cal_form, coeff_num);
    cal_grid_right = \
        valid_function(val_data_reshape[:,:,1], cal_coeff_right, cal_form_right)
    
    #%% calculate mean grid and RMSE
    cal_grid = np.ndarray((np.size(val_dots,0),np.size(cal_form,0),3))
    # left
    cal_grid[:,:,0] = cal_grid_left
    # right
    cal_grid[:,:,1] = cal_grid_right
    # mean: x,y,z
    cal_grid[:,0,2] = np.mean([cal_grid_left[:,0],cal_grid_right[:,0]], axis = 0)
    cal_grid[:,1,2] = np.mean([cal_grid_left[:,1],cal_grid_right[:,1]], axis = 0)
    
    # calculate RMSE and delta z
    cal_diff = np.ndarray((np.size(ground_truth_val_reshape,0),4))
    cal_diff[:,0:np.size(ground_truth,1)] = np.squeeze(cal_grid[:,:,2]) - \
                                            ground_truth_val_reshape
    if np.size(ground_truth,1) == 3:
        cal_diff[:,3] = abs(cal_diff[:,2]);
    else:
        nanarray = np.ndarray((np.size(ground_truth_val_reshape,0),1))
        nanarray.fill(np.nan)
        cal_diff[:,3] = nanarray[:,0]
        
    cal_diff[:,2] = cal_diff[:,0]**2 + cal_diff[:,1]**2
    
    # Output
    cal_coeff = np.ndarray((np.size(cal_form,0),np.size(cal_form[0][:],1),2))
    cal_coeff[:,:,0] = cal_coeff_left[:,:]
    cal_coeff[:,:,1] = cal_coeff_right[:,:]
    
    cal_form = cal_form #[cal_form_left, cal_form_right];
    return cal_coeff, cal_form, cal_grid, cal_diff