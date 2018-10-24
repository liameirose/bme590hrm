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