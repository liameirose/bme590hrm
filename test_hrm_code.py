import pytest


def test_import_data():
    from hrm_code import import_data
    [time, voltage] = import_data("test_data/test_data2.csv")
    assert time[0] == 0
    assert voltage[0] == -0.345
