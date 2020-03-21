# -*- coding: utf-8 -*-

import pytest
from stt_sample_inspector.skeleton import fib

__author__ = "Reuben Morais"
__copyright__ = "Reuben Morais"
__license__ = "mozilla"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
