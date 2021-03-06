# Data class and Shock details class

from __future__ import division
import h5py
import math
import numpy as np
import xlrd


# Data class holds raw and processed shock data for plotting
class Data(object):
    def __init__(self, filename):
        try:
            f = h5py.File(filename, 'r')
        except IOError:
            print ('Error in opening file.')
        else:
            with f:
                self._time_data = f['/dru/capture/data'][()]
                self._labels = f['/dru/capture/labels'][()]
                self._sample_rate = int(f['/dru/capture/rdt/sample_rate'][()])
                self._pga_gain_code = f['/dru/capture/rdt/pga_gain_code'][()]

                self.raw_volts, self.spec_interp_db, self.spec_interp_plus9dB, self.spec_interp_plus6dB, \
                self.spec_interp_minus3dB, self.spec_interp_minus6dB, self.srs_gs = ([] for i in range(7))

                self.srs_fn = self.get_fn()

                for ch_idx in range(len(self._labels) - 1):  # subtracting time label
                    self.raw_volts.append(self.counts_to_volts(self._time_data[ch_idx + 1], self._pga_gain_code))

    def counts_to_volts(self, x, pga_gain,
                        xducer_scale=0.0005):  # xducer_scale is 0.5 mV/g, temporary per Joe, Mark,Dave 3-27-14
        VREF = 5
        CODES = 32768  # 2^16 /2
        FIXGAIN = 1.75  # Salen-Key filter gain
        return VREF * (x / CODES / FIXGAIN / pga_gain / xducer_scale)


    def get_fn(self):
        """Method generates frequency vector for data class"""
        octave = 1 / 12  # a factor of 2 in frequency (next freq is twice prev) - reduces coupling of test support and electronics
        fn_min = 100
        fn_max = 100000
        n = math.ceil(math.log((fn_max / fn_min), 2) / octave)
        return fn_min * 2 ** ( octave * np.arange(0.0, n, 1.0))


class ShockDetails(object):
    """Shock details class holds data about shock margin and shock preferences"""
    def __init__(self, name, data):

        lvl = self.get_shock_levels(name)

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
    def extrap(self, x, xp, yp):
        y = np.interp(x, xp, yp)
        for i in range(len(x)):
            if x[i] < xp[0]:
                y[i] = yp[0] + (x[i] - xp[0]) * (yp[0] - yp[1]) / (xp[0] - xp[1])
            elif x[i] > xp[-1]:
                y[i] = yp[-1] + (x[i] - xp[-1]) * (yp[-1] - yp[-2]) / (xp[-1] - xp[-2])
        return y

    def get_shock_levels(self, name):  # For future : name should be used to search spreadsheet
        path = "shock_levels.xlsx"
        book = xlrd.open_workbook(path)
        # print book.nsheets
        # print book.sheet_names()
        sheet = book.sheet_by_index(0)  # selecting first sheet in spreadsheet
        # print first_sheet.row_values(0)
        # cell = sheet.cell(0,0)
        name = sheet.cell(0, 0).value
        lvl = [[sheet.cell(1, 0).value, sheet.cell(2, 0).value, sheet.cell(3, 0).value],
               [sheet.cell(1, 1).value, sheet.cell(2, 1).value, sheet.cell(3, 1).value]]
        return lvl