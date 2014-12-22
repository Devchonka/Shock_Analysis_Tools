#!usr/bin/python

import file_operations as fo
import Smallwood

def main():
    fname = '3rdFireTestSet.hdf5'
    data = fo.Data()
    fo.readFile(fname, data)

    # octave = 1/octaveLvl
    # n = ceil(log2(maxHz/minHz)/octave)
    # data.srs_fn = minHz*2.^(octave*(0:n))'

    # data.srs_gs = smallwood(data._time_data,fn)

if __name__ == "__main__":
    main()

    # print (sample_rate[()])