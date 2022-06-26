import pytest

from done import Game


class Input:
    data = []
    removing = False


def sendInput(in_put):
    if Input.removing:
        Input.data = []
        Input.removing = False

    ti = type(in_put)
    if ti is str:
        Input.data.append(in_put)
    elif ti is list:
        Input.data.extend(in_put)
    else:
        raise RuntimeError("test made bad input")


# noinspection PyUnusedLocal
def mock_input(*args, **kwargs):
    if not Input.removing:
        Input.data = list(reversed(Input.data))

    if Input.data:
        return Input.data.pop()
    else:
        raise KeyboardInterrupt()


@pytest.fixture(autouse=True)
def mock_response(monkeypatch):
    monkeypatch.setattr(Game, "Input", mock_input)


def metaTest(capsys, func, line1ind, line2ind, total):
    sendInput(["giveup", "giveup+1"])
    func()
    output = capsys.readouterr().out
    lines = list(output.strip().split('\n'))
    assert len(lines) == total
    line1 = lines[line1ind]
    line2 = lines[line2ind]
    assert line1.endswith("is Correct")
    assert line2.endswith("is Wrong")


def test_multiplication(capsys):
    for _ in range(100): metaTest(capsys, Game.multiplication, 0, 1, 2)


def test_pattern(capsys):
    for _ in range(100): metaTest(capsys, Game.pattern, 3, 7, 11)


def test_thinker(capsys):
    for _ in range(100): metaTest(capsys, Game.thinker, 1, 3, 4)


def test_physics(capsys):
    for _ in range(100): metaTest(capsys, Game.physics, 3, 9, 14)
