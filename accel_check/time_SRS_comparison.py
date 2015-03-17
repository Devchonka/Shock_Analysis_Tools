"""
This is the executable function of this quick analysis script.

This function plots the time and SRS data obtained from a commercial system and plots
it against a calculated SRS spectrum based on the time data to compare the validity of
the provided frequency domain data.

Algorithm to convert time data to frequency content is the Smallwood Algorithm.

The input to this function is an excel file with data in a certain arbitrarily chosen format.
The output of this function is an html website interactive in its plots for the user.

"""
from pandas import read_csv

import plotting
import smallwood as sm


def read_data(fname):
    with open(fname) as text:
        data_frame = read_csv(fname, sep='\t', lineterminator='\n', header=0)

        df_freq = data_frame[['predyn_f', 'predyn_f_data', 'postdyn_f_data']].dropna()
        df_predyn_time = data_frame[['predyn_t', 'predyn_t_data']].dropna()
        df_predyn_time['predyn_t'] = df_predyn_time['predyn_t'] - df_predyn_time.ix[0, 'predyn_t']

        df_postdyn_time = data_frame[['postdyn_t', 'postdyn_t_data']].dropna()
        df_postdyn_time['postdyn_t'] = df_postdyn_time['postdyn_t'] - df_postdyn_time.ix[0, 'postdyn_t']

    return df_freq, df_predyn_time, df_postdyn_time


def main():
    accel_name = 'A477Z - SE EDAPM HD, Z'
    predyn_date = 'NBNCo-1A - EAST BDRS PreDyn - 12/12/2014'
    postdyn_date = 'NBNCo-1A - EAST BDRS PostDyn - 1/12/2015'
    fname = 'A477Z.txt'
    df_freq, df_predyn_time, df_postdyn_time = read_data(fname)
    df_freq['srs_predyn'] = sm.smallwood(df_freq, df_predyn_time)
    df_freq['srs_postdyn'] = sm.smallwood(df_freq, df_postdyn_time)

    plotting.bokeh_html(df_freq, df_predyn_time, df_postdyn_time, accel_name, predyn_date, postdyn_date)


if __name__ == '__main__':
    main()