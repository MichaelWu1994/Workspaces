import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import butter, lfilter, filtfilt


def butter_bandpass(low, high, f_sample, order=5):
    """Calculate butterworth bandpass filter parameters.

    Args:
    -------
    low : float
        low bound of the band.
    high : float
        high bound of the band.
    f_sample: float
        frequency of the signal (in Hz).
    order : int
        order of filter (default = 5).

    Returns
    -------
    b, a : ndarray, ndarray
        Numerator (`b`) and denominator (`a`) polynomials of the IIR filter.
        Only returned if ``output='ba'``.
    """
    nyq = 0.5 * f_sample
    low = low / nyq
    high = high / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, low, high, f_sample, order=5):
    """Apply butterworth bandpass filter onto the data

    Parameters
    -------
    data : array_like
        an array of input data
    low : float
        low bound of bandpass frequency
    high : float
        high bound of bandpass frequency
    f_signal : float
        sampling frequency
    order: int
        order of the filter (default = 5)

    Returns
    -------
    y0 : array_like
        an array of linearly filtered data
    y1: array_like
        an array of forward-backward filtered data
    """
    b, a = butter_bandpass(low, high, f_sample, order=order)
    y0 = lfilter(b, a, data)
    y1 = filtfilt(b,a, data)
    return y0, y1


with open('record.csv') as csvfile:
    csvfile.readline()
    readCSV = csv.reader(csvfile, delimiter=',')

    t = []
    pck_id = []
    ch_data = [[] for i in range(0, 8)]

    for row in readCSV:
        t.append(row[0])
        pck_id.append(row[1])
        i = 2
        for ch in ch_data:
            ch.append(float(row[i])/1000)
            i += 1

    plt.figure(1)

    i = 0
    for ch in ch_data:
        #plt.plot(t, ch, 'C' + str(i), label="Ch" + str(i + 1))
        i += 1

    plt.plot(t,ch_data[0],'C0', label='Ch 1')
    plt.legend()
    #plt.show()

    lowcut = 0.5
    highcut = 50
    f_sample = 250
    data = np.array(ch_data[0], dtype='Float64')
    y0, y1 = butter_bandpass_filter(data, lowcut, highcut, f_sample, order=5)
    
    plt.figure(2)
    plt.plot(t, y1, label="filtfilt")
    plt.xlabel("time (s)")
    plt.ylabel("voltage (mV)")
    plt.grid()
    plt.show()
