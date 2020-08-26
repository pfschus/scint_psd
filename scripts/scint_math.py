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
    
    
def interp_area(pulse, a0, direction):
    """
    Calculate the area, using the trapezoidal rule, of the region between a sub-sample position and the sample above or below it.
    
    Parameters
    ----------
    pulse : ndarray
        A single pulse
    a0 : float
        Sub-sample position for interpolation
    direction : str
        'above' or 'below,' indicating the direction of the area to calculate
        
    Returns
    -------
    area : float
        Area of region between a_0 and sample 'above' or 'below it.        
    """
    # If a0 is an integer, do not calculate a sub-sample area. Return 0
    if np.floor(a0) == a0:
        area = 0
    else:    
        # Interpolate to find sub-sample pulse amplitude
        a1 = int(np.floor(a0)); a2 = int(np.ceil(a0));
        b1 = pulse[a1];         b2 = pulse[a2];
        b0 = linear_interp(a1, b1, a2, b2, a0, False);
        
        # Calculate the area
        if direction == 'above':
            area = .5*(a2-a0)*(b2+b0)
        elif direction == 'below':
            area = .5*(a0-a1)*(b0+b1)
        else:   
            print('Error, direction unknown')
        
    return area
    
    
def sum_pulse_region(pulse, i_start, i_end):
    """
    Sum the area of the pulse from i_start to i_end, which may be integers or floats, indicating sub-sample positions as calculated using cfd. 
    
    Parameters
    ----------
    pulse : ndarray
        A single pulse
    i_start : float
        Beginning of sample range to sum
    i_end : float
        End of sample range to sum
        
    Returns
    -------
    pulse_sum : float
        Sum of pulse from i_start to i_end    
    """
    
    # Interpolate sub-sample area for i_start
    sum_start = interp_area(pulse, i_start, 'above')
    # Sum area between nearest samples to i_start and i_end
    sum_middle = np.sum(pulse[int(np.ceil(i_start)):
                              int(np.floor(i_end))])
    # Interpolate sub-sample area for i_end
    sum_end   = interp_area(pulse, i_end, 'below')
    # Add them all together
    pulse_sum = sum_start + sum_middle + sum_end
    return pulse_sum
    
    
def find_in_range(x, x_min, x_max, y, y_min, y_max):
    """
    Find all indices at which x is within [x_min,x_max] and y is within [y_min,y_max].
    
    Intended for selecting events within given L, S ranges.    
    
    Parameters
    ----------
    x : ndarray
    x_min : float
    x_max : float
    y : ndarray
    y_min : float
    y_max : float    
    
    Returns
    -------
    indices : ndarray
    """
    ind_x = np.where((x > x_min) & (x < x_max))
    ind_y = np.where((y > y_min) & (y < y_max))

    indices = np.intersect1d(ind_x,ind_y)

    return indices
    