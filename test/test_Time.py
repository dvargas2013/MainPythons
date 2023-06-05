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

    assert TimeClass(minute=8) == TimeClass.fromString("0:08")


def test_TimeClass_comparisons():
    assert TimeClass(16, 8, 8) == TimeClass(8, 8, 8) + TimeClass(8)

    oneam = TimeClass(1)
    oneamNextDay = TimeClass(20) + TimeClass(5)

    assert oneamNextDay == oneam
    assert oneamNextDay > oneam
    assert (oneam > oneam) is False


def test_TimeClass_math():
    m40 = TimeClass(minute=40)
    pm810 = TimeClass.fromString("8:10pm")

    counter = pm810
    for i in range(35):
        assert pm810 - i * m40 == pm810 - m40 * i == counter
        counter -= m40


def test_dayofweek():
    assert Time.DayOfTheWeek(6, 7, 1700) == "Monday"
    assert Time.DayOfTheWeek(4, 30, 1803) == "Saturday"
    assert Time.DayOfTheWeek(1, 1, 1863) == "Thursday"
    assert Time.DayOfTheWeek(8, 25, 1946) == "Sunday"
    assert Time.DayOfTheWeek(11, 26, 2015) == "Thursday"


def test_days_between():
    assert Time.days_between((9, 2, 1945), (8, 4, 2016)) == 25904
    assert Time.days_between((7, 20, 1969), (8, 4, 2016)) == 17182
