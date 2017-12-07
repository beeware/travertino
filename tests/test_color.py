from unittest import TestCase

from travertino.colors import color, hsl, hsla, rgb, rgba


class ColorTests(TestCase):
    def assertEqualColor(self, a, b):
        self.assertEqual(a.rgba.r, b.rgba.r)
        self.assertEqual(a.rgba.g, b.rgba.g)
        self.assertEqual(a.rgba.b, b.rgba.b)
        self.assertEqual(a.rgba.a, b.rgba.a)

    def test_rgb_repr(self):
        self.assertEqual(repr(rgb(10, 20, 30)), "rgb(10, 20, 30)")

    def test_rgba_repr(self):
        self.assertEqual(repr(rgba(10, 20, 30, 0.5)), "rgba(10, 20, 30, 0.5)")

    def test_hsl_repr(self):
        self.assertEqual(repr(hsl(10, 0.2, 0.3)), "hsl(10, 0.2, 0.3)")

    def test_hsla_repr(self):
        self.assertEqual(repr(hsla(10, 0.2, 0.3, 0.5)), "hsla(10, 0.2, 0.3, 0.5)")

    def test_hsl_blacks(self):
        self.assertEqualColor(hsl(0, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(60, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(180, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(240, 0.0, 0.0), rgb(0x00, 0x00, 0x00))
        self.assertEqualColor(hsl(360, 0.0, 0.0), rgb(0x00, 0x00, 0x00))

    def test_hsl_whites(self):
        self.assertEqualColor(hsl(0, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(60, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(180, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(240, 0.0, 1.0), rgb(0xff, 0xff, 0xff))
        self.assertEqualColor(hsl(360, 0.0, 1.0), rgb(0xff, 0xff, 0xff))

    def test_hsl_grays(self):
        self.assertEqualColor(hsl(0, 0.0, 0.2), rgb(0x33, 0x33, 0x33))
        self.assertEqualColor(hsl(0, 0.0, 0.4), rgb(0x66, 0x66, 0x66))
        self.assertEqualColor(hsl(0, 0.0, 0.5), rgb(0x80, 0x80, 0x80))
        self.assertEqualColor(hsl(0, 0.0, 0.6), rgb(0x99, 0x99, 0x99))
        self.assertEqualColor(hsl(0, 0.0, 0.8), rgb(0xcc, 0xcc, 0xcc))

    def test_hsl_primaries(self):
        self.assertEqualColor(hsl(0, 1.0, 0.5), rgb(0xff, 0x00, 0x00))
        self.assertEqualColor(hsl(60, 1.0, 0.5), rgb(0xff, 0xff, 0x00))
        self.assertEqualColor(hsl(120, 1.0, 0.5), rgb(0x00, 0xff, 0x00))
        self.assertEqualColor(hsl(180, 1.0, 0.5), rgb(0x00, 0xff, 0xff))
        self.assertEqualColor(hsl(240, 1.0, 0.5), rgb(0x00, 0x00, 0xff))
        self.assertEqualColor(hsl(300, 1.0, 0.5), rgb(0xff, 0x00, 0xff))
        self.assertEqualColor(hsl(360, 1.0, 0.5), rgb(0xff, 0x00, 0x00))

    def test_hsl_muted(self):
        self.assertEqualColor(hsl(0, 0.25, 0.25), rgb(0x50, 0x30, 0x30))
        self.assertEqualColor(hsl(60, 0.25, 0.25), rgb(0x50, 0x50, 0x30))
        self.assertEqualColor(hsl(120, 0.25, 0.25), rgb(0x30, 0x50, 0x30))
        self.assertEqualColor(hsl(180, 0.25, 0.25), rgb(0x30, 0x50, 0x50))
        self.assertEqualColor(hsl(240, 0.25, 0.25), rgb(0x30, 0x30, 0x50))
        self.assertEqualColor(hsl(300, 0.25, 0.25), rgb(0x50, 0x30, 0x50))
        self.assertEqualColor(hsl(360, 0.25, 0.25), rgb(0x50, 0x30, 0x30))

        self.assertEqualColor(hsl(0, 0.25, 0.75), rgb(0xcf, 0xaf, 0xaf))
        self.assertEqualColor(hsl(60, 0.25, 0.75), rgb(0xcf, 0xcf, 0xaf))
        self.assertEqualColor(hsl(120, 0.25, 0.75), rgb(0xaf, 0xcf, 0xaf))
        self.assertEqualColor(hsl(180, 0.25, 0.75), rgb(0xaf, 0xcf, 0xcf))
        self.assertEqualColor(hsl(240, 0.25, 0.75), rgb(0xaf, 0xaf, 0xcf))
        self.assertEqualColor(hsl(300, 0.25, 0.75), rgb(0xcf, 0xaf, 0xcf))
        self.assertEqualColor(hsl(360, 0.25, 0.75), rgb(0xcf, 0xaf, 0xaf))

        self.assertEqualColor(hsl(0, 0.75, 0.75), rgb(0xef, 0x8f, 0x8f))
        self.assertEqualColor(hsl(60, 0.75, 0.75), rgb(0xef, 0xef, 0x8f))
        self.assertEqualColor(hsl(120, 0.75, 0.75), rgb(0x8f, 0xef, 0x8f))
        self.assertEqualColor(hsl(180, 0.75, 0.75), rgb(0x8f, 0xef, 0xef))
        self.assertEqualColor(hsl(240, 0.75, 0.75), rgb(0x8f, 0x8f, 0xef))
        self.assertEqualColor(hsl(300, 0.75, 0.75), rgb(0xef, 0x8f, 0xef))
        self.assertEqualColor(hsl(360, 0.75, 0.75), rgb(0xef, 0x8f, 0x8f))

        self.assertEqualColor(hsl(0, 0.75, 0.25), rgb(0x70, 0x10, 0x10))
        self.assertEqualColor(hsl(60, 0.75, 0.25), rgb(0x70, 0x70, 0x10))
        self.assertEqualColor(hsl(120, 0.75, 0.25), rgb(0x10, 0x70, 0x10))
        self.assertEqualColor(hsl(180, 0.75, 0.25), rgb(0x10, 0x70, 0x70))
        self.assertEqualColor(hsl(240, 0.75, 0.25), rgb(0x10, 0x10, 0x70))
        self.assertEqualColor(hsl(300, 0.75, 0.25), rgb(0x70, 0x10, 0x70))
        self.assertEqualColor(hsl(360, 0.75, 0.25), rgb(0x70, 0x10, 0x10))

    def test_hsl_alpha(self):
        self.assertEqualColor(hsla(60, 0.0, 0.0, 0.3), rgba(0x00, 0x00, 0x00, 0.3))
        self.assertEqualColor(hsla(60, 0.0, 1.0, 0.3), rgba(0xff, 0xff, 0xff, 0.3))
        self.assertEqualColor(hsla(60, 1.0, 0.5, 0.3), rgba(0xff, 0xff, 0x00, 0.3))
        self.assertEqualColor(hsla(60, 0.25, 0.25, 0.3), rgba(0x50, 0x50, 0x30, 0.3))
        self.assertEqualColor(hsla(60, 0.25, 0.75, 0.3), rgba(0xcf, 0xcf, 0xaf, 0.3))
        self.assertEqualColor(hsla(60, 0.75, 0.75, 0.3), rgba(0xef, 0xef, 0x8f, 0.3))
        self.assertEqualColor(hsla(60, 0.75, 0.25, 0.3), rgba(0x70, 0x70, 0x10, 0.3))


class ParseColorTests(TestCase):
    def assertEqualHSL(self, value, expected):
        # Nothing fancy - a color is equal if the attributes are all the same
        actual = color(value)
        self.assertEqual(actual.h, expected.h)
        self.assertEqual(actual.s, expected.s)
        self.assertEqual(actual.l, expected.l)
        self.assertAlmostEqual(actual.a, expected.a, places=3)

    def assertEqualColor(self, value, expected):
        # Nothing fancy - a color is equal if the attributes are all the same
        actual = color(value)
        self.assertEqual(actual.r, expected.r)
        self.assertEqual(actual.g, expected.g)
        self.assertEqual(actual.b, expected.b)
        self.assertAlmostEqual(actual.a, expected.a, places=3)

    def test_noop(self):
        self.assertEqualColor(rgba(1, 2, 3, 0.5), rgba(1, 2, 3, 0.5))
        self.assertEqualHSL(hsl(1, 0.2, 0.3), hsl(1, 0.2, 0.3))

    def test_rgb(self):
        self.assertEqualColor('rgb(1,2,3)', rgb(1, 2, 3))
        self.assertEqualColor('rgb(1, 2, 3)', rgb(1, 2, 3))
        self.assertEqualColor('rgb( 1 , 2 , 3)', rgb(1, 2, 3))

        self.assertEqualColor('#123', rgb(0x11, 0x22, 0x33))
        self.assertEqualColor('#112233', rgb(0x11, 0x22, 0x33))
        self.assertEqualColor('#abc', rgb(0xaa, 0xbb, 0xcc))
        self.assertEqualColor('#ABC', rgb(0xaa, 0xbb, 0xcc))
        self.assertEqualColor('#abcdef', rgb(0xab, 0xcd, 0xef))
        self.assertEqualColor('#ABCDEF', rgb(0xab, 0xcd, 0xef))

        with self.assertRaises(ValueError):
            color('rgb(10, 20)')

        with self.assertRaises(ValueError):
            color('rgb(a, 10, 20)')

        with self.assertRaises(ValueError):
            color('rgb(10, b, 20)')

        with self.assertRaises(ValueError):
            color('rgb(10, 20, c)')

        with self.assertRaises(ValueError):
            color('rgb(10, 20, 30, 0.5)')

    def test_rgba(self):
        self.assertEqualColor('rgba(1,2,3,0.5)', rgba(1, 2, 3, 0.5))
        self.assertEqualColor('rgba(1, 2, 3, 0.5)', rgba(1, 2, 3, 0.5))
        self.assertEqualColor('rgba( 1 , 2 , 3 , 0.5)', rgba(1, 2, 3, 0.5))

        self.assertEqualColor('#1234', rgba(0x11, 0x22, 0x33, 0.2666))
        self.assertEqualColor('#11223344', rgba(0x11, 0x22, 0x33, 0.2666))
        self.assertEqualColor('#abcd', rgba(0xaa, 0xbb, 0xcc, 0.8666))
        self.assertEqualColor('#ABCD', rgba(0xaa, 0xbb, 0xcc, 0.8666))
        self.assertEqualColor('#abcdefba', rgba(0xab, 0xcd, 0xef, 0.7294))
        self.assertEqualColor('#ABCDEFBA', rgba(0xab, 0xcd, 0xef, 0.7294))

        with self.assertRaises(ValueError):
            color('rgba(10, 20, 30)')

        with self.assertRaises(ValueError):
            color('rgba(a, 10, 20, 0.5)')

        with self.assertRaises(ValueError):
            color('rgba(10, b, 20, 0.5)')

        with self.assertRaises(ValueError):
            color('rgba(10, 20, c, 0.5)')

        with self.assertRaises(ValueError):
            color('rgba(10, 20, 30, c)')

        with self.assertRaises(ValueError):
            color('rgba(10, 20, 30, 0.5, 5)')

    def test_hsl(self):
        self.assertEqualHSL('hsl(1,20%,30%)', hsl(1, 0.2, 0.3))
        self.assertEqualHSL('hsl(1, 20%, 30%)', hsl(1, 0.2, 0.3))
        self.assertEqualHSL('hsl( 1, 20% , 30%)', hsl(1, 0.2, 0.3))

        with self.assertRaises(ValueError):
            color('hsl(1, 20%)')

        with self.assertRaises(ValueError):
            color('hsl(a, 20%, 30%)')

        with self.assertRaises(ValueError):
            color('hsl(1, a, 30%)')

        with self.assertRaises(ValueError):
            color('hsl(1, 20%, a)')

        with self.assertRaises(ValueError):
            color('hsl(1, 20%, 30%, 0.5)')

    def test_hsla(self):
        self.assertEqualHSL('hsla(1,20%,30%,0.5)', hsla(1, 0.2, 0.3, 0.5))
        self.assertEqualHSL('hsla(1, 20%, 30%, 0.5)', hsla(1, 0.2, 0.3, 0.5))
        self.assertEqualHSL('hsla( 1, 20% , 30% , 0.5)', hsla(1, 0.2, 0.3, 0.5))

        with self.assertRaises(ValueError):
            color('hsla(1, 20%, 30%)')

        with self.assertRaises(ValueError):
            color('hsla(a, 20%, 30%, 0.5)')

        with self.assertRaises(ValueError):
            color('hsla(1, a, 30%, 0.5)')

        with self.assertRaises(ValueError):
            color('hsla(1, 20%, a, 0.5)')

        with self.assertRaises(ValueError):
            color('hsla(1, 20%, 30%, a)')

        with self.assertRaises(ValueError):
            color('hsla(1, 20%, 30%, 0.5, 5)')

    def test_named_color(self):
        self.assertEqualColor('Red', rgb(0xFF, 0, 0))
        self.assertEqualColor('RED', rgb(0xFF, 0, 0))
        self.assertEqualColor('red', rgb(0xFF, 0, 0))
        self.assertEqualColor('rEd', rgb(0xFF, 0, 0))

        self.assertEqualColor('CornflowerBlue', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('cornflowerblue', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('CORNFLOWERBLUE', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('Cornflowerblue', rgb(0x64, 0x95, 0xED))
        self.assertEqualColor('CoRnFlOwErBlUe', rgb(0x64, 0x95, 0xED))

        with self.assertRaises(ValueError):
            color('not a color')
