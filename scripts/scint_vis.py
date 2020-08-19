"""
Visualization functions for the scint_psd repo.

Patricia Schuster, 2020
"""


import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import plotly.graph_objects as go




def plot_raw_pulses(signal_raw, i_values, plot_with = 'matplotlib'):
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
    plot_with : string
        'matplotlib' (default) or 'plotly'
    
    Returns
    -------
    fig : figure
        Either matplotlib or plotly figure
    """
    
    if len(i_values) > 1:
        title_text = 'Visualizing {} samples'.format(len(i_values))
    else:
        title_text = 'Visualizing sample i = {}'.format(i_values)
    
    
    if plot_with == 'matplotlib':
        fig = plt.figure()
        ax = fig.gca()

        for i in i_values:
            ax.plot(signal_raw[i,:])
            
        plt.xlabel('Sample')
        plt.ylabel('Channel')
        plt.title(title_text)
    
    
    elif plot_with == 'plotly':
        # Add traces
        traces = []
        for i in i_values:
            traces.append(go.Scatter(y = signal_raw[i,:],
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
    
        