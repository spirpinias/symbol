import pytest
import polars as pl

from hypothesis import given
from hypothesis import strategies as st

INT64_MIN = -(2**63)
INT64_MAX = 2**63 - 1

int64 = st.integers(min_value=INT64_MIN, max_value=INT64_MAX)


def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0


@given(st.lists(int64, min_size=1))
def test_min_never_greater_than_max(values):
    s = pl.Series(values)
    assert s.min() <= s.max()
