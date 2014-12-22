# Functions to do operations on hdf file

def readFile(filename, data):
    import h5py

    f = h5py.File(filename, 'r')

    data._time_data = f['/dru/capture/data']
    data._labels = f['/dru/capture/labels']
    data._sample_rate = f['/dru/capture/rdt/sample_rate']
    data._pga_gain_code = f['/dru/capture/rdt/pga_gain_code']

    # print ("%s\t" % ("time_data"))
    print (data._sample_rate[()])
    f.close()


class Data:
    # constructor
    def __init__(self, time_data=[], labels=[], sample_rate=0, pga_gain_code=0):
        self._time_data = time_data
        self._labels = labels
        self._sample_rate = sample_rate
        self._pga_gain_code = pga_gain_code
        print "Data object created"


def sample_freq(self):
    return 1 / self._sample_rate


def print_sample_rate(self):
    print self._sample_rate


    # destructor
def release(self):
    print "Data object destroyed, memory released"