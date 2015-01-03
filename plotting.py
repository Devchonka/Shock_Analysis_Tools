# Module for making plots

# TO DO : Add grid lines, make margin lines dashed, center SRS plot

from matplotlib.colors import cnames
import bokeh.plotting as bk
import bokeh.objects as bo

# for p4
from collections import OrderedDict
import numpy as np
from bokeh.models import HoverTool


def bokeh_html(data):
    bk.output_file("test.html", title="SRS test plots")
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

    # Figure 1: Raw time series data
    p1 = bk.figure(
        plot_width=500, plot_height=500, outline_line_color="red",
        tools=TOOLS,
        title="Raw Time Series Data", x_axis_label='Time(sec)', y_axis_label='Amplitude(Volts)')

    for channel_idx in range(24):
        p1.line(data._time_data[0], data.raw_volts[channel_idx],
                color=cnames.keys()[channel_idx])
        bk.hold()

    # Figure 2: EMPTY
    p2 = bk.figure(
        plot_width=500, plot_height=500, outline_line_color="red",
        tools=TOOLS,
        title="Another Figure")
    x_range1 = bo.Range1d(start=10e2, end=10e5)
    # Figure 3: SRS Frequency Response
    p3 = bk.figure(
        plot_width=1000, plot_height=1000,  # width and height of the entire plot in pixels, including border space
        outline_line_color="red",
        tools=TOOLS,
        y_axis_type="log", x_axis_type="log",
        x_range=x_range1,
        title="Shock Response Spectrum (SRS)", x_axis_label='Frequency (Hz)', y_axis_label='Acceleration (gs)')

    for channel_idx in range(24):
        p3.line(data.srs_fn, data.srs_gs[channel_idx], legend=data._labels[channel_idx],
                line_alpha=0.8, line_width=1.5, min_border=2,
                color=cnames.keys()[channel_idx])
        bk.hold()

    p3.grid.grid_line_color = "grey"

    p3.line(data.srs_fn, data.spec_interp_plus9dB, color='black', line_dash=[4, 4])
    p3.line(data.srs_fn, data.spec_interp_plus6dB, color='black', line_dash=[4, 4])
    p3.line(data.srs_fn, data.spec_interp_minus3dB, color='black', line_dash=[4, 4])
    p3.line(data.srs_fn, data.spec_interp_minus6dB, color='black', line_dash=[4, 4])


    # p3.xaxis[0].bounds = [0,10**3]
    # p3.x_range = bo.Range1d(start=10e2, end=10e5)
    # p3.xaxis.bounds = [10e2, 10e5]


# Figure 4: SRS Freq content per accel

    # Read in the data with pandas. Convert the year column to string

    freqs = [round(i) for i in data.srs_fn]
    channels = [str(i) for i in range(1,25)]

    colors = [
        "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
        "#ddb7b1", "#cc7878", "#933b41", "#550b1d"
    ]

    color = []
    rate = []
    for fn_idx in range(len(freqs)):
        for ch_idx in range(24):
            srs_rate = data.srs_gs[ch_idx][fn_idx]
            rate.append(srs_rate)
            color.append(colors[min(int(srs_rate)-2, 8)])

    source = bk.ColumnDataSource(
        data=dict(x = freqs, ch = channels, color=color, rate=rate)
    )

    TOOLS = "resize,hover,save"

    p4 = bk.figure(title="Frequency data per Channel",
        #x_range=freqs, y_range=list(reversed(channels)),
        x_axis_location="above", plot_width=1100, plot_height=600,
        toolbar_location="left", tools=TOOLS)

    p4.rect(freqs, channels, 1, 1, source=source,
        color="color", line_color=None)

    p4.grid.grid_line_color = None
    p4.axis.axis_line_color = None
    p4.axis.major_tick_line_color = None
    p4.axis.major_label_text_font_size = "5pt"
    p4.axis.major_label_standoff = 0
    p4.xaxis.major_label_orientation = np.pi/3

    hover = p4.select(dict(type=HoverTool))
    hover.snap_to_data = False
    hover.tooltips = OrderedDict([
        ('channel', '@ch @freqs'),
        ('rate', '@srs_rate'),
    ])

    bk.show(bk.VBox(bk.HBox(p1, p2), p3, p4))