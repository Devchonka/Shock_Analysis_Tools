# Module for making plots

import matplotlib.pyplot as plt
from matplotlib.colors import cnames
import bokeh.plotting as bk
import control

# http://bokeh.pydata.org/docs/user_guide/charts.html

def bokeh_html(data):
    # plt.plot(data.srs_fn, data.srs_gs)
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('SRS (gs)')
    # plt.title('Test Plot')
    # plt.show()

    bk.output_file("test.html", title="SRS test plots")

    # Figure 1: Raw time series data
    p1 = bk.figure(
        plot_width=500, plot_height=500,outline_line_color="red",
        tools="pan,box_zoom,reset,previewsave,resize",
        title="Raw Time Series Data", x_axis_label='Time(sec)', y_axis_label='Amplitude(counts)')

    for channel_idx in range(24):
        p1.line(data._time_data[0], data._time_data[channel_idx+1],
                color=cnames.keys()[channel_idx])
        bk.hold()

    p2 = bk.figure(
        plot_width=500, plot_height=500, outline_line_color="red",
        tools="pan,box_zoom,reset,previewsave,resize",
        title="Frequency Functions")

    # Figure 2: Transfer Functions, constant per frequency
    for freq_idx in range(120):
        control.bode(data.tf[freq_idx], dB=1,
                color=cnames.keys()[channel_idx])

        # control.nyquist(data.tf[freq_idx], (0.0001, 1000)); - another figure..

        bk.hold()

    # Figure 3: SRS Frequency Response
    p3 = bk.figure(
        plot_width=1000, plot_height=1000,  # width and height of the entire plot in pixels, including border space
        outline_line_color="red",
        tools="pan,box_zoom,reset,previewsave,resize",
        y_axis_type="log", x_axis_type="log",
        x_mapper_type="log", y_mapper_type="log",
        title="Testing 1 2 3", x_axis_label='Frequency (Hz)', y_axis_label='SRS (gs)')

    for channel_idx in range(24):
        p3.line(data.srs_fn, data.srs_gs[channel_idx], legend = data._labels[channel_idx],
                color=cnames.keys()[channel_idx])
        bk.hold()

    # Show all figures
    bk.show(bk.VBox(bk.HBox(p1, p2), p3))
    # bk.show(p1)