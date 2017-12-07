from unittest import TestCase
from unittest.mock import Mock

from travertino.size import IntrinsicSize, at_least


class SizeTests(TestCase):
    def assertSize(self, size, values):
        self.assertEqual(values[0], size.width)
        self.assertEqual(values[1], size.height)
        self.assertEqual(values[2], size.ratio)

    def setUp(self):
        self.maxDiff = None

        self.layout = Mock()
        self.size = IntrinsicSize(self.layout)
        self.size._width = 1
        self.size._height = 2
        self.size._ratio = 0.1

        self.assertSize(self.size, (1, 2, 0.1))

    def test_repr(self):
        self.assertEqual(repr(at_least(10)), 'at least 10')

    def test_set_width(self):
        self.size.width = 10
        self.assertSize(self.size, (10, 2, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_width=10)

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the width to the same value
        self.size.width = 10
        self.assertSize(self.size, (10, 2, 0.1))

        # Layout has NOT been dirtied.
        self.layout.dirty.assert_not_called()

        # Set the width to something new
        self.size.width = 20
        self.assertSize(self.size, (20, 2, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_width=20)

    def test_set_height(self):
        self.size.height = 10
        self.assertSize(self.size, (1, 10, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_height=10)

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the height to the same value
        self.size.height = 10
        self.assertSize(self.size, (1, 10, 0.1))

        # Layout has NOT been dirtied.
        self.layout.dirty.assert_not_called()

        # Set the height to something new
        self.size.height = 20
        self.assertSize(self.size, (1, 20, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_height=20)

    def test_set_min_width(self):
        self.size.width = at_least(10)
        self.assertSize(self.size, (at_least(10), 2, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_width=at_least(10))

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the exact_width to the same value
        self.size.width = at_least(10)
        self.assertSize(self.size, (at_least(10), 2, 0.1))

        # Layout has NOT been dirtied.
        self.layout.dirty.assert_not_called()

        # Set the exact_width to the same value, but not as a minimum
        self.size.width = 10
        self.assertSize(self.size, (10, 2, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_width=10)

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the exact_width to something new
        self.size.width = at_least(20)
        self.assertSize(self.size, (at_least(20), 2, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_width=at_least(20))

    def test_set_min_height(self):
        self.size.height = at_least(10)
        self.assertSize(self.size, (1, at_least(10), 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_height=at_least(10))

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the exact height to the same value
        self.size.height = at_least(10)
        self.assertSize(self.size, (1, at_least(10), 0.1))

        # Layout has NOT been dirtied.
        self.layout.dirty.assert_not_called()

        # Set the exact_height to the same value, but not as a minimum
        self.size.height = 10
        self.assertSize(self.size, (1, 10, 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_height=10)

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the exact height to something else
        self.size.height = at_least(20)
        self.assertSize(self.size, (1, at_least(20), 0.1))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_height=at_least(20))

    def test_set_ratio(self):
        self.size.ratio = 0.5
        self.assertSize(self.size, (1, 2, 0.5))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_ratio=0.5)

        # Clean the layout
        self.layout.dirty.reset_mock()

        # Set the ratio to the same value
        self.size.ratio = 0.5
        self.assertSize(self.size, (1, 2, 0.5))

        # Layout has NOT been dirtied.
        self.layout.dirty.assert_not_called()

        # Set the ratio to something else
        self.size.ratio = 0.75
        self.assertSize(self.size, (1, 2, 0.75))

        # Layout has been dirtied.
        self.layout.dirty.assert_called_once_with(intrinsic_ratio=0.75)
