# Module for making plots

# TO DO : Add grid lines, make margin lines dashed, center SRS plot

from matplotlib.colors import cnames
import bokeh.plotting as bk
import bokeh.objects as bo
import pandas as pd
import numpy as np

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


    colors = [
        "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
        "#ddb7b1", "#cc7878", "#933b41", "#550b1d"
    ]

    color =[[] for i in range(24)]
    for ch_idx in range(24):
        for fn_idx in range(120):
            color[ch_idx].append(colors[min(int(data.srs_gs[ch_idx][fn_idx]) - 2, 8)])

    for x in range(len(data.srs_fn)):
        df = pd.DataFrame(np.asarray(data.srs_gs).T.tolist(), index=data.srs_fn, columns=range(1, 25))
    df['srs_fn'] = data.srs_fn

    for x in range(len(data.srs_fn)):
        df2 = pd.DataFrame(np.asarray(color).T.tolist(), index=data.srs_fn, columns=range(1, 25))

#    df['color'] = df2

    import pdb
    pdb.set_trace()

    source = bk.ColumnDataSource(
        data=dict(
            freqs=df.iloc[1:24],  # x
            channel=range(1, 25),  # y
            color=df2,
            rate=df['srs_fn'])
        )

    TOOLS = "resize,hover,save"

    channels = range(1,25)

    p4 = bk.figure(title="Frequency data per Channel",
                   #y_range=list(reversed(channels)),
                   outline_line_color="red",
                   x_axis_type="log",
                   x_axis_location="above", plot_width=1100, plot_height=600,
                   toolbar_location="left", tools=TOOLS)



    p4.rect("srs_gs", "srs_fn", 100, 1, source=source,
     #x_range=weeks, y_range=list(reversed(days)),
     x_axis_location="above",
     color="color", line_color=None,
     tools="resize,hover,previewsave", title="Freq vs Accel",
     plot_width=900, plot_height=400, toolbar_location="left")



    p4.grid.grid_line_color = None
    p4.axis.axis_line_color = None
    p4.axis.major_tick_line_color = None
    p4.axis.major_label_text_font_size = "5pt"
    p4.axis.major_label_standoff = 0
    p4.xaxis.major_label_orientation = np.pi / 3

    hover = p4.select(dict(type=HoverTool))
    hover.snap_to_data = False
    hover.tooltips = OrderedDict([
        ('channel', '@ch @freqs'),
        ('rate', '@srs_rate'),
    ])


    bk.show(bk.VBox(bk.HBox(p1, p2), p3, p4))