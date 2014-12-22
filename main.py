#!usr/bin/python

import file_operations as fo
import Smallwood as sm

def main():
    fname = '3rdFireTestSet.hdf5'
    data = fo.Data()
    fo.readFile(fname, data)

    data.srs_fn = sm.get_fn()


    data.srs_gs = sm.smallwood(data._time_data,data.srs_fn)

if __name__ == "__main__":
    main()

    # print (sample_rate[()])