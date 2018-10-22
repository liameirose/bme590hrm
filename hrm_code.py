import numpy as np
from scipy import signal
import logging
import json


logging.basicConfig(filename='logging.txt', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y &I:%M:%S %p', level=logging.DEBUG)


def import_data(filepath):
    """
    Imports data file from specified file name AND path and returns time and voltage arrays

    Args:
        filepath: csv file to be imported
    Returns:
        time: array of time values
        voltage: array of voltage values
    """
    if filepath.endswith('.csv'):
        pass
    else:
        raise IOError("The file imported is not a csv file. Please import a csv file.")

    data = np.loadtxt(filepath, delimiter=",")
    time = data[:, 0]
    voltage = data[:, 1]
    return time, voltage


def calc_duration(time):
    """
    Calculates the duration of the ECG signal

    Args:
        time: array of time values
    Returns:
        dur: duration of ECG signal
    """
    dur = np.amax(time)-np.amin(time)
    return dur


def find_max_min_volt(voltage):
    """
    Determines the minimum and maximum voltages of the ECG signal

    Args:
        voltage: array of voltage values
    Returns:
        both: vector containing both the minimum and maximum voltages
    """
    max_volt = np.amax(voltage)
    min_volt = np.amin(voltage)
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


def correlate_signal(time, filtered_volt, fs):
    """
    Performs correlation of filtered data with a kernel of the normalized data from 0 to the sampling frequency

    Args:
        filtered_volt: array of filtered voltage values
        fs: sampling frequency of the ECG
    Returns:
        corr: array of correlated voltage values
    """
    normalize = filtered_volt - np.mean(filtered_volt)
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
    beat_times = list(beat_times)
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


def create_metrics(bpm, beat_times, both, dur, num_beats):
    """
    Creates metrics dictionary

    Args:
        bpm: average beats per minute
        beat_times: array of times when beats occur
        both: vector containing minimum and maximum voltage
        dur: duration of the ECG signal
        num_beats: number of beats that occurred during the signal
    Returns:
        metrics: dictionary of appropriate metrics from signal
    """
    metrics = {
        "mean_hr_bpm": bpm,
        "voltage extremes": both,
        "duration": dur,
        "num_beats": num_beats,
        "beats": beat_times
    }
    return metrics


#def create_jason(filepath, metrics):
    """
    Creates a jason file with metrics dictionary

    Args:
        filepath: csv file path
        metrics: dictionary of appropriate metrics from signal
    """
    #json_name = filepath.replace('.csv', '.json')
    #jsonfile = open(json_name, 'w')
    #json.dump(metrics, jsonfile)

    #logging.info('INFO: Successful creation .json file')


def main():
    filepath = "test_data/test_data1.csv"
    [time, voltage] = import_data(filepath)
    dur = calc_duration(time)
    fs = calc_sample_freq(time)
    filtered_volt = filter_signal(voltage)
    both = find_max_min_volt(voltage)
    corr = correlate_signal(time, filtered_volt, fs)
    beat_times = where_peaks(time, corr, fs)
    num_beats = num_beat(beat_times)
    bpm = calc_bpm(num_beats, dur)
    metrics = create_metrics(bpm, beat_times, both, dur, num_beats)
    #create_jason(filepath, metrics)


if __name__ == "__main__":
    main()


