# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 11:01:09 2018

@author: P. Wolf

title: valid_function
"""
#%% Imports
import numpy as np

#%% main function
def valid_function(input_data,cal_coeff,cal_form):
    output_val = np.ndarray((np.size(input_data,0),np.size(cal_form,0)))
    for i in range(np.size(cal_form,0)):
        val_comp = np.ndarray((np.size(input_data,0),np.size(cal_form[0][:],1)))
        for j in range(np.size(cal_form[0][:],1)):
            if cal_form[i][0][j] == '1':
                val_comp[:,j] = \
                cal_coeff[i,j] * np.ones((np.size(input_data,0),))
            elif cal_form[i][0][j] == 'x':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]
            elif cal_form[i][0][j] == 'x^2':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]**2
            elif cal_form[i][0][j] == 'x^3':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]**3
            elif cal_form[i][0][j] == 'y':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,1]
            elif cal_form[i][0][j] == 'y^2':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,1]**2
            elif cal_form[i][0][j] == 'y^3':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,1]**3
            elif cal_form[i][0][j] == 'x*y':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]*input_data[:,1]
            elif cal_form[i][0][j] == 'x^2*y':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]**2*input_data[:,1]
            elif cal_form[i][0][j] == 'x*y^2':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]*input_data[:,1]**2
            elif cal_form[i][0][j] == 'x^2*y^2':
                val_comp[:,j] = \
                cal_coeff[i,j] * input_data[:,0]**2*input_data[:,1]**2
            elif cal_form[i][0][j] == '0':
                val_comp[:,j] = \
                cal_coeff[i,j] * np.zeros((np.size(input_data,0),))
    
        output_val[:,i] = np.sum(val_comp[:,:], axis = 1)
    return output_val
