# test_rotate.py
import pytest
from euchre.utility import rotate, rotate_to

def test_rotate_basic():
    lst = [1, 2, 3, 4]
    rotated = rotate(lst)
    assert rotated == [2, 3, 4, 1]

def test_rotate_single_element():
    lst = [42]
    rotated = rotate(lst)
    assert rotated == [42]  # unchanged

def test_rotate_empty_list():
    lst = []
    with pytest.raises(IndexError):
        rotate(lst)

def test_rotate_to_target_present():
    lst = [1, 2, 3, 4]
    rotated = rotate_to(lst, 3)
    assert rotated == [3, 4, 1, 2]

def test_rotate_to_target_first_already():
    lst = [5, 6, 7]
    rotated = rotate_to(lst, 5)
    assert rotated == [5, 6, 7]  # no change

def test_rotate_to_target_not_present():
    lst = [10, 20, 30]
    with pytest.raises(Exception, match="Can not rotate list, target not present."):
        rotate_to(lst, 99)
