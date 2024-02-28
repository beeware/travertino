from __future__ import annotations

import sys
from dataclasses import dataclass
from unittest.mock import Mock

import pytest

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


def test_none():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: str = validated_property(
            choices=Choices(NONE, REBECCAPURPLE), initial=NONE
        )

    obj = MyObject()
    assert obj.prop == NONE

    with pytest.raises(ValueError):
        obj.prop = 10

    with pytest.raises(ValueError):
        obj.prop = 3.14159

    with pytest.raises(ValueError):
        obj.prop = "#112233"

    with pytest.raises(ValueError):
        obj.prop = "a"

    with pytest.raises(ValueError):
        obj.prop = "b"

    # Set the property to a different explicit value
    obj.prop = REBECCAPURPLE
    assert obj.prop == REBECCAPURPLE

    # A Travertino NONE is an explicit value
    obj.prop = NONE
    assert obj.prop == NONE

    # Set the property to a different explicit value
    obj.prop = REBECCAPURPLE
    assert obj.prop == REBECCAPURPLE

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    del obj.prop
    assert obj.prop == NONE

    with pytest.raises(
        ValueError,
        match=r"Invalid value 'invalid' for property prop; Valid values are: "
        r"none, rebeccapurple",
    ):
        obj.prop = "invalid"


def test_allow_string():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: str = validated_property(choices=Choices(string=True), initial="start")

    obj = MyObject()
    assert obj.prop == "start"

    with pytest.raises(ValueError):
        obj.prop = 10

    with pytest.raises(ValueError):
        obj.prop = 3.14159

    obj.prop = REBECCAPURPLE
    assert obj.prop == "rebeccapurple"

    obj.prop = "#112233"
    assert obj.prop == "#112233"

    obj.prop = "a"
    assert obj.prop == "a"

    obj.prop = "b"
    assert obj.prop == "b"

    # A Travertino NONE is an explicit string value
    obj.prop = NONE
    assert obj.prop == NONE

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    del obj.prop
    assert obj.prop == "start"

    with pytest.raises(
        ValueError,
        match=r"Invalid value 99 for property prop; Valid values are: <string>",
    ):
        obj.prop = 99


def test_allow_integer():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: int = validated_property(choices=Choices(integer=True), initial=0)

    obj = MyObject()
    assert obj.prop == 0

    obj.prop = 10
    assert obj.prop == 10

    # This is an odd case; Python happily rounds floats to integers.
    # It's more trouble than it's worth to correct this.
    obj.prop = 3.14159
    assert obj.prop == 3

    with pytest.raises(ValueError):
        obj.prop = REBECCAPURPLE

    with pytest.raises(ValueError):
        obj.prop = "#112233"

    with pytest.raises(ValueError):
        obj.prop = "a"

    with pytest.raises(ValueError):
        obj.prop = "b"

    # A Travertino NONE is an explicit string value
    with pytest.raises(ValueError):
        obj.prop = NONE

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    del obj.prop
    assert obj.prop == 0

    # Check the error message
    with pytest.raises(
        ValueError,
        match=r"Invalid value 'invalid' for property prop; Valid values are: <integer>",
    ):
        obj.prop = "invalid"


def test_allow_number():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: float = validated_property(choices=Choices(number=True), initial=0)

    obj = MyObject()
    assert obj.prop == 0

    obj.prop = 10
    assert obj.prop == 10.0

    obj.prop = 3.14159
    assert obj.prop == 3.14159

    with pytest.raises(ValueError):
        obj.prop = REBECCAPURPLE

    with pytest.raises(ValueError):
        obj.prop = "#112233"

    with pytest.raises(ValueError):
        obj.prop = "a"

    with pytest.raises(ValueError):
        obj.prop = "b"

    # A Travertino NONE is an explicit string value
    with pytest.raises(ValueError):
        obj.prop = NONE

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    del obj.prop
    assert obj.prop == 0

    with pytest.raises(
        ValueError,
        match=r"Invalid value 'invalid' for property prop; Valid values are: <number>",
    ):
        obj.prop = "invalid"


def test_allow_color():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: str = validated_property(choices=Choices(color=True), initial="goldenrod")

    obj = MyObject()
    assert obj.prop == NAMED_COLOR[GOLDENROD]

    with pytest.raises(ValueError):
        obj.prop = 10

    with pytest.raises(ValueError):
        obj.prop = 3.14159

    obj.prop = REBECCAPURPLE
    assert obj.prop == NAMED_COLOR[REBECCAPURPLE]

    obj.prop = "#112233"
    assert obj.prop == rgb(0x11, 0x22, 0x33)

    with pytest.raises(ValueError):
        obj.prop = "a"

    with pytest.raises(ValueError):
        obj.prop = "b"

    # A Travertino NONE is an explicit string value
    with pytest.raises(ValueError):
        obj.prop = NONE

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    del obj.prop
    assert obj.prop == NAMED_COLOR["goldenrod"]

    with pytest.raises(
        ValueError,
        match=r"Invalid value 'invalid' for property prop; Valid values are: <color>",
    ):
        obj.prop = "invalid"


def test_values():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: str = validated_property(choices=Choices("a", "b", NONE), initial="a")

    obj = MyObject()
    assert obj.prop == "a"

    with pytest.raises(ValueError):
        obj.prop = 10

    with pytest.raises(ValueError):
        obj.prop = 3.14159

    with pytest.raises(ValueError):
        obj.prop = REBECCAPURPLE

    with pytest.raises(ValueError):
        obj.prop = "#112233"

    obj.prop = NONE
    assert obj.prop == NONE

    obj.prop = "b"
    assert obj.prop == "b"

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    del obj.prop
    assert obj.prop == "a"

    with pytest.raises(
        ValueError,
        match=r"Invalid value 'invalid' for property prop; Valid values are: a, b, none",
    ):
        obj.prop = "invalid"


def test_multiple_choices():
    @prep_style_class
    class MyObject(BaseStyle):
        prop: str | float = validated_property(
            choices=Choices("a", "b", NONE, number=True, color=True),
            initial=None,
        )

    obj = MyObject()

    obj.prop = 10
    assert obj.prop == 10.0

    obj.prop = 3.14159
    assert obj.prop == 3.14159

    obj.prop = REBECCAPURPLE
    assert obj.prop == NAMED_COLOR[REBECCAPURPLE]

    obj.prop = "#112233"
    assert obj.prop == rgb(0x11, 0x22, 0x33)

    obj.prop = "a"
    assert obj.prop == "a"

    obj.prop = NONE
    assert obj.prop == NONE

    obj.prop = "b"
    assert obj.prop == "b"

    # A Python None is invalid
    with pytest.raises(ValueError):
        obj.prop = None

    # The property can be reset
    # There's no initial value, so the property is None
    del obj.prop
    assert obj.prop is None

    # Check the error message
    with pytest.raises(
        ValueError,
        match=r"Invalid value 'invalid' for property prop; Valid values are: "
        r"a, b, none, <number>, <color>",
    ):
        obj.prop = "invalid"


def test_string_symbol():
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
    assert obj.prop == TOP
    assert obj.prop is TOP
