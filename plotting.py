# Module for making plots

import matplotlib.pyplot as plt
import bokeh.plotting as bk


def test_plot(data):
    # plt.plot(data.srs_fn, data.srs_gs)
    # plt.xlabel('Frequency (Hz)')
    # plt.ylabel('SRS (gs)')
    # plt.title('Test Plot')
    # plt.show()

    bk.output_file("test.html", title="SRS test plots")
    p = bk.figure(
        tools="pan,box_zoom,reset,previewsave,resize",
        #y_axis_type="log", x_axis_type="log", y_range=[0, 10**3], x_range=[200, 10000],
        y_axis_type="log", x_axis_type="log", x_range=[200, 10000],
        title="Testing 1 2 3", x_axis_label='Frequency (Hz)', y_axis_label='SRS (gs)')

    for channel_idx in range(24):
        p.line(data.srs_fn, data.srs_gs[channel_idx], legend = data._labels[channel_idx])
        bk.hold()
    bk.show(p)