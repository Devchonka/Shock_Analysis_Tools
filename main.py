#!usr/bin/python

# prc_error has !! UNRECOGNIZED VALUE !!!! is it as stored parameter in hdf file.

# not sure what that is

import file_operations as fo
import Smallwood as sm
import plotting

def main():
    fname = '3rdFireTestSet.hdf5'
    data = fo.Data()  # create data object that will keep all variables from file, raw and processed
    fo.readFile(fname, data)  # add raw accel readings and time into object

    sm.get_fn(data)  # add freq list into object
    sm.smallwood(data)  # add srs data into obj

    plotting.bokeh_html(data)

if __name__ == "__main__":
    main()

    # print (sample_rate[()])