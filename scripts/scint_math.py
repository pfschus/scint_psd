"""
Math functions for supporting the scint library

Patricia Schuster, 2020
"""

import numpy as np

def cfd(signal_tot, frac = 0.5):
    """
    Constant fraction discriminator: Find the sample number at which each pulse exceeds relative amplitude frac.
    
    Parameters
    ----------
    signal_tot : ndarray
        2-dimensional array of signal_tot (baseline-subtracted)
    frac : float    
    
    Returns
    -------
    b0 : ndarray
        Sub-sample positions of where each pulse crosses frac
    """
    # Calculate relative amplitude pulses
    max_vals = np.amax(signal_tot,axis=1)
    signal_rel = (signal_tot.T/max_vals).T

    # Calculate sub-sample position where each pulse crosses frac
    b0 = np.zeros(signal_tot.shape[0])
    
    # This is not the most efficient way of accomplishing this, but it works
    for p in np.arange(0,signal_rel.shape[0]):
        b2 = np.min(np.argwhere(signal_rel[p,:] > frac))
        b1 = b2-1

        a2 = signal_rel[p,b2]
        a1 = signal_rel[p,b1]
        a0 = frac

        b0[p] = linear_interp(a1,b1,a2,b2,a0, print_flag=False)
        
    return b0


def linear_interp(a1, b1, a2, b2, a0, print_flag = True):
    """
    Used to interpolate between two points on a graph
    Known points: (a1, b1) and (a2, b2)
    For a0, what is b0? Use b0 = b1 + (b2 - b1) * (a0 -a1)/(a2-a1)
    
    Parameters
    ----------
    a1 : float
    b1 : float
    a2 : float
    b2 : float
    a0 : float
    
    Returns
    -------
    b0 : float
    """
    if np.logical_and(a1 == a2, print_flag):
        print('Warning in linear interpolation: a1 == a2.')

    if a1 != a2:
        b0 = b1 + (b2 - b1) * (a0 -a1)/(a2-a1)
    else: # If divide by zero due to a2=a1
        b0 = b1 
        
        
        
    return b0