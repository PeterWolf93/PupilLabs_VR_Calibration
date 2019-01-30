# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 07:26:07 2018

@author: P. Wolf

title: start_calib
"""
#%% Imports
import numpy as np
from calib_main import calib_main
from load_pickle import load_pickle

#%% Version number
version_num = 'V9'

#%% data path
directory = 'F:\\Arbeit und Uni\\MasterArbeit\\'
# path to the pupil capture data
data_directory = directory + 'Pupil_VR_Recordings\\'
# path to the calibration data from the stimulus script
time_directory = directory + 'HTC_Vive_Recs\\Data\\'

#%% Configurations
disp_plots = 1
# 1. uncalibrated data; 2. GT after calibration
disp_what = [1, 1, 0]

# atm calculated data can't be saved
save_data = 0
# forst check the save directory for the plots
save_plots = 0

#%% choose data set
choose_dataset = 0

if choose_dataset == 0:
    # specify the recording you want to calibrate
    subj_name = 'olbe'
    file_date = '2018_11_20'
    file_num = '001'
    # capture frequency in Hz
    set_fps = 120
    # left; right; both
    use_eye = 'both'
    
#%% load calibration times from pickle file
mask_ind_cal,mask_ind_val = load_pickle(time_directory,subj_name,file_date,file_num)

#%% extract calibration grid
gt_px = mask_ind_cal[:,3:5]

#%% specify dots for calibration and validation
cal_dots = np.linspace(1,np.size(gt_px,0),np.size(gt_px,0));
val_dots = np.linspace(1,np.size(gt_px,0),np.size(gt_px,0));


#%% choose coefficents for design matrix
choose_coeff = 1
if choose_coeff == 1:
    coeff_num_all = 6
    cal_form_all_x = [['1','x','y','x^2','y^2','x*y']]
    cal_form_all_y = [['1','x','y','x^2','y^2','x*y']]
    cal_form_all = [cal_form_all_x, cal_form_all_y]

#%% screen resolutions
screen_width = np.nan
screen_height = np.nan
screen_dist = 1

#%% shorten input data and configs
class CalibConfig(object):
    def __init__(self, disp_plots, disp_what, save_data, save_plots):
        self.disp_plots = disp_plots
        self.disp_what = disp_what
        
        self.save_data = save_data
        self.save_plots = save_plots
        
fct_cfg = CalibConfig(disp_plots, disp_what, save_data, save_plots)

class CalibInputValue(object):
    def __init__(self, coeff_num_all, cal_form_all, version_num, data_directory, 
                 time_directory, subj_name, file_date, file_num, mask_ind_cal, 
                 mask_ind_val, cal_dots, val_dots, gt_px, set_fps, use_eye):
        self.coeff_num_all = coeff_num_all
        self.cal_form_all = cal_form_all
        
        self.version_num = version_num
        self.data_directory = data_directory
        self.time_directory = time_directory
        self.subj_name = subj_name
        self.file_date = file_date
        self.file_num = file_num
        
        self.mask_ind_cal = mask_ind_cal
        self.mask_ind_val = mask_ind_val
        
        self.cal_dots = cal_dots
        self.val_dots = val_dots
        self.gt_px = gt_px
        self.set_fps = set_fps
        self.use_eye = use_eye
        
fct_in = CalibInputValue(coeff_num_all, cal_form_all, version_num, data_directory, 
                 time_directory, subj_name, file_date, file_num, mask_ind_cal, 
                 mask_ind_val, cal_dots, val_dots, gt_px, set_fps, use_eye)

class ScreenConfig(object):
    def __init__(self, screen_width, screen_height, screen_dist):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.screen_dist = screen_dist

screen_cfg = ScreenConfig(screen_width, screen_height, screen_dist)

#%% Output
fct_out = calib_main(fct_cfg,fct_in,screen_cfg)