# PART 1: Functions to manipulate original data file and class definition for data object
# PART 2: Function helpers for plotting

# PART 1: Functions to manipulate original data file and class definition for data object

def readFile(filename, data):
    import h5py

    f = h5py.File(filename, 'r')

    data._time_data = f['/dru/capture/data'][()]
    data._labels = f['/dru/capture/labels'][()]
    data._sample_rate = int(f['/dru/capture/rdt/sample_rate'][()])
    data._pga_gain_code = f['/dru/capture/rdt/pga_gain_code'][()]

    # data.raw_volts = [[] for x in xrange(24)]
    data.raw_volts = []
    for ch_idx in range(24):
        data.raw_volts.append(counts_to_volts(data._time_data[ch_idx+1],data._pga_gain_code))
    # f.close() #- cannot close till end of execution


class Data:
    # constructor
    def __init__(self, time_data=None, labels=None, sample_rate=0, pga_gain_code=0):
        if time_data is None:
            time_data = []
            labels = []
        self._time_data = time_data
        self._labels = labels
        self._sample_rate = sample_rate
        self._pga_gain_code = pga_gain_code


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