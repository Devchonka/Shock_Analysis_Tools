# Functions to manipulate original data file and class definition for data object
# import pdb
# pdb.set_trace()

# TO DO:
# Do I need a class destructor to free memory ?


def readFile(filename, data):
    import h5py

    f = h5py.File(filename, 'r')

    data._time_data = f['/dru/capture/data'][()]
    data._labels = f['/dru/capture/labels'][()]
    data._sample_rate = int(f['/dru/capture/rdt/sample_rate'][()])
    data._pga_gain_code = f['/dru/capture/rdt/pga_gain_code'][()]
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
        print "Data object created"
