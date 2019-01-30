# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 07:16:34 2018

@author: P. Wolf

title: calib_main
"""
#%% Imports
from load_pupil import load_pupil
from build_val import build_val
from plot_results import plot_Grid_2D
from plot_results import plot_mask
from plot_results import plot_calib
from pix2deg import pix2deg
import numpy as np
import pickle

#%% shorten Output
class CalibReturnValue(object):
    def __init__(self, fct_in, fct_cfg, csv_data, eye_data, masked_eye_data, 
                 val_eye_data, masked_val_eye_data, cal_coeff, gt_deg, 
                 fixation_cal_data, fixation_val_data, cal_grid, cal_diff):
        self.fct_in = fct_in
        self.fct_cfg = fct_cfg
#        self.csv_data = csv_data
        self.eye_data = eye_data
        self.masked_eye_data = masked_eye_data
        
        self.val_eye_data = val_eye_data
        self.masked_val_eye_data = masked_val_eye_data
        
        self.cal_coeff = cal_coeff
        
        self.gt_deg = gt_deg
        self.fixation_cal_data = fixation_cal_data
        self.fixation_val_data = fixation_val_data
        self.cal_grid = cal_grid
        self.cal_diff = cal_diff

#%% define left and reight based on the used eye
# HTC:        left = id1    right = id0
def change_left_right(use_eye,csv_data):
    if use_eye == 'left':
        print('Using Right Eye')
        # eyedata
        csv_data.id0_eyedata = csv_data.id1_eyedata
        
        # capture_data
        csv_data.id0_capturedata = csv_data.id1_capturedata
        
        # frame_drops
        csv_data.id0_rel_framedrops = csv_data.id1_rel_framedrops
        csv_data.id0_abs_framedrops = csv_data.id1_abs_framedrops
        
        # fps
        csv_data.id0_real_fps = csv_data.id1_real_fps
        
    elif use_eye == 'right':
        print('Using Left Eye')
        # eyedata
        csv_data.id1_eyedata = csv_data.id0_eyedata
        
        # capture_data
        csv_data.id1_capturedata = csv_data.id0_capturedata
        
        # frame_drops
        csv_data.id1_rel_framedrops = csv_data.id0_rel_framedrops
        csv_data.id1_abs_framedrops = csv_data.id0_abs_framedrops
        
        # fps
        csv_data.id1_real_fps = csv_data.id0_real_fps
        
    elif use_eye == 'both':
        print('Using Both Eye')
        # eyedata
        temp_id0_eyedata = csv_data.id0_eyedata
        temp_id1_eyedata = csv_data.id1_eyedata
        
        csv_data.id0_eyedata = temp_id1_eyedata
        csv_data.id1_eyedata = temp_id0_eyedata
        
        # capture_data
        temp_id0_capturedata = csv_data.id0_capturedata
        temp_id1_capturedata = csv_data.id1_capturedata
        
        csv_data.id0_capturedata = temp_id1_capturedata
        csv_data.id1_capturedata = temp_id0_capturedata
        
        # frame_drops
        temp_id0_rel_framedrops = csv_data.id0_rel_framedrops
        temp_id1_rel_framedrops = csv_data.id1_rel_framedrops
        
        csv_data.id0_rel_framedrops = temp_id1_rel_framedrops
        csv_data.id1_rel_framedrops = temp_id0_rel_framedrops
        
        temp_id0_abs_framedrops = csv_data.id0_abs_framedrops
        temp_id1_abs_framedrops = csv_data.id1_abs_framedrops
        
        csv_data.id0_abs_framedrops = temp_id1_abs_framedrops
        csv_data.id1_abs_framedrops = temp_id0_abs_framedrops
        
        # fps
        temp_id0_real_fps = csv_data.id0_real_fps
        temp_id1_real_fps = csv_data.id1_real_fps
        
        csv_data.id0_real_fps = temp_id1_real_fps
        csv_data.id1_real_fps = temp_id0_real_fps
        
    return csv_data
    

#%% main function
def calib_main(fct_cfg, fct_in, screen_cfg):
    #%% dont change these configs
    fix_time = 1
    use_filter = 0
    window_size = 10
    csv_data_input = 'pupil_positions.csv'
    info_input = 'info.csv'
    
    #%% load recorded data
    csv_data = load_pupil(fct_in.data_directory, fct_in.file_date, fct_in.file_num, 
                          csv_data_input, info_input, fix_time, fct_in.set_fps, 
                          use_filter, window_size)
    
    # choose which eye u want to use
    csv_data = change_left_right(fct_in.use_eye,csv_data)
    
    # save recorded data in new array
    # eye_data(t,parameter,eye)
    eye_data = np.ndarray((np.size(csv_data.id0_eyedata,0),np.size(csv_data.id0_eyedata,1),2))
    eye_data[:,:,0] = csv_data.id0_eyedata
    eye_data[:,:,1] = csv_data.id1_eyedata
    
    real_fps = np.ndarray((2,))
    real_fps[0] = csv_data.id0_real_fps
    real_fps[1] = csv_data.id1_real_fps
    
    print('Finished Loading')
    
    #%% change gt_px from pixels to degree (gt_deg)
    gt_deg = np.ndarray((np.shape(fct_in.gt_px)))
    gt_deg[:,0],gt_deg[:,1] = pix2deg(fct_in.gt_px[:,0],fct_in.gt_px[:,1],screen_cfg,'3D')
    
    #%% extract fixation data from eyedata
    # calibration
    mask_cal = np.zeros((np.size(eye_data,0),1), dtype = bool)
    mask_ind_cal_temp = fct_in.mask_ind_cal
    mask_ind_cal_temp[:,0] = mask_ind_cal_temp[:,0] - float(csv_data.info.loc[:,'Start Time (System)'][0])
    fixation_cal_data = np.ndarray((np.size(fct_in.mask_ind_cal,0),2,2))
    # save coordinates to i
    cal_inds = [0] * np.size(fct_in.mask_ind_cal,0)
    for i in range(np.size(mask_ind_cal_temp,0)):
        cal_inds[i] = np.where(eye_data[:,0,0] > mask_ind_cal_temp[i,0])[0][0]
        mask_cal[cal_inds[i]] = 1
    
    fixation_cal_data = eye_data[cal_inds,3:5,:]
    
    # validation
    mask_val = np.zeros((np.size(eye_data,0),1), dtype = bool)
    mask_ind_val_temp = fct_in.mask_ind_val
    mask_ind_val_temp[:,0] = mask_ind_val_temp[:,0] - float(csv_data.info.loc[:,'Start Time (System)'][0])
    fixation_val_data = np.ndarray((np.size(fct_in.mask_ind_val,0),2,2))
    # save coordinates to i
    val_inds = [0] * np.size(fct_in.mask_ind_val,0)
    for i in range(np.size(mask_ind_cal_temp,0)):
        val_inds[i] = np.where(eye_data[:,0,0] > mask_ind_val_temp[i,0])[0][0]
        mask_val[val_inds[i]] = 1
    
    fixation_val_data = eye_data[val_inds,3:5,:]
    
    # change time values in the mask array to integers
    mask_ind_cal = np.ndarray((np.size(cal_inds),4))
    mask_ind_cal[:,0] = cal_inds
    mask_ind_cal[:,1] = cal_inds
    mask_ind_cal[:,2] = mask_ind_cal_temp[:,1]
    mask_ind_cal[:,3] = mask_ind_cal_temp[:,2]
    
    mask_ind_val = np.ndarray((np.size(val_inds),4))
    mask_ind_val[:,0] = val_inds
    mask_ind_val[:,1] = val_inds
    mask_ind_val[:,2] = mask_ind_val_temp[:,1]
    mask_ind_val[:,3] = mask_ind_val_temp[:,2]
    
    # create masked eye_data
    mask = mask_cal | mask_val
    masked_eye_data = eye_data[mask[:,0],:,:]
    
    # calibrate all dots
    cal_coeff,cal_grid,val_eye_data,cal_diff = \
        build_val(eye_data,real_fps,fixation_cal_data,fixation_val_data, 
                  gt_deg,range(np.size(gt_deg,0)),range(np.size(gt_deg,0)),
                  fct_in.cal_form_all,fct_in.coeff_num_all)
    print('Finished Calibrating')
    
    # create mask with val_eye_data
    masked_val_eye_data = val_eye_data[mask[:,0],:,:]
    
    #%% plot results
    if fct_cfg.disp_plots == 1:
        if fct_cfg.disp_what[0] == 1:
            plot_mask(mask_ind_cal, eye_data, masked_eye_data, fct_cfg.save_plots)
        if fct_cfg.disp_what[1] == 1:
            plot_Grid_2D(cal_grid, gt_deg, fct_cfg.save_plots)
        if fct_cfg.disp_what[2] == 1:
            plot_calib(masked_val_eye_data, val_eye_data, gt_deg, cal_grid, fct_cfg.save_plots)
    print('Finished Plotting')
    
    #%% save output data
    fct_out = CalibReturnValue(fct_in, fct_cfg, csv_data, eye_data, masked_eye_data, 
                               val_eye_data, masked_val_eye_data,cal_coeff, gt_deg, 
                               fixation_cal_data, fixation_val_data, cal_grid, cal_diff)
    #%% output
    return fct_out
