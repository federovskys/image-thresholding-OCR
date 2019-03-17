#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 16 17:42:52 2019

@author: pedrofRodenas
"""

import cv2
import numpy as np
import argparse
import ntpath
import os


def adaptative_thresholding(path, threshold):
    
    # Load image
    I = cv2.imread(path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(I, cv2.COLOR_BGR2GRAY)
    
    # Original image size
    orignrows, origncols = gray.shape
    
    # Windows size
    M = int(np.floor(orignrows/16) + 1)
    N = int(np.floor(origncols/16) + 1)
    
    # Image border padding related to windows size
    Mextend = round(M/2)-1
    Nextend = round(N/2)-1
    
    # Padding image
    aux =cv2.copyMakeBorder(gray, top=Mextend, bottom=Mextend, left=Nextend,
                          right=Nextend, borderType=cv2.BORDER_REFLECT)
    
    windows = np.zeros((M,N),np.int32)
    
    # Image integral calculation
    imageIntegral = cv2.integral(aux, windows,-1)
    
    # Integral image size
    nrows, ncols = imageIntegral.shape
    
    # Memory allocation for mean image
    result = np.zeros((orignrows, origncols))
    
    # Image cumulative pixels in windows size calculation
    for i in range(nrows-M):
        for j in range(ncols-N):
        
            result[i, j] = imageIntegral[i+M, j+N] - imageIntegral[i, j+N]+ imageIntegral[i, j] - imageIntegral[i+M,j]
     
    # Output binary image memory allocation    
    binar = np.ones((orignrows, origncols), dtype=np.bool)
    
    # Gray image weighted by windows size
    graymult = (gray).astype('float64')*M*N
    
    # Output image binarization
    binar[graymult <= result*(100.0 - threshold)/100.0] = False
    
    # binary image to UINT8 conversion
    binar = (255*binar).astype(np.uint8)
    
    return binar


if __name__ == '__main__':                
    parser = argparse.ArgumentParser(description='applies adaptative binarization and saves output.')
    parser.add_argument('-i', '--input_path', dest="input_path", type=str, required=True, help="image path")
    parser.add_argument("-t", "--threshold", dest='threshold', type=float, default=25, help="binarization threshold")
    
    args = parser.parse_args()

    if not os.path.exists(args.input_path):
        raise IOError('input file does not exit')
    
    if not  0 < args.threshold < 100:
        raise IOError('threshold must be between 0 and 100')
        
    
    output = adaptative_thresholding(args.input_path, args.threshold)
    
    imgname = ntpath.basename(args.input_path)

    cv2.imwrite(os.path.splitext(imgname)[0]+'_bin'+os.path.splitext(imgname)[1], output)
        
    