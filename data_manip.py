# PART 1: Functions to manipulate original data file and class definition for data object
# PART 2: Function helpers for plotting

# PART 1: Functions to manipulate original data file and class definition for data object
import h5py


class Data:

    def __init__(self):
        self._sample_rate = 0
        self._pga_gain_code = 0
        self._time_data, self._labels, self.raw_volts, self.spec_interp_db, \
        self.spec_interp_plus9dB, self.spec_interp_plus6dB, self.spec_interp_minus3dB, \
        self.spec_interp_minus6dB, self.srs_fn = ([] for i in range(9))


def readFile(filename, data):
    print "Data object called by read file"

    f = h5py.File(filename, 'r')

    data._time_data = f['/dru/capture/data'][()]
    data._labels = f['/dru/capture/labels'][()]
    data._sample_rate = int(f['/dru/capture/rdt/sample_rate'][()])
    data._pga_gain_code = f['/dru/capture/rdt/pga_gain_code'][()]

    for ch_idx in range(24):
        data.raw_volts.append(counts_to_volts(data._time_data[ch_idx+1],data._pga_gain_code))


class ShockDetails:
    def __init__(self,name,f,srs_data, srs_data_interp):
        self.name = name
        self.f = f
        self.srs_data = srs_data
        self.srs_data_interp = srs_data_interp

# PART 2: Function helpers for plotting

def counts_to_volts (x, pga_gain, xducer_scale=0.0005):  # xducer_scale is 0.5 mV/g, temporary per Joe, Mark,Dave 3-27-14
    VREF = 5
    CODES = 32768  # 2^16 /2
    FIXGAIN = 1.75  # Salen-Key filter gain
    return VREF * (x / CODES / FIXGAIN / pga_gain / xducer_scale)