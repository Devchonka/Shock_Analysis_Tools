# Module for making plots

# TO DO : Add grid lines, make margin lines dashed, center SRS plot

from matplotlib.colors import cnames
import bokeh.plotting as bk
import bokeh.objects as bo


def bokeh_html(data):
    bk.output_file("test.html", title="SRS test plots")

    # Figure 1: Raw time series data
    p1 = bk.figure(
        plot_width=500, plot_height=500, outline_line_color="red",
        tools="pan,box_zoom,reset,previewsave,resize",
        title="Raw Time Series Data", x_axis_label='Time(sec)', y_axis_label='Amplitude(Volts)')

    for channel_idx in range(24):
        p1.line(data._time_data[0], data.raw_volts[channel_idx],
                color=cnames.keys()[channel_idx])
        bk.hold()

    # Figure 2: EMPTY
    p2 = bk.figure(
            plot_width=500, plot_height=500, outline_line_color="red",
            tools="pan,box_zoom,reset,previewsave,resize",
            title="Another Figure")

    # Figure 3: SRS Frequency Response
    p3 = bk.figure(
        plot_width=1000, plot_height=1000,  # width and height of the entire plot in pixels, including border space
        outline_line_color="red",
        tools="pan,box_zoom,reset, previewsave, resize",
        y_axis_type="log", x_axis_type="log",
        # x_mapper_type="log", y_mapper_type="log",
        x_range=[10e2, 10e5],
        title="Shock Response Spectrum (SRS)", x_axis_label='Frequency (Hz)', y_axis_label='Acceleration (gs)')

    for channel_idx in range(24):
        p3.line(data.srs_fn, data.srs_gs[channel_idx], legend = data._labels[channel_idx],
                line_alpha=0.8, line_width=1.5, min_border=2,
                color=cnames.keys()[channel_idx])
        bk.hold()

    p3.grid.grid_line_color = "grey"

    p3.line(data.srs_fn, data.spec_interp_plus9dB, color = 'black')
    p3.line(data.srs_fn, data.spec_interp_plus6dB, color = 'black')
    p3.line(data.srs_fn, data.spec_interp_minus3dB, color = 'black')
    p3.line(data.srs_fn, data.spec_interp_minus6dB, color = 'black')

    p3.x_range = bo.Range1d(start=10e2, end=10e5)
    # p3.xaxis.bounds = [10e2, 10e5]

    bk.show(bk.VBox(bk.HBox(p1, p2), p3))