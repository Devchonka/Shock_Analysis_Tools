# Smallwood algorithm for SRS
# Code based on "An Improved Recursive Formula For Calculating Shock Response Spectra" b David O Smallwood
from __future__ import division
import math
import numpy as np
import scipy.signal as sc
import control


def get_fn(data):
    octave = 1 / 12  # a factor of 2 in frequency (next freq is twice prev) - reduces coupling of test support and electronics
    fn_min = 100
    fn_max = 100000
    n = math.ceil(math.log((fn_max / fn_min), 2) / octave)
    data.srs_fn = fn_min * 2 ** ( octave * np.arange(0.0, n, 1.0))



def smallwood(data):  # input is nxm 2D array, where first row is time and the rest are accel readings
    t_min = data._time_data[0, 0]
    t_max = data._time_data[0, -1]
    num_pts = len(data._time_data[0])  # number time data points
    dt = (t_max - t_min) / (num_pts - 1)
    t_m = (t_max - t_min) + 1 / data.srs_fn[0]
    t_lim_pts = int(round(t_m / dt))
    num_zeros = t_lim_pts - num_pts
    zeros = [0] * num_zeros

    yy = []  # create unfiltered response list of lists, append zeros for filtfilt
    for channel in range(1, 25):  # copy row 1-24 of data, append zeros to each row
        yy.append((list(data._time_data[channel]) + list(zeros)))


    zeta = 0.05  # aka Q = 10

    srs_resp = []
    data.tf = []
    a1, a2, b1, b2, b3 = ([] for i in range(5))

    # pri_max, pri_min, pri_abs = ([[] for x in xrange(24)] for i in range(3))

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

        a1.append(- 2 * C)
        a2.append(E**2)
        b1.append(1 - S_p)
        b2.append(2 * (S_p - C))
        b3.append(E**2 - S_p)

        # transfer functions
        num = [b1[freq_idx], b2[freq_idx], b3[freq_idx]]
        den = [1, a1[freq_idx], a2[freq_idx]]

        data.tf.append(control.tf(num, den))

        for channel in range(24):  # primary response
            y_response[channel] = sc.filtfilt(num, den, yy[channel])

            # pri_max[channel].append(max(0, max(y_response[channel])))
            # pri_min[channel].append(abs(min(0, min(y_response[channel]))))
            pri_max = max(0, max(y_response[channel]))
            pri_min = abs(min(0, min(y_response[channel])))
            pri_abs[channel].append(max(pri_max, pri_min))

    for channel in range(24):
        srs_resp.append(pri_abs[channel])

    data.srs_gs = srs_resp