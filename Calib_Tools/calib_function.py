# -*- coding: utf-8 -*-
"""
Created on Fri Jul 27 10:59:59 2018

@author: P. Wolf

title: calib_function
"""
#%% Imports
import numpy as np
from sklearn.linear_model import LinearRegression

#%% main function
def calib_function(input_data, ground_truth, cal_form, coeff_num):
    # create deisgn matrix
    design_X = np.ndarray((np.size(input_data,0),np.size(cal_form[0][:],1),np.size(cal_form,0)))
    for i in range(np.size(cal_form,0)):
        x_comp = np.ndarray((np.size(input_data,0),np.size(cal_form[0][:],1)))
        for j in range(np.size(cal_form[0][:],1)):
            if cal_form[i][0][j] == '1':
                x_comp[:,j] = \
                np.ones((np.size(input_data,0),))
            elif cal_form[i][0][j] == 'x':
                x_comp[:,j] = \
                input_data[:,0]
            elif cal_form[i][0][j] == 'x^2':
                x_comp[:,j] = \
                input_data[:,0]**2
            elif cal_form[i][0][j] == 'x^3':
                x_comp[:,j] = \
                input_data[:,0]**3
            elif cal_form[i][0][j] == 'y':
                x_comp[:,j] = \
                input_data[:,1]
            elif cal_form[i][0][j] == 'y^2':
                x_comp[:,j] = \
                input_data[:,1]**2
            elif cal_form[i][0][j] == 'y^3':
                x_comp[:,j] = \
                input_data[:,1]**3
            elif cal_form[i][0][j] == 'x*y':
                x_comp[:,j] = \
                input_data[:,0]*input_data[:,1]
            elif cal_form[i][0][j] == 'x^2*y':
                x_comp[:,j] = \
                input_data[:,0]**2*input_data[:,1]
            elif cal_form[i][0][j] == 'x*y^2':
                x_comp[:,j] = \
                input_data[:,0]*input_data[:,1]**2
            elif cal_form[i][0][j] == 'x^2*y^2':
                x_comp[:,j] = \
                input_data[:,0]**2*input_data[:,1]**2
            elif cal_form[i][0][j] == '0':
                x_comp[:,j] = \
                np.zeros((np.size(input_data,0),))
            
        design_X[:,:,i] = x_comp[:,:]
    
    cal_coeff = np.ndarray((np.size(cal_form,0),np.size(cal_form[0][:],1)))
    design_Y = ground_truth
    
    for i in range(np.size(cal_form,0)):
        x_eye = design_X[:,:,i]
        y_eye = design_Y[:,i]
        regressor = LinearRegression(fit_intercept = False)
        regressor.fit(x_eye, y_eye)
        cal_coeff[i,:] = regressor.coef_
    
    cal_form = cal_form
    
    return cal_coeff, cal_form
