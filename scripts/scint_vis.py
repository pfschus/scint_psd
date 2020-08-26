"""
Visualization functions for the scint_psd repo.

Patricia Schuster, 2020
"""


import numpy as np
import os
import sys
import matplotlib
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
    cfd_shift_frac : float, optional
        Fractional amplitude used by cfd for centering pulses
        If 0, do not apply a shift
        Accepts fractions between 0 and 1
        Used to shift the position of the pulses to synchronize rise times
    plot_with : string, optional
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
        i_p = scint_math.cfd(signal_raw, frac = cfd_shift_frac)
    else:
        i_p = np.zeros(signal_raw.shape[0])
    
    if plot_with == 'matplotlib':
        fig = plt.figure()
        ax = fig.gca()

        for i in i_values:
            ax.plot(x_values-i_p[i], signal_raw[i,:])
            
        plt.xlabel('Sample')
        plt.ylabel('Channel')
        plt.title(title_text)
    
    
    elif plot_with == 'plotly':
        # Add traces
        traces = []
        for i in i_values:
            traces.append(go.Scatter(x = x_values-i_p[i], 
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
    
def plot_L_ch_vs_S(L_ch, S, nbins = 100, plot_with = 'matplotlib'):
    """
    Create two-dimensional heatmap of L vs. S, also called a "PSD Plot"
    
    Parameters
    ----------
    L_ch : ndarray
        Light output values in integrated digitizer channel units
        As calculated by scint.calc_L_ch
    S : ndarray
        Pulse shape parameter, using the tail-to-total method  
        As calculated by scint.calc_S    
    nbins : int, optional
        Number of bins on each axis
    plot_with : string, optional
        'matplotlib' (default) or 'plotly'
    
    Returns
    -------
    fig : figure
        Either matplotlib or plotly figure
    """
    
    if plot_with == 'matplotlib':
        fig = plt.figure()
        plt.hist2d(L_ch,S,bins=nbins,norm=matplotlib.colors.LogNorm())
        plt.colorbar()
        plt.xlabel('Light output (IDCU)')
        plt.ylabel('S (tail-to-total)')

    if plot_with == 'plotly':
        # Set up colorscale
        colorscale = create_log_colorscale()

        trace = go.Histogram2d(x = L_ch,
                               y = S,
                               nbinsx = nbins,
                               nbinsy = nbins,
                               colorscale = colorscale)

        layout = go.Layout(title = 'PSD Plot',
                           xaxis_title = 'Light output (IDCU)',
                           yaxis_title = 'S (tail-to-total)')

        fig = go.Figure(data = trace,
                        layout = layout)

    return fig
        
def create_log_colorscale(log_base = 2.7):
    """
    Generate and return a logarithmic colorscale, intended for PSD Plot
    
    Parameters
    ----------
    log_base : float, optional
        Base for log scale
        
    Returns
    -------
    colorscale : plotly colorscale
        Colorscale for PSD plot
    """
    log_base = 2.7
    i_logs = 1-np.flip(np.logspace(-log_base,0,num=50,base=log_base))
    i_lins = np.arange(0.02,1.02,.02)

    viridis = matplotlib.cm.get_cmap('viridis')

    colorscale = [[0,'rgb(255,255,255)']]
    for i_log, i_lin in zip(i_logs, i_lins):
        
        this_color = viridis(i_log)
        rgb_string = 'rgb({:.2f},{:.2f},{:.2f})'.format(
                           255*this_color[0],
                           255*this_color[1],
                           255*this_color[2])
        colorscale.append([i_lin, rgb_string])
        
    return colorscale



