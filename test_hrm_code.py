import pytest
import json
import numpy as np


@pytest.mark.parametrize("candidate, expected", [
    (1.345, True),
    (-4.554, True),
    ('9999', True)
])
def test_number_please(candidate, expected):
    from hrm_code import number_please
    assert number_please(candidate) == expected


def test_import_data():
    from hrm_code import import_data
    [time, voltage] = import_data("test_data/test_data2.csv")
    assert time[0] == 0
    assert voltage[0] == -0.345


def test_calc_duration():
    from hrm_code import calc_duration
    fake_time = [0, 1, 2, 3, 4.3, 5, 6, 7.2]
    dur = calc_duration(fake_time)
    assert dur == 7.2


def test_find_min_max_volt():
    from hrm_code import find_max_min_volt
    fake_voltage = [1.2, -0.3, 4.8, 0, -3]
    both = find_max_min_volt(fake_voltage)
    assert both == [-3, 4.8]


def test_calc_freq():
    from hrm_code import calc_sample_freq
    fake_time = [0, 0.5, 1, 1.5, 2]
    fs = calc_sample_freq(fake_time)
    assert fs == 2


def test_detect_peak():
    from hrm_code import detect_peak
    # Peaks should occur every 60 sec
    fs = 60
    t = np.arange(0, 5, 1/fs)
    wave = abs(np.sin(t*np.pi)**20)
    peaks = detect_peak(wave, fs, hrw=0.1)
    assert peaks == [27, 87, 147, 207, 267]


def test_num_beat():
    from hrm_code import num_beat
    fake_peaklist = [1, 3, 4]
    fake_time = [0, 0.5, 1, 1.5, 2, 2.5, 3]
    [num_beats, beats] = num_beat(fake_time, fake_peaklist)
    assert num_beats == 3
    assert beats == [0.5, 1.5, 2]


def test_calc_bpm():
    from hrm_code import calc_bpm
    fake_num_beats = 20
    fake_dur = 40
    bpm = calc_bpm(fake_num_beats, fake_dur)
    assert bpm == 30


def test_create_metrics():
    from hrm_code import create_metrics
    bpm = 70
    both = [-1.4, 5.6]
    dur = 30
    num_beats = 80
    beats = [0.5, 0.75, 0.8]
    metrics = create_metrics(bpm, beats, both, dur, num_beats)
    assert metrics == {
        "mean_hr_bpm": 70,
        "voltage extremes": [-1.4, 5.6],
        "duration": 30,
        "num_beats": 80,
        "beats": [0.5, 0.75, 0.8]
    }


def test_create_jason():
    from hrm_code import create_jason
    metrics = {"Favorite Ice Cream Flavor": "Chocolate",
               "Favorite Book": "A Tree Grows in Brooklyn",
               "Favorite Number": 8}
    filename = "test_output.csv"
    create_jason(filename, metrics)

    read_file = json.load(open('test_output.json'))
    assert read_file == {"Favorite Ice Cream Flavor": "Chocolate",
                         "Favorite Book": "A Tree Grows in Brooklyn",
                         "Favorite Number": 8}
