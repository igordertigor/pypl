from pypl import scales


def test_min_to_min():
    s = scales.linear_scale((1, 2), (2, 2.5))
    assert s(1) == 2


def test_max_to_max():
    s = scales.linear_scale((1, 2), (2, 2.5))
    assert s(2) == 2.5


def test_reverse():
    s = scales.linear_scale((1, 2), (2.5, 2))
    assert s(2) == 2
    assert s(1) == 2.5
