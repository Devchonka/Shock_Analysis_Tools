# Smallwood algorithm for SRS
# Code based on "An Improved Recursive Formula For Calculating Shock Response Spectra" b David O Smallwood
from __future__ import division
import math
import numpy as np
import scipy.signal as sc


def get_fn():
    octave = 1 / 12  # a factor of 2 in frequency (next freq is twice prev) - reduces coupling of test support and electronics
    fn_min = 100
    fn_max = 100000
    n = math.ceil(math.log((fn_max / fn_min), 2) / octave)
    fn = fn_min * 2 ** ( octave * np.arange(0.0, n, 1.0))
    return fn


def smallwood(input, fn):
    t_min = input[0, 0]
    t_max = input[0, -1]
    n = len(input[0])  # number time data points
    dt = (t_max - t_min) / (n - 1)

    t_m = (t_max - t_min) + 1 / fn[0]
    yy = [0] * int(round(t_m / dt))



    for i in range(0, len(input[1])):
        yy[i] = input[1, i]

    zeta = 0.05  # aka Q = 10

    srs_resp = []
    a1, a2, b1, b2, b3 = ([] for i in range(5))
    # SRS transfer function calculations
    for i in range(0, len(fn)):
        omega_n = 2 * math.pi * fn[i]
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
        num = [b1[i], b2[i], b3[i]]
        den = [1, a1[i], a2[i]]

        y_response = sc.filtfilt(num, den, yy)
        # primary response
        pri_max = max(0, max(y_response))
        pri_min = abs(min(0, min(y_response)))
        pri_abs = max(pri_max, pri_min)

        srs_resp.append(pri_abs)
    return srs_resp