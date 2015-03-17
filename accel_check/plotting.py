"""
This is the module to help make plots of the comparison of time and frequency domain data
using pandas dataframes and the bokeh library to create an interactive html website.
"""

import bokeh.plotting as bk
from bokeh.models import Range1d


def bokeh_html(df_freq, df_predyn_time, df_postdyn_time, accel_name, predyn_date, postdyn_date):
    bk.output_file("A477Z.html", title="Comparison of SRS for A477Z Shock")
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

    # Figure 1: Raw time series data : Predynamic
    p1 = bk.figure(
        plot_width=600, plot_height=600, outline_line_color="red",
        tools=TOOLS,
        title=accel_name + ' Predyn Time data', x_axis_label='Time(sec)', y_axis_label='Amplitude(g\'s)')

    p1.line(x=df_predyn_time['predyn_t'], y=df_predyn_time['predyn_t_data'], width=10, height=20,
            x_axis_location="above", legend=predyn_date)

    # Figure 2: Raw time series data : Postdynamic
    p2 = bk.figure(
        plot_width=600, plot_height=600, outline_line_color="red",
        tools=TOOLS,
        title=accel_name + ' Postdyn Time data', x_axis_label='Time(sec)', y_axis_label='Amplitude(g\'s)')

    p2.line(x=df_postdyn_time['postdyn_t'], y=df_postdyn_time['postdyn_t_data'], width=10, height=20,
            x_axis_location="above", legend=postdyn_date)

    # Figure 3: Freq domain data : Predynamic : DAQScribe + independent conversion

    p3 = bk.figure(
        plot_width=600, plot_height=600, outline_line_color="red",
        tools=TOOLS, y_axis_type="log", x_axis_type="log",
        title=accel_name + ' Predyn SRS data', x_axis_label='Frequency (Hz)',
        y_axis_label='                      Acceleration (gs)')
    # tool provided data
    p3.line(x=df_freq['predyn_f'], y=df_freq['predyn_f_data'], plot_width=800, plot_height=800,
            x_axis_location="above", legend='DAQScribe SRS Conversion', line_width=1.5)

    # our own calculated data
    p3.line(x=df_freq['predyn_f'], y=df_freq['srs_predyn'], plot_width=800, plot_height=800,
            legend='Mech Sys SRS Conversion', color="red", line_dash=[4, 4],
            line_alpha=0.8, min_border=2, line_width=2.5)

    p3.x_range = Range1d(start=10 ** 2, end=10 ** 5)
    p3.legend.orientation = "bottom_right"

    # Figure 4: Freq domain data : Postdynamic : DAQScribe + independent conversion
    p4 = bk.figure(
        plot_width=600, plot_height=600, outline_line_color="red",
        tools=TOOLS, y_axis_type="log", x_axis_type="log",
        title=accel_name + ' Postdyn SRS data', x_axis_label='Frequency (Hz)',
        y_axis_label='                      Acceleration (gs)')
    # tool provided data
    p4.line(x=df_freq['predyn_f'], y=df_freq['postdyn_f_data'], plot_width=800, plot_height=800,
            x_axis_location="above", legend='DAQScribe SRS Conversion', line_width=1.5)
    # our own calculated data
    p4.line(x=df_freq['predyn_f'], y=df_freq['srs_postdyn'], plot_width=800, plot_height=800,
            legend='Mech Sys SRS Conversion', color="red", line_dash=[4, 4],
            line_alpha=0.8, min_border=2, line_width=2.5)

    p4.x_range = Range1d(start=10 ** 2, end=10 ** 5)
    p4.legend.orientation = "bottom_right"

    bk.show(bk.VBox(bk.HBox(p1, p2), bk.HBox(p3, p4)))