#!usr/bin/python

import data_manip as dm
import Smallwood as sm
import plotting


def main():
    # Read file and store data in "data" object
    fname = 'DRU_ISDLA1_SPTFire.hdf5'
    data = dm.Data(fname)  # create data object that will keep all variables from file, raw and processed

    # Run smallwood algorithm to process data for SRS
    sm.smallwood(data)  # add srs data into obj

    shock_name = 'Level 1'  # set by GUI
    dm.ShockDetails(shock_name, data)  # add margin lines into obj

    # Plot data
    plotting.bokeh_html(data)  # make plots


if __name__ == "__main__":
    main()