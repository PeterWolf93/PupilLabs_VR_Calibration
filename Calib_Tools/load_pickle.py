# -*- coding: utf-8 -*-
"""
Created on Tue Feb 27 13:16:58 2018

@author: VRLab
"""
import pickle
import numpy as np

def load_pickle(directory,subj_name,file_date,file_num):
    name_list = ['_calib_', '_valid_']
    path = directory + subj_name + '/'
    for j in range(2):
        file_name_cal = subj_name + name_list[j] + file_date + '_' + file_num
        load_temp = pickle.load(open(path + file_name_cal + '.p', 'rb'))
        data_temp = np.zeros((np.size(load_temp[0],0),5))
        data_temp[:,0:1] = np.asarray(load_temp[0])
        data_temp[:,3:5] = np.asarray(load_temp[1][:,0:2])
        
        # assign a number to each datapoint and sort by time
        data_temp[:,2] = np.linspace(1,np.size(load_temp[0],0),np.size(load_temp[0],0))
        data_temp = data_temp[data_temp[:,0].argsort()]
        
        # assign an order to each datapoint and sort by the number of each datapoint
        data_temp[:,1] = np.linspace(1,np.size(load_temp[0],0),np.size(load_temp[0],0))
        data_temp = data_temp[data_temp[:,2].argsort()]
        
        if j == 0:
            calib_data = data_temp
        elif j == 1:
            valid_data = data_temp
            
    return calib_data,valid_data