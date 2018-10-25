import numpy as np
from scipy import signal
import pandas as pd
import logging
import math
import json
import csv


logging.basicConfig(filename='logging.txt', format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y &I:%M:%S %p', level=logging.DEBUG)


def number_please(input):
    """
    Function checks to see if the number is real and it is a float.

    Args:
        input: number(s) to check
    Returns:
        boolean: states whether the value(s) are real or not
    """
    try:
        float(input)
        if np.isreal(float(input)):
            return True
        else:
            raise ValueError
    except ValueError:
        logging.warning("Data contains non-real or non-numerical value(s)")
        return False


def import_data(filepath):
    """
    Imports data file from specified file name AND path and returns
    time and voltage arrays

    Args:
        filepath: csv file to be imported
    Returns:
        time: array of time values
        voltage: array of voltage values
    """
    if filepath.endswith('.csv'):
        pass
    else:
        raise IOError("The file imported is not a csv file. "
                      "Please import a csv file.")

    try:
        file = open(filepath, 'r')
    except FileNotFoundError:
        raise FileNotFoundError('File not found, input an new path')

    time = []
    voltage = []
    temp_data = csv.reader(file, delimiter=',')

    for row in temp_data:
        if (number_please(row[0])) and (number_please(row[1])):
            temp_time = float(row[0])
            temp_volt = float(row[1])

            time.append(temp_time)
            voltage.append(temp_volt)

    if time == [] or voltage == []:
        logging.error('Time or voltage data is empty')

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
    if dur < 10:
        logging.info("Warning: Duration of signal is less than 10 seconds. ")

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
    if abs(max_volt) > 300 or abs(min_volt) > 300:
        logging.warning("Warning: Voltage is out of ECG range")
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
    Window length of 17 (must be odd) and order of 3
    (must be less than window length)

    Args:
        voltage: array of voltage values
    Returns:
        filtered_volt: array of filtered voltage values
    """
    filtered_volt = signal.savgol_filter(np.ravel(voltage), 17, 8)
    return filtered_volt


def detect_peak(filtered_volt, fs, hrw):
    """
    Function finds index of peaks using a moving average
    Adapted from: Analyzing a Discrete Heart Rate Signal Using Python-Part 1
    http://www.paulvangent.com/2016/03/15/
    analyzing-a-discrete-heart-rate-signal-using-python-part-1/

    Args:
        filtered_volt: array of filtered voltage values
        fs: sampling frequency of ECG
        hrw: user-input multiplication factor for the moving average
             input to determine the window
    Returns:
        peaklist: index of where peaks occur
    """
    filtered_volt = pd.Series(data=filtered_volt)
    mov_avg = filtered_volt.rolling(int(hrw * fs)).mean()
    avg_hr = (np.mean(filtered_volt))
    mov_avg = [avg_hr if math.isnan(x) else x for x in mov_avg]
    mov_avg = [(x + abs(avg_hr - abs(np.amin(filtered_volt) / 2))) * 1.2
               for x in mov_avg]
    window = []
    peaklist = []
    pos = 0
    for datapoint in filtered_volt:
        rollingmean = mov_avg[pos]
        if (datapoint < rollingmean) and (len(window) < 1):
            pos += 1
        elif datapoint > rollingmean:
            window.append(datapoint)
            pos += 1
            if pos >= len(filtered_volt):
                beatposition = pos - len(window) + (window.index(max(window)))
                peaklist.append(beatposition)
                window = []
        else:
            beatposition = pos - len(window) + (window.index(max(window)))
            peaklist.append(beatposition)
            window = []
            pos += 1
    return peaklist


def num_beat(time, peaklist):
    """
    Determines the number of beats that occurred during the ECG signal

    Args:
        peaklist: array of times when a beat occurred
        time: time array of ECG signals
    Returns:
        num_beats: value stating number of total beats
        beats: array of times when beats occurred
    """
    num_beats = len(peaklist)
    beats = []
    for i in peaklist:
        beats.append(time[i])
    beats = np.array(beats).tolist()
    return num_beats, beats


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

    if bpm > 180:
        logging.warning("Average heart rate detected to be more than 180 bpm.")
    if bpm < 40:
        logging.warning("Average heart rate detected to be less than 40 bpm.")
    return bpm


def create_metrics(bpm, beats, both, dur, num_beats):
    """
    Creates metrics dictionary

    Args:
        bpm: average beats per minute
        beats: array of times when beats occur
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
        "beats": beats
    }
    return metrics


def create_jason(filepath, metrics):
    """
    Creates a jason file with metrics dictionary

    Args:
        filepath: csv file path
        metrics: dictionary of appropriate metrics from signal
    """
    try:
        json_name = filepath.replace('.csv', '.json')
        with open(json_name, "w") as outfile:
            json.dump(metrics, outfile)
        logging.info('INFO: Successful creation .json file')

    except TypeError:
        print('Invalid json input')
        logging.debug('Error: json Output')


def main():
    filepath = "test_data/test_data9.csv"
    [time, voltage] = import_data(filepath)
    dur = calc_duration(time)
    fs = calc_sample_freq(time)
    filtered_volt = filter_signal(voltage)
    both = find_max_min_volt(voltage)
    peaklist = detect_peak(filtered_volt, fs, 0.5)
    [num_beats, beats] = num_beat(time, peaklist)
    bpm = calc_bpm(num_beats, dur)
    metrics = create_metrics(bpm, beats, both, dur, num_beats)
    create_jason(filepath, metrics)
    logging.info('INFO: Program has ended.')


if __name__ == "__main__":
    main()
