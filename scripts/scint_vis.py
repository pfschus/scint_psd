"""
Visualization functions for the scint_psd repo.

Patricia Schuster, 2020
"""


import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import plotly.graph_objects as go

import scint_math as scint_math


def plot_raw_pulses(signal_raw, 
                    i_values, 
                    cfd_shift_frac = 0,
                    plot_with = 'matplotlib'):
    """
    Make a plot of raw pulses.
    
    Parameters
    ----------
    signal_raw : ndarray
        2-dimensional array of signal, may be raw or tot (baseline-subtracted)
        Shape = (# pulses, # samples)
        Pulse n: signal[n,:] 
    i_values : list of ints
        Indices of events you want to visualize
        If you want to plot a single pulse, use [i] to keep list format
    cfd_shift_frac : float
        Fractional amplitude used by cfd for centering pulses
        If 0, do not apply a shift
        Accepts fractions between 0 and 1
        Used to shift the position of the pulses to synchronize rise times
    plot_with : string
        'matplotlib' (default) or 'plotly'
    
    Returns
    -------
    fig : figure
        Either matplotlib or plotly figure
    """
    
    if len(i_values) > 1:
        title_text = 'Visualizing {} raw samples'.format(len(i_values))
    else:
        title_text = 'Visualizing sample i = {}'.format(i_values)
    
    x_values = np.arange(signal_raw.shape[1])
    if cfd_shift_frac > 0:
        b0 = scint_math.cfd(signal_raw, frac = cfd_shift_frac)
    else:
        b0 = np.zeros(signal_raw.shape[0])
    
    if plot_with == 'matplotlib':
        fig = plt.figure()
        ax = fig.gca()

        for i in i_values:
            ax.plot(x_values-b0[i], signal_raw[i,:])
            
        plt.xlabel('Sample')
        plt.ylabel('Channel')
        plt.title(title_text)
    
    
    elif plot_with == 'plotly':
        # Add traces
        traces = []
        for i in i_values:
            traces.append(go.Scatter(x = x_values-b0[i], 
                                     y = signal_raw[i,:],
                                     name = '{}'.format(i)))

        # Set up layout
        layout = go.Layout(title = title_text,
                           showlegend = False,
                           xaxis_title = 'sample',
                           yaxis_title = 'channel',
                           legend_title = 'event index')

        # Combine to figure
        fig = go.Figure(data = traces,
                        layout = layout)

    return fig
    
        