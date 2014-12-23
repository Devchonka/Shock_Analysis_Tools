# Module for making plots

import matplotlib.pyplot as plt


def test_plot(data):
    plt.plot(data.srs_fn,data.srs_gs)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('SRS (gs)')
    plt.title('Test Plot')
    plt.show()