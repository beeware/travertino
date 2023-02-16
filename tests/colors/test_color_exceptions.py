from unittest import TestCase

from travertino.colors import hsl, hsla, rgb, rgba


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
            10,
        )

    def test_negative_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got -1$",
            rgb,
            120,
            -1,
            10,
        )

    def test_too_big_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got 256$",
            rgb,
            120,
            256,
            10,
        )

    def test_negative_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got -1$",
            rgb,
            120,
            10,
            -1,
        )

    def test_too_big_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got 256$",
            rgb,
            120,
            10,
            256,
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
            0.5,
        )

    def test_too_big_red(self):
        self.assertRaisesRegex(
            ValueError,
            "^red value should be between 0-255. Got 256$",
            rgba,
            256,
            120,
            10,
            0.5,
        )

    def test_negative_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got -1$",
            rgba,
            120,
            -1,
            10,
            0.5,
        )

    def test_too_big_green(self):
        self.assertRaisesRegex(
            ValueError,
            "^green value should be between 0-255. Got 256$",
            rgba,
            120,
            256,
            10,
            0.5,
        )

    def test_negative_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got -1$",
            rgba,
            120,
            10,
            -1,
            0.5,
        )

    def test_too_big_blue(self):
        self.assertRaisesRegex(
            ValueError,
            "^blue value should be between 0-255. Got 256$",
            rgba,
            120,
            10,
            256,
            0.5,
        )

    def test_negative_alpha(self):
        self.assertRaisesRegex(
            ValueError,
            "^alpha value should be between 0-1. Got -0.5$",
            rgba,
            120,
            10,
            60,
            -0.5,
        )

    def test_too_big_alpha(self):
        self.assertRaisesRegex(
            ValueError,
            "^alpha value should be between 0-1. Got 1.1",
            rgba,
            120,
            10,
            60,
            1.1,
        )


class HSLColorExceptionTests(TestCase):
    def test_negative_hue(self):
        self.assertRaisesRegex(
            ValueError,
            "^hue value should be between 0-360. Got -1$",
            hsl,
            -1,
            0.5,
            0.8,
        )

    def test_too_big_hue(self):
        self.assertRaisesRegex(
            ValueError,
            "^hue value should be between 0-360. Got 361$",
            hsl,
            361,
            0.5,
            0.8,
        )

    def test_negative_saturation(self):
        self.assertRaisesRegex(
            ValueError,
            "^saturation value should be between 0-1. Got -0.1$",
            hsl,
            120,
            -0.1,
            0.8,
        )

    def test_too_big_saturation(self):
        self.assertRaisesRegex(
            ValueError,
            "^saturation value should be between 0-1. Got 1.1$",
            hsl,
            120,
            1.1,
            0.8,
        )

    def test_negative_lightness(self):
        self.assertRaisesRegex(
            ValueError,
            "^lightness value should be between 0-1. Got -0.1$",
            hsl,
            120,
            0.8,
            -0.1,
        )

    def test_too_big_lightness(self):
        self.assertRaisesRegex(
            ValueError,
            "^lightness value should be between 0-1. Got 1.1$",
            hsl,
            120,
            0.8,
            1.1,
        )


class HSLAColorExceptionTests(TestCase):
    def test_negative_hue(self):
        self.assertRaisesRegex(
            ValueError,
            "^hue value should be between 0-360. Got -1$",
            hsla,
            -1,
            0.5,
            0.8,
            0.5,
        )

    def test_too_big_hue(self):
        self.assertRaisesRegex(
            ValueError,
            "^hue value should be between 0-360. Got 361$",
            hsla,
            361,
            0.5,
            0.8,
            0.5,
        )

    def test_negative_saturation(self):
        self.assertRaisesRegex(
            ValueError,
            "^saturation value should be between 0-1. Got -0.1$",
            hsla,
            120,
            -0.1,
            0.8,
            0.5,
        )

    def test_too_big_saturation(self):
        self.assertRaisesRegex(
            ValueError,
            "^saturation value should be between 0-1. Got 1.1$",
            hsla,
            120,
            1.1,
            0.8,
            0.5,
        )

    def test_negative_lightness(self):
        self.assertRaisesRegex(
            ValueError,
            "^lightness value should be between 0-1. Got -0.1$",
            hsla,
            120,
            0.8,
            -0.1,
            0.5,
        )

    def test_too_big_lightness(self):
        self.assertRaisesRegex(
            ValueError,
            "^lightness value should be between 0-1. Got 1.1$",
            hsla,
            120,
            0.8,
            1.1,
            0.5,
        )

    def test_negative_alpha(self):
        self.assertRaisesRegex(
            ValueError,
            "^alpha value should be between 0-1. Got -0.1$",
            hsla,
            120,
            0.8,
            0.5,
            -0.1,
        )

    def test_too_big_alpha(self):
        self.assertRaisesRegex(
            ValueError,
            "^alpha value should be between 0-1. Got 1.1$",
            hsla,
            120,
            0.8,
            0.5,
            1.1,
        )
