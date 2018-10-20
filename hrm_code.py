import numpy as np
import pandas as pd
from scipy import signal
import json


def import_data(filepath):
    """
    Imports data file from specified file name AND path and returns time and voltage arrays

    Args:
        filepath: csv file to be imported
    Returns:
        time: array of time values
        voltage: array of voltage values
    """
    headers = ['time', 'voltage']
    data = pd.read_csv(filepath, names=headers)
    time = data['time']
    voltage = data['voltage']
    return time, voltage


def calc_duration(time):
    """
    Calculates the duration of the ECG signal

    Args:
        time: array of time values
    Returns:
        dur: duration of ECG signal
    """
    dur = time.max()-time.min()
    return dur


def find_max_min_volt(voltage):
    """
    Determines the minimum and maximum voltages of the ECG signal

    Args:
        voltage: array of voltage values
    Returns:
        both: vector containing both the minimum and maximum voltages
    """
    max_volt = voltage.max()
    min_volt = voltage.min()
    both = [min_volt, max_volt]
    return both


def calc_sample_freq(time):
    """
    Calculates the sampling frequency of the ECG signal

    Args:
        time: array of time values
    Returns:
        fs: sampling frequency of ECG
    """
    fs = 1/(time[1]-time[0])
    return fs


def filter_signal(voltage):
    """
    Filters the voltage signal with a Savitzky-Golay filter
    Window length of 17 (must be odd) and order of 3 (must be less than window length)

    Args:
        voltage: array of voltage values
    Returns:
        filtered_volt: array of filtered voltage values
    """
    filtered_volt = signal.savgol_filter(np.ravel(voltage), 17, 8)
    return filtered_volt


def correlate_signal(filtered_volt, fs):
    """
    Performs correlation of filtered data with a kernel of the normalized data from 0 to the sampling frequency

    Args:
        filtered_volt: array of filtered voltage values
        fs: sampling frequency of the ECG
    Returns:
        corr: array of correlated voltage values
    """
    normalize = (filtered_volt-np.min(filtered_volt))/(np.max(filtered_volt)-filtered_volt)
    corr_with = normalize[0: int(fs)]
    corr = np.correlate(np.squeeze(filtered_volt), np.squeeze(corr_with), 'full')
    return corr


def where_peaks(time, corr, fs):
    """
    Finds the location of the peaks from the correlated voltage signal

    Args:
        time: array of time values
        corr: correlated voltage values
        fs:
    Returns:
        beat_times: array of times when a beat occurred
    """
    peaks = signal.find_peaks_cwt(corr, np.arange(1, int(fs)))
    beats = peaks
    beat_times = time[beats]
    return beat_times


def num_beat(beat_times):
    """
    Determines the number of beats that occurred during the ECG signal

    Args:
        beat_times: array of times when a beat occurred
    Returns:
        num_beats: value stating number of total beats
    """
    num_beats = len(beat_times)
    return num_beats


def calc_bpm(num_beats, dur):
    """
    Determines the beats per minute of an ECG signal

    Args:
        num_beats: number of total beats
        dur: duration of ECG signal
    Returns:
        bpm: average beats per minute
    """
    bpm = num_beats/(dur/60)
    print(bpm)
    return bpm


#def create_dict(bpm, both, dur, num_beats, beat_times):
    """
    Creates dictionary of necessary output values

    Args:
        bpm: average beats per minute
        both: tuple containing voltage extremes
        dur: duration of ECG signal
        num_beats: number of beats in ECG signal
        beat_times: array of times when beat occurred
    Returns:
        metrics: dictionary values of metrics
    """
    #metrics = {
        #"mean_hr_bpm": bpm,
        #"voltage extremes": both,
        #"duration": dur,
        #"num_beats": num_beats,
        #"beats": beat_times}
    #return metrics


def main():
    filepath = "test_data/test_data1.csv"
    [time, voltage] = import_data(filepath)
    dur = calc_duration(time)
    fs = calc_sample_freq(time)
    filtered_volt = filter_signal(voltage)
    both = find_max_min_volt(voltage)
    corr = correlate_signal(voltage, fs)
    beat_times = where_peaks(time, corr, fs)
    num_beats = num_beat(beat_times)
    bpm = calc_bpm(num_beats, dur)
    #metrics = create_dict(bpm, both, dur, num_beats, beat_times)


if __name__ == "__main__":
    main()


