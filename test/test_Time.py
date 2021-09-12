from done import Time

TimeClass = Time.Time


def test_TimeClass_equivalence():
    for i in range(1, 11):
        t = TimeClass(i, i, i)
        assert t.hr == t.mn == t.sc == i


def test_TimeClass_specialConstructors():

    assert TimeClass(minute=8).mn == 8

    for i in range(1, 11):
        assert TimeClass(i, pm=True).hr == i + 12


def test_TimeClass_comparisons():
    assert TimeClass(16, 8, 8) == TimeClass(8, 8, 8) + TimeClass(8)

    oneam = TimeClass(1)
    oneamNextDay = TimeClass(20) + TimeClass(5)

    assert oneamNextDay == oneam
    assert oneamNextDay > oneam
    assert (oneam > oneam) is False

# TODO DayOfTheWeek, stopwatch, countdown
