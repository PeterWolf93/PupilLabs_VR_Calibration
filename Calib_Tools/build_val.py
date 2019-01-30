# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:34:42 2018

@author: P. Wolf

title: build_val
"""
#%% Imports
import numpy as np
from build_grid import build_grid
from valid_function import valid_function

#%% main function
def build_val(eye_data, fps, cal_data, val_data, ground_truth, cal_dots, 
              val_dots, cal_form, coeff_num):
    
    # calibrate with the chosen dots
    cal_coeff, cal_form, cal_grid, cal_diff = \
        build_grid(cal_data, val_data, ground_truth, cal_dots, val_dots, 
                   cal_form, coeff_num)
    
    # validate the whole eyedata and save the calibrated eyedata
    val_eye_data = np.ndarray((np.size(eye_data,0),10,2))
    val_eye_data.fill(np.nan)
    for i in range(2):
        # time, worldframe, confidence
        val_eye_data[:,0:3,i] = eye_data[:,0:3,i]
        # validated x,y,z in °
        if np.size(ground_truth,1) == 3:
            val_eye_data[:,3:6,i] = \
            valid_function(eye_data[:,3:5,i],cal_coeff[:,:,i],cal_form)
        else:
            val_eye_data[:,3:5,i] =  \
            valid_function(eye_data[:,3:5,i],cal_coeff[:,:,i],cal_form)
        
        # pupil diameter
        val_eye_data[:,6,i] = eye_data[:,5,i]
        
        # v_x, v_y, v_z in °/s
        if np.size(ground_truth,1) == 3:
            val_eye_data[:,7:10,i] = \
            np.vstack([[0, 0, 0], np.diff(val_eye_data[:,3:6,i], axis = 0)*fps[i]])
        else:
            val_eye_data[:,7:9,i] = \
            np.vstack([[0, 0], np.diff(val_eye_data[:,3:5,i], axis = 0)*fps[i]])
        
    return cal_coeff, cal_grid, val_eye_data, cal_diff

