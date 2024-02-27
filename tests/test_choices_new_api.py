from __future__ import annotations

import sys
from dataclasses import dataclass
from unittest import TestCase
from unittest.mock import Mock

from travertino.colors import NAMED_COLOR, rgb
from travertino.constants import GOLDENROD, NONE, REBECCAPURPLE, TOP
from travertino.declaration import BaseStyle, Choices, validated_property

if sys.version_info < (3, 10):
    _DATACLASS_KWARGS = {"init": False}
else:
    _DATACLASS_KWARGS = {"kw_only": True}


def prep_style_class(cls):
    """Decorator to apply dataclass and mock a style class's apply method."""
    orig_init = cls.__init__

    def __init__(self, *args, **kwargs):
        self.apply = Mock()
        orig_init(self, *args, **kwargs)

    cls.__init__ = __init__
    return dataclass(**_DATACLASS_KWARGS)(cls)


class PropertyChoiceTests(TestCase):
    def assert_property(self, obj, value, check_mock=True):
        self.assertEqual(obj.prop, value)
        if check_mock:
            obj.apply.assert_called_once_with("prop", value)
            obj.apply.reset_mock()

    def test_none(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: str = validated_property(
                choices=Choices(NONE, REBECCAPURPLE), initial=NONE
            )

        obj = MyObject()
        self.assert_property(obj, NONE, check_mock=False)

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        with self.assertRaises(ValueError):
            obj.prop = "#112233"

        with self.assertRaises(ValueError):
            obj.prop = "a"

        with self.assertRaises(ValueError):
            obj.prop = "b"

        # Set the property to a different explicit value
        obj.prop = REBECCAPURPLE
        self.assert_property(obj, REBECCAPURPLE)

        # A Travertino NONE is an explicit value
        obj.prop = NONE
        self.assert_property(obj, NONE)

        # Set the property to a different explicit value
        obj.prop = REBECCAPURPLE
        self.assert_property(obj, REBECCAPURPLE)

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        del obj.prop
        self.assert_property(obj, NONE)

        # Check the error message
        try:
            obj.prop = "invalid"
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property prop; Valid values are: none, rebeccapurple",
            )

    def test_allow_string(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: str = validated_property(
                choices=Choices(string=True), initial="start"
            )

        obj = MyObject()
        self.assertEqual(obj.prop, "start")

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        obj.prop = REBECCAPURPLE
        self.assert_property(obj, "rebeccapurple")

        obj.prop = "#112233"
        self.assert_property(obj, "#112233")

        obj.prop = "a"
        self.assert_property(obj, "a")

        obj.prop = "b"
        self.assert_property(obj, "b")

        # A Travertino NONE is an explicit string value
        obj.prop = NONE
        self.assert_property(obj, NONE)

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        del obj.prop
        self.assert_property(obj, "start")

        # Check the error message
        try:
            obj.prop = 99
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v), "Invalid value 99 for property prop; Valid values are: <string>"
            )

    def test_allow_integer(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: int = validated_property(choices=Choices(integer=True), initial=0)

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
            obj.prop = "#112233"

        with self.assertRaises(ValueError):
            obj.prop = "a"

        with self.assertRaises(ValueError):
            obj.prop = "b"

        # A Travertino NONE is an explicit string value
        with self.assertRaises(ValueError):
            obj.prop = NONE

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        del obj.prop
        self.assert_property(obj, 0)

        # Check the error message
        try:
            obj.prop = "invalid"
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property prop; Valid values are: <integer>",
            )

    def test_allow_number(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: float = validated_property(choices=Choices(number=True), initial=0)

        obj = MyObject()
        self.assertEqual(obj.prop, 0)

        obj.prop = 10
        self.assert_property(obj, 10.0)

        obj.prop = 3.14159
        self.assert_property(obj, 3.14159)

        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE

        with self.assertRaises(ValueError):
            obj.prop = "#112233"

        with self.assertRaises(ValueError):
            obj.prop = "a"

        with self.assertRaises(ValueError):
            obj.prop = "b"

        # A Travertino NONE is an explicit string value
        with self.assertRaises(ValueError):
            obj.prop = NONE

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        del obj.prop
        self.assert_property(obj, 0)

        # Check the error message
        try:
            obj.prop = "invalid"
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property prop; Valid values are: <number>",
            )

    def test_allow_color(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: str = validated_property(
                choices=Choices(color=True), initial="goldenrod"
            )

        obj = MyObject()
        self.assertEqual(obj.prop, NAMED_COLOR[GOLDENROD])

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        obj.prop = REBECCAPURPLE
        self.assert_property(obj, NAMED_COLOR[REBECCAPURPLE])

        obj.prop = "#112233"
        self.assert_property(obj, rgb(0x11, 0x22, 0x33))

        with self.assertRaises(ValueError):
            obj.prop = "a"

        with self.assertRaises(ValueError):
            obj.prop = "b"

        # A Travertino NONE is an explicit string value
        with self.assertRaises(ValueError):
            obj.prop = NONE

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        del obj.prop
        self.assert_property(obj, NAMED_COLOR["goldenrod"])

        # Check the error message
        try:
            obj.prop = "invalid"
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property prop; Valid values are: <color>",
            )

    def test_values(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: str = validated_property(choices=Choices("a", "b", NONE), initial="a")

        obj = MyObject()
        self.assertEqual(obj.prop, "a")

        with self.assertRaises(ValueError):
            obj.prop = 10

        with self.assertRaises(ValueError):
            obj.prop = 3.14159

        with self.assertRaises(ValueError):
            obj.prop = REBECCAPURPLE

        with self.assertRaises(ValueError):
            obj.prop = "#112233"

        obj.prop = NONE
        self.assert_property(obj, NONE)

        obj.prop = "b"
        self.assert_property(obj, "b")

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        del obj.prop
        self.assert_property(obj, "a")

        # Check the error message
        try:
            obj.prop = "invalid"
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property prop; Valid values are: a, b, none",
            )

    def test_multiple_choices(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: str | float = validated_property(
                choices=Choices("a", "b", NONE, number=True, color=True),
                initial=None,
            )

        obj = MyObject()

        obj.prop = 10
        self.assert_property(obj, 10.0)

        obj.prop = 3.14159
        self.assert_property(obj, 3.14159)

        obj.prop = REBECCAPURPLE
        self.assert_property(obj, NAMED_COLOR[REBECCAPURPLE])

        obj.prop = "#112233"
        self.assert_property(obj, rgb(0x11, 0x22, 0x33))

        obj.prop = "a"
        self.assert_property(obj, "a")

        obj.prop = NONE
        self.assert_property(obj, NONE)

        obj.prop = "b"
        self.assert_property(obj, "b")

        # A Python None is invalid
        with self.assertRaises(ValueError):
            obj.prop = None

        # The property can be reset
        # There's no initial value, so the property is None
        del obj.prop
        self.assertIsNone(obj.prop)

        # Check the error message
        try:
            obj.prop = "invalid"
            self.fail("Should raise ValueError")
        except ValueError as v:
            self.assertEqual(
                str(v),
                "Invalid value 'invalid' for property prop; "
                "Valid values are: a, b, none, <number>, <color>",
            )

    def test_string_symbol(self):
        @prep_style_class
        class MyObject(BaseStyle):
            prop: str = validated_property(choices=Choices(TOP, NONE))

        obj = MyObject()

        # Set a symbolic value using the string value of the symbol
        # We can't just use the string directly, though - that would
        # get optimized by the compiler. So we create a string and
        # transform it into the value we want.
        val = "TOP"
        obj.prop = val.lower()

        # Both equality and instance checking should work.
        self.assertEqual(obj.prop, TOP)
        self.assertIs(obj.prop, TOP)
