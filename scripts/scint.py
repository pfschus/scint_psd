"""
Main functions for `scint_psd` repo.

Patricia Schuster, 2020
"""

import numpy as np
import scipy.io as sio
import os
import sys

import scint_math as scint_math


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
    
    
    
def calc_L_ch(signal_tot, Delta_0 = 10, Delta_2 = 100, cfd_frac = None):
    """
    Calculate the light output in integrated digitizer channel units, L_ch, from the baseline-subtracted signal, signal_tot.
    If no sample parameters are provided, simply sum the entire pulse. Otherwise, provide:
        - Delta_0, Delta_2, window boundaries relative to i_p
    
    Parameters
    ----------
    signal_tot : ndarray
        2-dimensional array of signal_tot (baseline-subtracted)
    Delta_0 : int, optional
        Window between i_p and starting sample
    Delta_2 : int, optional
        Window between i_p and ending sample
    cfd_frac : float, optional
        Fraction for cfd calculation to locate rise time of pulse
        If provided, calculate sum between [i_p-Delta_0:i_p+Delta_2] range
    
    Returns
    -------
    L_ch : ndarray
        Light output values in integrated digitizer channel units   
    """    
    # Note: These if statements are pretty sloppy. Should improve them.
    
    if cfd_frac == None: # Simply sum entire pulse
        L_ch = np.sum(signal_tot, axis=1)

    else: # Use ranges relative to i_p
        [num_pulses, pulse_length] = signal_tot.shape
    
        # Set up integration regions
        i_p = scint_math.cfd(signal_tot, cfd_frac)
        
        # Calculate boundary samples, correct any out of range
        i_0 = i_p - Delta_0
        i_0[i_0 < 0] = 0
        i_2 = i_p + Delta_2
        i_2[i_2 > pulse_length - 1] = pulse_length - 1
        
        # Iterate through pulses and calculate L
        L_ch = np.zeros(num_pulses)
        for i in np.arange(num_pulses):        
            L_ch[i] = scint_math.sum_pulse_region(
                          signal_tot[i,:],
                          i_0[i],
                          i_2[i])
        
    return L_ch
    
def calc_S(signal_tot, 
           Delta_1, 
           Delta_2, 
           Delta_0 = 10, 
           cfd_frac = 0.5):
    """
    Calculate the pulse shape from the baseline-subtracted signal, signal_tot.
    
    Parameters
    ----------
    signal_tot : ndarray
        2-dimensional array of signal_tot (baseline-subtracted)
    Delta_1 : int
        Window between i_p and start sample of tail region
    Delta_2 : int
        Window between i_p and ending sample of tail and total regions
    Delta_0 : int, optional
        Window between i_p and starting sample
    cfd_frac : float, optional
        Fraction for cfd calculation to locate rise time of pulse
    
    Returns
    -------
    S : ndarray
        Pulse shape parameter, using the tail-to-total method  
    """    
    [num_pulses, pulse_length] = signal_tot.shape
    
    # Set up integration regions
    i_p = scint_math.cfd(signal_tot, cfd_frac)
    
    # Calculate boundary samples, correct any out of range
    i_0 = i_p - Delta_0
    i_0[i_0 < 0] = 0
    i_1 = i_p + Delta_1
    i_1[i_1 > pulse_length - 1] = pulse_length - 1
    i_2 = i_p + Delta_2
    i_2[i_2 > pulse_length - 1] = pulse_length - 1
    
    # Iterate through pulses and calculate L
    S = np.zeros(num_pulses)
    for i in np.arange(num_pulses):        
        total = scint_math.sum_pulse_region(
                      signal_tot[i,:], i_0[i], i_2[i])
        tail = scint_math.sum_pulse_region(
                      signal_tot[i,:], i_1[i], i_2[i])
        S[i] = np.divide(tail,total)
        
    return S