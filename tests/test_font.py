from unittest import TestCase

from travertino.constants import NORMAL, ITALIC, OBLIQUE, SMALL_CAPS, BOLD
from travertino.fonts import font, Font


class FontTests(TestCase):
    def assertFont(self, font, family, size, style, variant, weight):
        self.assertEqual(font.family, family)
        self.assertEqual(font.size, size)
        self.assertEqual(font.style, style)
        self.assertEqual(font.variant, variant)
        self.assertEqual(font.weight, weight)

    def test_equality(self):
        self.assertEqual(
            Font('Comic Sans', '12 pt'),
            Font('Comic Sans', 12, NORMAL, NORMAL, NORMAL)
        )

    def test_hash(self):
        self.assertEqual(
            hash(Font('Comic Sans', 12)),
            hash(Font('Comic Sans', 12)),
        )

        self.assertNotEqual(
            hash(Font('Comic Sans', 12, weight=BOLD)),
            hash(Font('Comic Sans', 12)),
        )

    def test_repr(self):
        self.assertEqual(
            repr(Font('Comic Sans', 12)),
            '<Font: 12pt Comic Sans>'
        )

        self.assertEqual(
            repr(Font('Comic Sans', 12, style=ITALIC)),
            '<Font: italic 12pt Comic Sans>'
        )

        self.assertEqual(
            repr(Font('Comic Sans', 12, style=ITALIC, variant=SMALL_CAPS)),
            '<Font: italic small-caps 12pt Comic Sans>'
        )

        self.assertEqual(
            repr(Font('Comic Sans', 12, style=ITALIC, variant=SMALL_CAPS, weight=BOLD)),
            '<Font: italic small-caps bold 12pt Comic Sans>'
        )

        self.assertEqual(
            repr(Font('Comic Sans', 12, variant=SMALL_CAPS, weight=BOLD)),
            '<Font: small-caps bold 12pt Comic Sans>'
        )

        self.assertEqual(
            repr(Font('Comic Sans', 12, weight=BOLD)),
            '<Font: bold 12pt Comic Sans>'
        )

        self.assertEqual(
            repr(Font('Comic Sans', 12, style=ITALIC, weight=BOLD)),
            '<Font: italic bold 12pt Comic Sans>'
        )

    def test_simple_construction(self):
        # Simplest case
        self.assertFont(
            Font('Comic Sans', 12),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        # String size
        self.assertFont(
            Font('Comic Sans', '12'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        # String size with 'pt'
        self.assertFont(
            Font('Comic Sans', '12pt'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', '12 pt'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        with self.assertRaises(ValueError):
            Font('Comic Sans', '12 quatloos'),

    def test_family(self):
        self.assertFont(
            Font('Comic Sans', 12),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            Font('Wingdings', 12),
            'Wingdings', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            Font("'Comic Sans'", 12),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            Font('"Comic Sans"', 12),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_style(self):
        self.assertFont(
            Font('Comic Sans', 12, style=ITALIC),
            'Comic Sans', 12, ITALIC, NORMAL, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', 12, style='italic'),
            'Comic Sans', 12, ITALIC, NORMAL, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', 12, style=OBLIQUE),
            'Comic Sans', 12, OBLIQUE, NORMAL, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', 12, style='oblique'),
            'Comic Sans', 12, OBLIQUE, NORMAL, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', 12, style='something else'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_make_normal_style(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.normal_style(),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        f = Font('Comic Sans', 12, style=ITALIC)
        self.assertFont(
            f.normal_style(),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_make_italic(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.italic(),
            'Comic Sans', 12, ITALIC, NORMAL, NORMAL
        )

    def test_make_oblique(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.oblique(),
            'Comic Sans', 12, OBLIQUE, NORMAL, NORMAL
        )

    def test_variant(self):
        self.assertFont(
            Font('Comic Sans', 12, variant=SMALL_CAPS),
            'Comic Sans', 12, NORMAL, SMALL_CAPS, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', 12, variant='small-caps'),
            'Comic Sans', 12, NORMAL, SMALL_CAPS, NORMAL
        )

        self.assertFont(
            Font('Comic Sans', 12, variant='something else'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_make_normal_variant(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.normal_variant(),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        f = Font('Comic Sans', 12, variant=SMALL_CAPS)
        self.assertFont(
            f.normal_variant(),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_make_small_caps(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.small_caps(),
            'Comic Sans', 12, NORMAL, SMALL_CAPS, NORMAL
        )

    def test_weight(self):
        self.assertFont(
            Font('Comic Sans', 12, weight=BOLD),
            'Comic Sans', 12, NORMAL, NORMAL, BOLD
        )

        self.assertFont(
            Font('Comic Sans', 12, weight='bold'),
            'Comic Sans', 12, NORMAL, NORMAL, BOLD
        )

        self.assertFont(
            Font('Comic Sans', 12, weight='something else'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_make_normal_weight(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.normal_weight(),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        f = Font('Comic Sans', 12, weight=BOLD)
        self.assertFont(
            f.normal_weight(),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_make_bold(self):
        f = Font('Comic Sans', 12)
        self.assertFont(
            f.bold(),
            'Comic Sans', 12, NORMAL, NORMAL, BOLD
        )


class ParseFontTests(TestCase):
    def assertFont(self, font, family, size, style, variant, weight):
        self.assertEqual(font.family, family)
        self.assertEqual(font.size, size)
        self.assertEqual(font.style, style)
        self.assertEqual(font.variant, variant)
        self.assertEqual(font.weight, weight)

    def test_font_instance(self):
        f = Font('Comic Sans', 12)

        parsed = font(f)

        self.assertEqual(f, parsed)
        self.assertIs(f, parsed)

    def test_successful_combinations(self):
        self.assertFont(
            font('12pt Comic Sans'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            font('italic 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, NORMAL, NORMAL
        )

        self.assertFont(
            font('italic small-caps 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, SMALL_CAPS, NORMAL
        )

        self.assertFont(
            font('italic small-caps bold 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, SMALL_CAPS, BOLD
        )

        self.assertFont(
            font('small-caps bold 12pt Comic Sans'),
            'Comic Sans', 12, NORMAL, SMALL_CAPS, BOLD
        )

        self.assertFont(
            font('italic bold 12 pt Comic Sans'),
            'Comic Sans', 12, ITALIC, NORMAL, BOLD
        )

        self.assertFont(
            font('bold 12 pt Comic Sans'),
            'Comic Sans', 12, NORMAL, NORMAL, BOLD
        )

    def test_font_sizes(self):
        self.assertFont(
            font('12pt Comic Sans'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            font('12 pt Comic Sans'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            font('12 Comic Sans'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        with self.assertRaises(ValueError):
            font('12quatloo Comic Sans')

    def test_font_family(self):
        self.assertFont(
            font("12pt 'Comic Sans'"),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            font('12pt "Comic Sans"'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

    def test_normal(self):
        self.assertFont(
            font('normal 12pt Comic Sans'),
            'Comic Sans', 12, NORMAL, NORMAL, NORMAL
        )

        self.assertFont(
            font('italic normal 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, NORMAL, NORMAL
        )

        self.assertFont(
            font('italic small-caps normal 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, SMALL_CAPS, NORMAL
        )

    def test_style(self):
        self.assertFont(
            font('italic 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, NORMAL, NORMAL
        )

        self.assertFont(
            font('oblique 12pt Comic Sans'),
            'Comic Sans', 12, OBLIQUE, NORMAL, NORMAL
        )

        with self.assertRaises(ValueError):
            font('wiggly small-caps bold 12pt Comic Sans')

    def test_variant(self):
        self.assertFont(
            font('italic small-caps 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, SMALL_CAPS, NORMAL
        )

        with self.assertRaises(ValueError):
            font('italic wiggly bold 12pt Comic Sans')

    def test_weight(self):
        self.assertFont(
            font('italic small-caps bold 12pt Comic Sans'),
            'Comic Sans', 12, ITALIC, SMALL_CAPS, BOLD
        )

        with self.assertRaises(ValueError):
            font('italic small-caps wiggly 12pt Comic Sans')

    def test_duplicates(self):
        with self.assertRaises(ValueError):
            font('oblique italic 12pt Comic Sans')

        with self.assertRaises(ValueError):
            font('italic small-caps oblique 12pt Comic Sans')

        with self.assertRaises(ValueError):
            font('italic small-caps bold small-caps 12pt Comic Sans')

        with self.assertRaises(ValueError):
            font('bold bold 12pt Comic Sans')

    def test_invaid(self):
        with self.assertRaises(ValueError):
            font(42)
