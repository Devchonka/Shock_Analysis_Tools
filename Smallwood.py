# Smallwood algorithm for SRS
# Code based on "An Improved Recursive Formula For Calculating Shock Response Spectra" b David O Smallwood

import math
import scipy.signal as sc

# Smallwood Algorithm
def smallwood(data):
    len_ch_vec = len(data.raw_volts)
    len_freq_vec = len(data.srs_fn)
    t_min = data._time_data[0, 0]
    t_max = data._time_data[0, -1]
    num_pts = len(data._time_data[0])  # number time data points
    dt = (t_max - t_min) / (num_pts - 1)
    t_m = (t_max - t_min) + 1 / data.srs_fn[0]
    t_lim_pts = int(round(t_m / dt))
    num_zeros = t_lim_pts - num_pts
    zeros = [0] * num_zeros

    yy = []  # create unfiltered response list of lists, append zeros for filtfilt
    for channel in range(len_ch_vec):  # copy row 1-24 of data, append zeros to each row
        yy.append((list(data.raw_volts[channel]) + list(zeros)))

    zeta = 0.05  # aka Q = 10

    srs_resp = []
    a1, a2, b1, b2, b3 = ([] for i in range(5))

    pri_abs = [[] for x in range(len_ch_vec)]
    y_response = [[] for x in range(len_ch_vec)]

    # SRS transfer function calculations
    for freq_idx in range(0, len_freq_vec):
        omega_n = 2 * math.pi * data.srs_fn[freq_idx]
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

        for channel in range(len_ch_vec):  # primary response
            y_response[channel] = sc.lfilter(num, den, yy[channel])

            pri_max = max(0, max(y_response[channel]))
            pri_min = abs(min(0, min(y_response[channel])))
            pri_abs[channel].append(max(pri_max, pri_min))

    for channel in range(len_ch_vec):
        srs_resp.append(pri_abs[channel])

    data.srs_gs = srs_resp