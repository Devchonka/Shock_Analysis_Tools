# Smallwood algorithm for SRS
# Code based on "An Improved Recursive Formula For Calculating Shock Response Spectra" b David O Smallwood
# Module also contains frequency related functions

from __future__ import division
import math
import numpy as np
import scipy.signal as sc
import data_manip as fo


# Plugs in frequency vector into data obj
def get_fn(data):
    octave = 1 / 12  # a factor of 2 in frequency (next freq is twice prev) - reduces coupling of test support and electronics
    fn_min = 100
    fn_max = 100000
    n = math.ceil(math.log((fn_max / fn_min), 2) / octave)
    data.srs_fn = fn_min * 2 ** ( octave * np.arange(0.0, n, 1.0))


 # Function to linearly extrapolate outside bounds range
def extrap(x, xp, yp):

    y = np.interp(x, xp, yp)
    for i in range(len(x)):
        if x[i] < xp[0]:
            y[i] = yp[0] + (x[i]-xp[0]) * (yp[0]-yp[1]) / (xp[0]-xp[1])
        elif x[i] > xp[-1]:
            y[i]= yp[-1] + (x[i]-xp[-1])*(yp[-1]-yp[-2])/(xp[-1]-xp[-2])

    return y


# Function to return margins to spec in dB
def shock_levels(data):

    lvl = [[200, 4000, 10000], [140, 4200, 4200]]

    srs_data_interp_db = extrap([20 * i for i in [math.log10(i) for i in data.srs_fn]],  # all 3 vec same as matlab
                             [20 * i for i in [math.log10(i) for i in lvl[0]]],
                             [20 * i for i in [math.log10(i) for i in lvl[1]]])

    srs_data_interp = [10 ** i for i in [i / 20 for i in srs_data_interp_db]]

    shock_details = fo.ShockDetails('Level 1', lvl[0], lvl[1], srs_data_interp)

    # Calculations for the level selected and the -3,-6,+6,+9 dB margin to it
    data.spec_interp_db = [20 * i for i in [np.log10(i) for i in shock_details.srs_data_interp]]
    data.spec_interp_plus9dB = [10 ** i1 for i1 in [i / 20 for i in [i2 + 9 for i2 in data.spec_interp_db]]]
    data.spec_interp_plus6dB = [10 ** i1 for i1 in [i / 20 for i in [i2 + 6 for i2 in data.spec_interp_db]]]
    data.spec_interp_minus3dB = [10 ** i1 for i1 in [i / 20 for i in [i2 - 3 for i2 in data.spec_interp_db]]]
    data.spec_interp_minus6dB = [10 ** i1 for i1 in [i / 20 for i in [i2 - 6 for i2 in data.spec_interp_db]]]


# Smallwood Algorithm
def smallwood(data):
    t_min = data._time_data[0, 0]
    t_max = data._time_data[0, -1]
    num_pts = len(data._time_data[0])  # number time data points
    dt = (t_max - t_min) / (num_pts - 1)
    t_m = (t_max - t_min) + 1 / data.srs_fn[0]
    t_lim_pts = int(round(t_m / dt))
    num_zeros = t_lim_pts - num_pts
    zeros = [0] * num_zeros

    yy = []  # create unfiltered response list of lists, append zeros for filtfilt
    for channel in range(24):  # copy row 1-24 of data, append zeros to each row
        yy.append((list(data.raw_volts[channel]) + list(zeros)))

    zeta = 0.05  # aka Q = 10

    srs_resp = []
    a1, a2, b1, b2, b3 = ([] for i in range(5))

    pri_abs = [[] for x in xrange(24)]
    y_response = [[] for x in xrange(24)]

    # SRS transfer function calculations
    for freq_idx in range(0, len(data.srs_fn)):
        omega_n = 2 * math.pi * data.srs_fn[freq_idx]
        omega_d = omega_n * math.sqrt(1 - zeta ** 2)
        E = math.exp(-zeta * omega_n * dt)
        K = omega_d * dt
        C = E * math.cos(K)
        S = E * math.sin(K)
        S_p = S / K

        a1.append(2 * C)
        a2.append(- E**2)
        b1.append(1 - S_p)
        b2.append(2 * (S_p - C))
        b3.append(E**2 - S_p)

        # transfer functions, each one evaluated at a certain freq
        num = [b1[freq_idx], b2[freq_idx], b3[freq_idx]]
        den = [1, -a1[freq_idx], -a2[freq_idx]]

        for channel in range(24):  # primary response
            y_response[channel] = sc.lfilter(num,den,yy[channel])

            pri_max = max(0, max(y_response[channel]))
            pri_min = abs(min(0, min(y_response[channel])))
            pri_abs[channel].append(max(pri_max, pri_min))

    for channel in range(24):
        srs_resp.append(pri_abs[channel])

    data.srs_gs = srs_resp