"""
Main functions for `scint_psd` repo.

Patricia Schuster, 2020
"""

import numpy as np
import scipy.io as sio
import os
import sys




def load_signal_raw(filepath):
    """
    Load data following the structure of the demo data provided in this repo. Each file is a `.mat` file containing a dictionary with the variable `signal_raw`. 
    
    Modify as needed for the structure of your data file. 
    
    Parameters
    ----------
    filepath : str
        Path to the raw data file
        
    
    Returns
    -------
    signal_raw : ndarray
        2-dimensional array of signal, may be raw or tot (baseline-subtracted)
        Shape = (# pulses, # samples)
        Pulse n: signal[n,:]    
    """
    signal_raw = sio.loadmat(filepath)['signal_raw']
    return signal_raw