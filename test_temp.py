from temp import add


def test_add() -> None:
    a, b = 1, 1

    result = add(a, b)

    assert result == 2
