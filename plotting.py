# Module for making plots

import matplotlib.pyplot as plt


def test_plot(data):
    plt.plot(data.srs_fn,data.srs_fn)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Frequency (Hz)')
    plt.title('Test Plot')
    # plt.show()