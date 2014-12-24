# Module for making plots

import matplotlib.pyplot as plt
from bokeh.plotting import figure, output_file, show


def test_plot(data):
    plt.plot(data.srs_fn, data.srs_gs)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SRS (gs)')
    plt.title('Test Plot')
    # plt.show()
    
    output_file("test.html", title="SRS test plots")
    p = figure(title="Example Title")
    p.line(data.srs_fn, data.srs_gs, legend="g's", x_axis_label='Frequency(Hz)', y_axis_label='Acceleration (g)')
    # show(p)