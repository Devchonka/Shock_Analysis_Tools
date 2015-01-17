# Module for making plots

from matplotlib.colors import cnames
import bokeh.plotting as bk
import bokeh.objects as bo
import math

from collections import OrderedDict
from bokeh.models import HoverTool


def bokeh_html(data):
    bk.output_file("test.html", title="SRS test plots")
    TOOLS = "pan,wheel_zoom,box_zoom,reset,save,box_select"

    # Figure 1: Raw time series data
    p1 = bk.figure(
        plot_width=700, plot_height=700, outline_line_color="red",
        tools=TOOLS,
        title="Raw Time Series Data", x_axis_label='Time(sec)', y_axis_label='Amplitude(Volts)')

    for channel_idx in range(24):
        p1.line(data._time_data[0], data.raw_volts[channel_idx],
                color=cnames.keys()[channel_idx])
        bk.hold()

    # Figure 2: SRS Frequency Response
    p2 = bk.figure(
        plot_width=1100, plot_height=800,  # width and height of the entire plot in pixels, including border space
        outline_line_color="red",
        tools=TOOLS,
        y_axis_type="log", x_axis_type="log",
        title="Shock Response Spectrum (SRS)", y_axis_label='Acceleration (gs)', x_axis_label='Frequency (Hz)')

    for channel_idx in range(24):
        p2.line(data.srs_fn, data.srs_gs[channel_idx], legend=data._labels[channel_idx + 1],
                line_alpha=0.8, line_width=1.5, min_border=2,
                color=cnames.keys()[channel_idx])
        bk.hold()

    p2.grid.grid_line_color = "grey"

    p2.line(data.srs_fn, data.spec_interp_plus9dB, color='black', line_dash=[4, 4])
    p2.line(data.srs_fn, data.spec_interp_plus6dB, color='black', line_dash=[4, 4])
    p2.line(data.srs_fn, data.spec_interp_minus3dB, color='black', line_dash=[4, 4])
    p2.line(data.srs_fn, data.spec_interp_minus6dB, color='black', line_dash=[4, 4])

    p2.x_range = bo.Range1d(start=10 ** 2, end=10 ** 5)

    # Figure 3: SRS Freq content per accel
    colors = [
        "#75968f", "#a5bab7", "#c9d9d3", "#e2e2e2", "#dfccce",
        "#ddb7b1", "#cc7878", "#933b41", "#550b1d"
    ]

    freq = []
    channel = []
    color = []
    rate = []
    largest_gs = 0
    smallest_gs = 10000

    for ch_idx in range(24):
        for fn_idx in range(120):
            freq.append(data.srs_fn[fn_idx])
            rate.append(data.srs_gs[ch_idx][fn_idx])
            channel.append(ch_idx + 1)
            if largest_gs < data.srs_gs[ch_idx][fn_idx]:
                largest_gs = data.srs_gs[ch_idx][fn_idx]
            if smallest_gs > data.srs_gs[ch_idx][fn_idx]:
                smallest_gs = data.srs_gs[ch_idx][fn_idx]

    largest_gs_lg = math.log(largest_gs)
    smallest_gs_lg = math.log(smallest_gs)
    diff = largest_gs_lg - smallest_gs_lg

    for i in range(len(rate)):
        color.append(colors[int((math.log(rate[i]) - smallest_gs_lg) * 8 / diff)])

    source = bk.ColumnDataSource(
        data=dict(
            freq=[str(round(x, 1)) for x in freq],  # y
            channel=channel,  # x
            color=color,
            rate=rate)
    )

    TOOLS = "resize,hover,save"

    p3 = bk.figure(title="Frequency data per Channel",
                   x_range=[str(x) for x in range(1, 25)],
                   y_range=[str(round(x, 1)) for x in list(reversed(data.srs_fn))],
                   outline_line_color="red",
                   x_axis_location="above", plot_width=1100, plot_height=900,
                   toolbar_location="left", tools=TOOLS)

    p3.rect("channel", "freq", 1, 1, source=source,
            x_axis_location="above",
            color="color",
            line_color=None,
            title="Freq vs Accel")

    p3.grid.grid_line_color = "black"
    p3.axis.axis_line_color = "black"
    p3.axis.major_tick_line_color = "black"
    p3.axis.major_label_text_font_size = "5pt"
    p3.axis.major_label_standoff = 0

    hover = p3.select(dict(type=HoverTool))
    hover.snap_to_data = False
    hover.tooltips = OrderedDict([
        ('channel', '@channel'),
        ('freq', '@freq'),
        ('rate', '@rate')
    ])

    bk.show(bk.VBox(p1, p2, p3))