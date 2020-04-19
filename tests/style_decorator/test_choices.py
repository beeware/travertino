from unittest import TestCase
from unittest.mock import Mock

from travertino.colors import NAMED_COLOR, rgb
from travertino.constants import TOP, GOLDENROD, REBECCAPURPLE
from travertino.declaration import Choices
from travertino.style_decorator import style
from travertino.style_properties import style_property


class StyleDecoratorPropertyChoiceTests(TestCase):
    def assert_property(self, obj, value, check_mock=True):
        self.assertEqual(obj.prop, value)
        if check_mock:
            obj.apply.assert_called_once_with('prop', value)
            obj.apply.reset_mock()

    def test_none(self):

        @style
        class MyObject:
            prop = style_property(choices=Choices(None), initial=None)
            apply = Mock()

        obj = MyObject()
        self.assertIsNone(obj.prop)

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE

        with self.assertRaises(ValueError):
            obj.prop = '#112233'

        with self.assertRaises(ValueError):
            obj.prop = 'a'

        with self.assertRaises(ValueError):
            obj.prop = 'b'

        obj.prop = None
        self.assert_property(obj, None, check_mock=False)

        obj.prop = 'none'
        self.assert_property(obj, None, check_mock=False)

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property 'prop'; Valid values are: none"
            )

    def test_allow_string(self):
        @style
        class MyObject:
            prop = style_property(choices=Choices(string=True), initial='start')
            apply = Mock()

        obj = MyObject()
        self.assertEqual(obj.prop, 'start')

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        obj.prop = REBECCAPURPLE
        self.assert_property(obj, 'rebeccapurple')

        obj.prop = '#112233'
        self.assert_property(obj, '#112233')

        obj.prop = 'a'
        self.assert_property(obj, 'a')

        obj.prop = 'b'
        self.assert_property(obj, 'b')

        with self.assertRaises(ValueError):
            obj.prop = None

        obj.prop = 'none'
        self.assert_property(obj, 'none')

        # Check the error message
        try:
            obj.prop = 99
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value '99' for property 'prop'; Valid values are: <string>"
            )

    def test_allow_integer(self):
        @style
        class MyObject:
            apply = Mock()
            prop = style_property(choices=Choices(integer=True), initial=0)

        obj = MyObject()
        self.assertEqual(obj.prop, 0)

        obj.prop = 10
        self.assert_property(obj, 10)

        # This is an odd case; Python happily rounds floats to integers.
        # It's more trouble than it's worth to correct this.
        obj.prop = 3.14159
        self.assert_property(obj, 3)

        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE

        with self.assertRaises(ValueError):
            obj.prop = '#112233'

        with self.assertRaises(ValueError):
            obj.prop = 'a'

        with self.assertRaises(ValueError):
            obj.prop = 'b'

        with self.assertRaises(ValueError):
            obj.prop = None

        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property 'prop'; "
                "Valid values are: <integer>"
            )

    def test_allow_number(self):
        @style
        class MyObject:
            prop = style_property(choices=Choices(number=True), initial=0)
            apply = Mock()

        obj = MyObject()
        self.assertEqual(obj.prop, 0)

        obj.prop = 10
        self.assert_property(obj, 10.0)

        obj.prop = 3.14159
        self.assert_property(obj, 3.14159)

        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE

        with self.assertRaises(ValueError):
            obj.prop = '#112233'

        with self.assertRaises(ValueError):
            obj.prop = 'a'

        with self.assertRaises(ValueError):
            obj.prop = 'b'

        with self.assertRaises(ValueError):
            obj.prop = None

        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property 'prop'; "
                "Valid values are: <number>"
            )

    def test_allow_color(self):
        @style
        class MyObject:
            apply = Mock()
            prop = style_property(choices=Choices(color=True), initial='goldenrod')

        obj = MyObject()
        self.assertEqual(obj.prop, NAMED_COLOR[GOLDENROD])

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        obj.prop = REBECCAPURPLE
        self.assert_property(obj, NAMED_COLOR[REBECCAPURPLE])

        obj.prop = '#112233'
        self.assert_property(obj, rgb(0x11, 0x22, 0x33))

        with self.assertRaises(ValueError):
            obj.prop = 'a'

        with self.assertRaises(ValueError):
            obj.prop = 'b'

        with self.assertRaises(ValueError):
            obj.prop = None

        with self.assertRaises(ValueError):
            obj.prop = 'none'

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property 'prop'; "
                "Valid values are: <color>"
            )

    def test_values(self):
        @style
        class MyObject:
            apply = Mock()
            prop = style_property(choices=Choices('a', 'b', None), initial='a')

        obj = MyObject()
        self.assertEqual(obj.prop, 'a')

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE

        with self.assertRaises(ValueError):
            obj.prop = '#112233'

        obj.prop = None
        self.assert_property(obj, None)

        obj.prop = 'a'
        self.assert_property(obj, 'a')

        obj.prop = 'none'
        self.assert_property(obj, None)

        obj.prop = 'b'
        self.assert_property(obj, 'b')


        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property 'prop'; "
                "Valid values are: a, b, none"
            )

    def test_multiple_choices(self):
        @style
        class MyObject:
            apply = Mock()
            prop = style_property(choices=Choices(
                    'a', 'b', None,
                    number=True, color=True
                ), initial=None)

        obj = MyObject()

        obj.prop = 10
        self.assert_property(obj, 10.0)

        obj.prop = 3.14159
        self.assert_property(obj, 3.14159)

        obj.prop = REBECCAPURPLE
        self.assert_property(obj, NAMED_COLOR[REBECCAPURPLE])

        obj.prop = '#112233'
        self.assert_property(obj, rgb(0x11, 0x22, 0x33))

        obj.prop = None
        self.assert_property(obj, None)

        obj.prop = 'a'
        self.assert_property(obj, 'a')

        obj.prop = 'none'
        self.assert_property(obj, None)

        obj.prop = 'b'
        self.assert_property(obj, 'b')

        # Check the error message
        try:
            obj.prop = 'invalid'
            self.fail('Should raise ValueError')
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property 'prop'; "
                "Valid values are: a, b, none, <number>, <color>"
            )

    def test_string_symbol(self):
        @style
        class MyObject:
            apply = Mock()
            prop = style_property(choices=Choices(TOP, None), initial=None)

        obj = MyObject()

        # Set a symbolic value using the string value of the symbol
        # We can't just use the string directly, though - that would
        # get optimized by the compiler. So we create a string and
        # transform it into the value we want.
        val = 'TOP'
        obj.prop = val.lower()

        # Both equality and instance checking should work.
        self.assertEqual(obj.prop, TOP)
        self.assertIs(obj.prop, TOP)
