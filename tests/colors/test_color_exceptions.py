from unittest import TestCase

from travertino.colors import rgb, rgba


class RGBColorExceptionTests(TestCase):

    def test_negative_red(self):
        self.assertRaisesRegex(
            ValueError, "^red value should be between 0-255. Got -1$", rgb, -1, 120, 10
        )

    def test_too_big_red(self):
        self.assertRaisesRegex(
            ValueError,
            "^red value should be between 0-255. Got 256$",
            rgb,
            256,
            120,
            10
        )

    def test_negative_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got -1$",
            rgb,
            120,
            -1,
            10
        )

    def test_too_big_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got 256$",
            rgb,
            120,
            256,
            10
        )

    def test_negative_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got -1$",
            rgb,
            120,
            10,
            -1
        )

    def test_too_big_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got 256$",
            rgb,
            120,
            10,
            256
        )


class RGBAColorExceptionTests(TestCase):

    def test_negative_red(self):
        self.assertRaisesRegex(
            ValueError,
            "^red value should be between 0-255. Got -1$",
            rgba,
            -1,
            120,
            10,
            0.5
        )

    def test_too_big_red(self):
        self.assertRaisesRegex(
            ValueError,
            "^red value should be between 0-255. Got 256$",
            rgba,
            256,
            120,
            10,
            0.5
        )

    def test_negative_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got -1$",
            rgba,
            120,
            -1,
            10,
            0.5
        )

    def test_too_big_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got 256$",
            rgba,
            120,
            256,
            10,
            0.5
        )

    def test_negative_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got -1$",
            rgba,
            120,
            10,
            -1,
            0.5
        )

    def test_too_big_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got 256$",
            rgba,
            120,
            10,
            256,
            0.5
        )

    def test_negative_alpha(self):
        self.assertRaisesRegex(
            ValueError,
            "^alpha value should be between 0-1. Got -0.5$",
            rgba,
            120,
            10,
            60,
            -0.5
        )

    def test_too_big_alpha(self):
        self.assertRaisesRegex(
            ValueError,
            "^alpha value should be between 0-1. Got 1.1",
            rgba,
            120,
            10,
            60,
            1.1
        )
