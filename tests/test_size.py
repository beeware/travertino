from typing import NamedTuple
from unittest.mock import Mock

import pytest

from travertino.size import BaseIntrinsicSize, at_least


class Size(NamedTuple):
    width: int
    height: int
    ratio: float

    def change(self, dimension, value):
        return self._replace(**{dimension: value})


BASE_SIZE = Size(width=1, height=2, ratio=0.1)


class TestBox:
    pass


@pytest.fixture
def box():
    box = TestBox()

    box.maxDiff = None

    box.layout = Mock()
    box.size = BaseIntrinsicSize(layout=box.layout)
    box.size._width, box.size._height, box.size._ratio = BASE_SIZE

    assert_size(box.size, BASE_SIZE)

    return box


def assert_size(size, values):
    assert (size.width, size.height, size.ratio) == values


def test_at_least_repr():
    assert repr(at_least(10)) == "at least 10"


def test_size_repr(box):
    assert repr(box.size) == "(1, 2)"
    box.size.width = at_least(10)
    assert repr(box.size) == "(at least 10, 2)"


@pytest.mark.parametrize("dimension", ["width", "height"])
@pytest.mark.parametrize("minimum", [True, False])
def test_set_dimension(box, dimension, minimum):
    dim = at_least if minimum else lambda x: x

    setattr(box.size, dimension, dim(10))
    assert_size(box.size, BASE_SIZE.change(dimension, dim(10)))

    # Layout has been dirtied.
    box.layout.dirty.assert_called_once_with(**{f"intrinsic_{dimension}": dim(10)})

    # Clean the layout
    box.layout.dirty.reset_mock()

    # Set the width to the same value
    setattr(box.size, dimension, dim(10))
    assert_size(box.size, BASE_SIZE.change(dimension, dim(10)))

    # Layout has NOT been dirtied.
    box.layout.dirty.assert_not_called()

    if minimum:
        # Set the width to the same value, but not as a minimum
        setattr(box.size, dimension, 10)
        assert_size(box.size, BASE_SIZE.change(dimension, 10))

        # Layout has been dirtied.
        box.layout.dirty.assert_called_once_with(**{f"intrinsic_{dimension}": 10})

        # Clean the layout
        box.layout.dirty.reset_mock()

    # Set the width to something new
    setattr(box.size, dimension, dim(20))
    assert_size(box.size, BASE_SIZE.change(dimension, dim(20)))

    # Layout has been dirtied.
    box.layout.dirty.assert_called_once_with(**{f"intrinsic_{dimension}": dim(20)})
