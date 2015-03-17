"""
This is the main algorithm which takes time data in the form of a pandas dataframe,
and the frequency vector to calculate the transfer functions at each frequency.
"""

import math

import scipy.signal as sc


# Smallwood Algorithm
def smallwood(df_freq, df_time_data):
    len_freq_vec = df_freq.shape[0]
    t_min = df_time_data.iloc[0, 0]
    t_max = df_time_data.iloc[-1, 0]

    num_pts = df_time_data.shape[0]  # number time data points - CLEAN UP< NOT SURE
    dt = (t_max - t_min) / (num_pts - 1)
    print('Assuming sampling rate of %d' % (1 / dt))
    t_m = (t_max - t_min) + 1 / df_freq.iloc[0, 0]
    t_lim_pts = int(round(t_m / dt))
    num_zeros = t_lim_pts - num_pts
    zeros = [0] * num_zeros

    # create unfiltered response list, append zeros for filtfilt

    yy = (list(df_time_data.iloc[:, 1]) + list(zeros))  # copy row 1append zeros to row

    zeta = 0.05  # aka Q = 10

    srs_resp = []
    a1, a2, b1, b2, b3 = ([] for i in range(5))

    pri_abs = []

    # SRS transfer function calculations
    for freq_idx in range(0, len_freq_vec):
        omega_n = 2 * math.pi * df_freq.iloc[freq_idx, 0]
        omega_d = omega_n * math.sqrt(1 - zeta ** 2)
        E = math.exp(-zeta * omega_n * dt)
        K = omega_d * dt
        C = E * math.cos(K)
        S = E * math.sin(K)
        S_p = S / K

        a1.append(2 * C)
        a2.append(- E ** 2)
        b1.append(1 - S_p)
        b2.append(2 * (S_p - C))
        b3.append(E ** 2 - S_p)

        # transfer functions, each one evaluated at a certain freq
        num = [b1[freq_idx], b2[freq_idx], b3[freq_idx]]
        den = [1, -a1[freq_idx], -a2[freq_idx]]

        y_response = sc.lfilter(num, den, yy)

        pri_max = max(0, max(y_response))
        pri_min = abs(min(0, min(y_response)))
        pri_abs = max(pri_max, pri_min)

        srs_resp.append(pri_abs)

    return srs_resp