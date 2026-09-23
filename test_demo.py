import pytest


def somme(a, b):
    return a + b

def test_somme():
    assert somme(5, 6) == 11
    assert somme(-5, 5) == 0
    assert somme(0, 8) == 8
 
def my_min(a, b):
    return a - b

def test_my_min():
    assert my_min(8, 5) == 3
    assert my_min(8, 8) == 0
    assert my_min(10, 8) == 2


def my_div(a, b):
    return a / b 

def test_my_div():
    assert my_div(8, 2) == 4
    assert my_div(9, 3) == 3

def test_my_div_zero_error():
    with pytest.raises(ZeroDivisionError, match=""):
        my_div(8, 0)