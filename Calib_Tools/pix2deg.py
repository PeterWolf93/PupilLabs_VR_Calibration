# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 10:58:17 2018

@author: P. Wolf

title: pix2deg
"""
#%% Imports
import numpy as np

#%% main function
def pix2deg(x_px,y_px,cfg,mode):
    if mode == '2D':
        x_rad = np.arctan((x_px * cfg.screen_width)/(cfg.screen_xres * cfg.screen_dist))
        y_rad = np.arctan((y_px * cfg.screen_height)/(cfg.screen_yres * cfg.screen_dist))
        
        x_deg = x_rad / np.pi * 180
        y_deg = y_rad / np.pi * 180
    elif mode == '3D':
        x_rad = np.arctan(x_px / cfg.screen_dist)
        y_rad = np.arctan(y_px / cfg.screen_dist)
        
        x_deg = x_rad / np.pi * 180
        y_deg = y_rad / np.pi * 180
    return x_deg, y_deg
