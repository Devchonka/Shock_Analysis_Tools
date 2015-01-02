# Data class and Shock details class

from __future__ import division
import h5py
import math
import numpy as np


# Data class holds raw and processed shock data for plotting
class Data(object):
    def __init__(self, filename):
        f = h5py.File(filename, 'r')
        self._time_data = f['/dru/capture/data'][()]
        self._labels = f['/dru/capture/labels'][()]
        self._sample_rate = int(f['/dru/capture/rdt/sample_rate'][()])
        self._pga_gain_code = f['/dru/capture/rdt/pga_gain_code'][()]

        self.raw_volts, self.spec_interp_db, self.spec_interp_plus9dB, self.spec_interp_plus6dB, \
        self.spec_interp_minus3dB, self.spec_interp_minus6dB = ([] for i in range(6))

        self.get_fn()

        for ch_idx in range(24):
            self.raw_volts.append(self.counts_to_volts(self._time_data[ch_idx + 1], self._pga_gain_code))

    def counts_to_volts(self, x, pga_gain, xducer_scale=0.0005):  # xducer_scale is 0.5 mV/g, temporary per Joe, Mark,Dave 3-27-14
        VREF = 5
        CODES = 32768  # 2^16 /2
        FIXGAIN = 1.75  # Salen-Key filter gain
        return VREF * (x / CODES / FIXGAIN / pga_gain / xducer_scale)

        # Plugs in frequency vector into data obj
    def get_fn(self):
        octave = 1 / 12  # a factor of 2 in frequency (next freq is twice prev) - reduces coupling of test support and electronics
        fn_min = 100
        fn_max = 100000
        n = math.ceil(math.log((fn_max / fn_min), 2) / octave)
        self.srs_fn = fn_min * 2 ** ( octave * np.arange(0.0, n, 1.0))


# Shock details class holds data about shock margin and shock preferences
class ShockDetails(object):
    def __init__(self, name, data):

        if name == 'Level 1':
            lvl = [[200, 4000, 10000], [140, 4200, 4200]]

        srs_data_interp_db = self.extrap([20 * i for i in [math.log10(i) for i in data.srs_fn]],
                                            [20 * i for i in [math.log10(i) for i in lvl[0]]],
                                            [20 * i for i in [math.log10(i) for i in lvl[1]]])
        self.srs_data_interp = [10 ** i for i in [i / 20 for i in srs_data_interp_db]]
        self.name = name
        self.f = lvl[0]
        self.srs_data = lvl[1]

        # Calculations for the level selected and the -3,-6,+6,+9 dB margin to it
        data.spec_interp_db = [20 * i for i in [np.log10(i) for i in self.srs_data_interp]]
        data.spec_interp_plus9dB = [10 ** i1 for i1 in [i / 20 for i in [i2 + 9 for i2 in data.spec_interp_db]]]
        data.spec_interp_plus6dB = [10 ** i1 for i1 in [i / 20 for i in [i2 + 6 for i2 in data.spec_interp_db]]]
        data.spec_interp_minus3dB = [10 ** i1 for i1 in [i / 20 for i in [i2 - 3 for i2 in data.spec_interp_db]]]
        data.spec_interp_minus6dB = [10 ** i1 for i1 in [i / 20 for i in [i2 - 6 for i2 in data.spec_interp_db]]]


# Function to linearly extrapolate outside bounds range
    def extrap(self,x, xp, yp):
        y = np.interp(x, xp, yp)
        for i in range(len(x)):
            if x[i] < xp[0]:
                y[i] = yp[0] + (x[i] - xp[0]) * (yp[0] - yp[1]) / (xp[0] - xp[1])
            elif x[i] > xp[-1]:
                y[i] = yp[-1] + (x[i] - xp[-1]) * (yp[-1] - yp[-2]) / (xp[-1] - xp[-2])
        return y