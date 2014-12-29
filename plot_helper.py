# Module of helper functions for plotting


def counts_to_volts (x, pga_gain, xducer_scale=0.0005):  # xducer_scale is 0.5 mV/g, temporary per Joe, Mark,Dave 3-27-14
    VREF = 5
    CODES = 32768  # 2^16 /2
    FIXGAIN = 1.75  # Salen-Key filter gain
    return VREF * (x / CODES / FIXGAIN / pga_gain / xducer_scale)