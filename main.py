#!usr/bin/python

import file_operations as fo
import Smallwood as sm
import plotting

def main():
    fname = 'DRU_ISDLA1_SPTFire.hdf5'
    data = fo.Data  # create data object that will keep all variables from file, raw and processed
    fo.readFile(fname, data)  # add raw accel readings and time into object from input file

    sm.get_fn(data)  # add freq list into object
    sm.smallwood(data)  # add srs data into obj
    sm.shock_levels(data)  # add margin lines into obj

    plotting.bokeh_html(data)  # make plots

if __name__ == "__main__":
    main()