#!usr/bin/python

import data_manip as dm
import Smallwood as sm
import plotting

def main():
    # Read file and store data in "data" object
    fname = 'DRU_ISDLA1_SPTFire.hdf5'
    data = dm.Data()  # create data object that will keep all variables from file, raw and processed
    dm.readFile(fname, data)  # add raw accel readings and time into object from input file

    # Run smallwood algorithm to process data for SRS
    sm.get_fn(data)  # add freq list into object
    sm.smallwood(data)  # add srs data into obj
    sm.shock_levels(data)  # add margin lines into obj

    # Plot data
    plotting.bokeh_html(data)  # make plots

if __name__ == "__main__":
    main()