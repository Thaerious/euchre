from euchre.bots.tools.Query import normalize_value
import pytest

@pytest.mark.parametrize(
    "for_player, target, expected",
    [
        (0, 0, 0),  
        (0, 1, 1),
        (0, 2, 2),
        (0, 3, 3),
        (1, 1, 0),
        (2, 2, 0),
        (3, 3, 0),
        (1, 2, 1),
        (1, 3, 2),
        (3, 0, 1),
        (2, 0, 2),
    ]
)
def test_normalize_value(for_player, target, expected):
    assert expected == normalize_value(for_player, target)
