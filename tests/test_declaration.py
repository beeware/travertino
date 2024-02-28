from __future__ import annotations

from unittest.mock import call

import pytest

from tests.test_choices import prep_style_class
from travertino.declaration import (
    BaseStyle,
    Choices,
    directional_property,
    validated_property,
)

VALUE1 = "value1"
VALUE2 = "value2"
VALUE3 = "value3"
VALUE_CHOICES = Choices(VALUE1, VALUE2, VALUE3, None, integer=True)
DEFAULT_VALUE_CHOICES = Choices(VALUE1, VALUE2, VALUE3, integer=True, default=True)


@prep_style_class
class Style(BaseStyle):
    # Some properties with explicit initial values
    explicit_const: str | int = validated_property(
        choices=VALUE_CHOICES, initial=VALUE1
    )
    explicit_value: str | int = validated_property(choices=VALUE_CHOICES, initial=0)
    explicit_none: str | int | None = validated_property(
        choices=VALUE_CHOICES, initial=None
    )

    # A property with an implicit default value.
    # This usually means the default is platform specific.
    implicit: str | int | None = validated_property(choices=DEFAULT_VALUE_CHOICES)

    # A set of directional properties
    thing: str | int = directional_property("thing{}", choices=VALUE_CHOICES, initial=0)
    thing_top: str | int
    thing_right: str | int
    thing_bottom: str | int
    thing_left: str | int


class ExampleNode:
    def __init__(self, style=None):
        if style is None:
            self.style = Style()
        else:
            self.style = style.copy(self)


def test_invalid_style():
    with pytest.raises(ValueError):
        # Define a style that has an invalid initial value on a validated property
        class BadStyle(BaseStyle):
            value = validated_property(choices=VALUE_CHOICES, initial="something")


def test_create_and_copy():
    style = Style(explicit_const=VALUE2, implicit=VALUE3)

    dup = style.copy()
    assert dup.explicit_const == VALUE2
    assert dup.explicit_value == 0
    assert dup.implicit == VALUE3


def test_reapply():
    node = ExampleNode(style=Style(explicit_const=VALUE2, implicit=VALUE3))

    node.style.reapply()
    node.style.apply.assert_has_calls(
        [
            call("explicit_const", VALUE2),
            call("explicit_value", 0),
            call("explicit_none", None),
            call("implicit", VALUE3),
            call("thing_left", 0),
            call("thing_top", 0),
            call("thing_right", 0),
            call("thing_bottom", 0),
        ],
        any_order=True,
    )


def test_property_with_explicit_const():
    node = ExampleNode()

    # Default value is VALUE1
    assert node.style.explicit_const is VALUE1
    node.style.apply.assert_not_called()

    # Modify the value
    node.style.explicit_const = 10

    assert node.style.explicit_const == 10
    node.style.apply.assert_called_once_with("explicit_const", 10)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    node.style.explicit_const = 10
    assert node.style.explicit_const == 10
    node.style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    node.style.explicit_const = 20
    assert node.style.explicit_const == 20
    node.style.apply.assert_called_once_with("explicit_const", 20)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear the property
    del node.style.explicit_const
    assert node.style.explicit_const is VALUE1
    node.style.apply.assert_called_once_with("explicit_const", VALUE1)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear the property again.
    # The underlying attribute won't exist, so this
    # should be a no-op.
    del node.style.explicit_const
    assert node.style.explicit_const is VALUE1
    node.style.apply.assert_not_called()


def test_property_with_explicit_value():
    node = ExampleNode()

    # Default value is 0
    assert node.style.explicit_value == 0
    node.style.apply.assert_not_called()

    # Modify the value
    node.style.explicit_value = 10

    assert node.style.explicit_value == 10
    node.style.apply.assert_called_once_with("explicit_value", 10)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    node.style.explicit_value = 10
    assert node.style.explicit_value == 10
    node.style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    node.style.explicit_value = 20
    assert node.style.explicit_value == 20
    node.style.apply.assert_called_once_with("explicit_value", 20)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear the property
    del node.style.explicit_value
    assert node.style.explicit_value == 0
    node.style.apply.assert_called_once_with("explicit_value", 0)


def test_property_with_explicit_none():
    node = ExampleNode()

    # Default value is None
    assert node.style.explicit_none is None
    node.style.apply.assert_not_called()

    # Modify the value
    node.style.explicit_none = 10

    assert node.style.explicit_none == 10
    node.style.apply.assert_called_once_with("explicit_none", 10)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set the property to the same value.
    # No dirty notification is sent
    node.style.explicit_none = 10
    assert node.style.explicit_none == 10
    node.style.apply.assert_not_called()

    # Set the property to something new
    # A dirty notification is set.
    node.style.explicit_none = 20
    assert node.style.explicit_none == 20
    node.style.apply.assert_called_once_with("explicit_none", 20)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear the property
    del node.style.explicit_none
    assert node.style.explicit_none is None
    node.style.apply.assert_called_once_with("explicit_none", None)


def test_property_with_implicit_default():
    node = ExampleNode()

    # Default value is None
    assert node.style.implicit is None
    node.style.apply.assert_not_called()

    # Modify the value
    node.style.implicit = 10

    assert node.style.implicit == 10
    node.style.apply.assert_called_once_with("implicit", 10)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set the value to the same value.
    # No dirty notification is sent
    node.style.implicit = 10
    assert node.style.implicit == 10
    node.style.apply.assert_not_called()

    # Set the value to something new
    # A dirty notification is set.
    node.style.implicit = 20
    assert node.style.implicit == 20
    node.style.apply.assert_called_once_with("implicit", 20)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear the property
    del node.style.implicit
    assert node.style.implicit is None
    node.style.apply.assert_called_once_with("implicit", None)


def test_directional_property():
    node = ExampleNode()

    # Default value is 0
    assert node.style.thing == (0, 0, 0, 0)
    assert node.style.thing_top == 0
    assert node.style.thing_right == 0
    assert node.style.thing_bottom == 0
    assert node.style.thing_left == 0
    node.style.apply.assert_not_called()

    # Set a value in one axis
    node.style.thing_top = 10

    assert node.style.thing == (10, 0, 0, 0)
    assert node.style.thing_top == 10
    assert node.style.thing_right == 0
    assert node.style.thing_bottom == 0
    assert node.style.thing_left == 0
    node.style.apply.assert_called_once_with("thing_top", 10)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set a value directly with a single item
    node.style.thing = (10,)

    assert node.style.thing == (10, 10, 10, 10)
    assert node.style.thing_top == 10
    assert node.style.thing_right == 10
    assert node.style.thing_bottom == 10
    assert node.style.thing_left == 10
    node.style.apply.assert_has_calls(
        [
            call("thing_right", 10),
            call("thing_bottom", 10),
            call("thing_left", 10),
        ]
    )

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set a value directly with a single item
    node.style.thing = 30

    assert node.style.thing == (30, 30, 30, 30)
    assert node.style.thing_top == 30
    assert node.style.thing_right == 30
    assert node.style.thing_bottom == 30
    assert node.style.thing_left == 30
    node.style.apply.assert_has_calls(
        [
            call("thing_top", 30),
            call("thing_right", 30),
            call("thing_bottom", 30),
            call("thing_left", 30),
        ]
    )

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set a value directly with a 2 values
    node.style.thing = (10, 20)

    assert node.style.thing == (10, 20, 10, 20)
    assert node.style.thing_top == 10
    assert node.style.thing_right == 20
    assert node.style.thing_bottom == 10
    assert node.style.thing_left == 20
    node.style.apply.assert_has_calls(
        [
            call("thing_top", 10),
            call("thing_right", 20),
            call("thing_bottom", 10),
            call("thing_left", 20),
        ]
    )

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set a value directly with a 3 values
    node.style.thing = (10, 20, 30)

    assert node.style.thing == (10, 20, 30, 20)
    assert node.style.thing_top == 10
    assert node.style.thing_right == 20
    assert node.style.thing_bottom == 30
    assert node.style.thing_left == 20
    node.style.apply.assert_called_once_with("thing_bottom", 30)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Set a value directly with a 4 values
    node.style.thing = (10, 20, 30, 40)

    assert node.style.thing == (10, 20, 30, 40)
    assert node.style.thing_top == 10
    assert node.style.thing_right == 20
    assert node.style.thing_bottom == 30
    assert node.style.thing_left == 40
    node.style.apply.assert_called_once_with("thing_left", 40)

    # Set a value directly with an invalid number of values
    with pytest.raises(ValueError):
        node.style.thing = ()

    with pytest.raises(ValueError):
        node.style.thing = (10, 20, 30, 40, 50)

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear a value on one axis
    del node.style.thing_top

    assert node.style.thing == (0, 20, 30, 40)
    assert node.style.thing_top == 0
    assert node.style.thing_right == 20
    assert node.style.thing_bottom == 30
    assert node.style.thing_left == 40
    node.style.apply.assert_called_once_with("thing_top", 0)

    # Restore the top thing
    node.style.thing_top = 10

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Clear a value directly
    del node.style.thing

    assert node.style.thing == (0, 0, 0, 0)
    assert node.style.thing_top == 0
    assert node.style.thing_right == 0
    assert node.style.thing_bottom == 0
    assert node.style.thing_left == 0
    node.style.apply.assert_has_calls(
        [
            call("thing_right", 0),
            call("thing_bottom", 0),
            call("thing_left", 0),
        ]
    )


def test_set_multiple_properties():
    node = ExampleNode()

    # Set a pair of properties
    node.style.update(explicit_value=20, explicit_none=10)

    assert node.style.explicit_const is VALUE1
    assert node.style.explicit_none == 10
    assert node.style.explicit_value == 20
    node.style.apply.assert_has_calls(
        [
            call("explicit_value", 20),
            call("explicit_none", 10),
        ],
        any_order=True,
    )

    # Set a different pair of properties
    node.style.update(explicit_const=VALUE2, explicit_value=30)

    assert node.style.explicit_const is VALUE2
    assert node.style.explicit_value == 30
    assert node.style.explicit_none == 10
    node.style.apply.assert_has_calls(
        [
            call("explicit_const", VALUE2),
            call("explicit_value", 30),
        ],
        any_order=True,
    )

    # Clear the applicator mock
    node.style.apply.reset_mock()

    # Setting a non-property
    with pytest.raises(NameError):
        node.style.update(not_a_property=10)

    node.style.apply.assert_not_called()


def test_str():
    node = ExampleNode()

    node.style.update(
        explicit_const=VALUE2,
        explicit_value=20,
        thing=(30, 40, 50, 60),
    )

    assert (
        str(node.style) == "explicit-const: value2; "
        "explicit-value: 20; "
        "thing-bottom: 50; "
        "thing-left: 60; "
        "thing-right: 40; "
        "thing-top: 30"
    )


def test_dict():
    "Style declarations expose a dict-like interface"
    node = ExampleNode()

    node.style.update(
        explicit_const=VALUE2,
        explicit_value=20,
        thing=(30, 40, 50, 60),
    )

    assert node.style.keys() == {
        "explicit_const",
        "explicit_value",
        "thing_bottom",
        "thing_left",
        "thing_right",
        "thing_top",
    }
    assert sorted(node.style.items()) == sorted(
        [
            ("explicit_const", "value2"),
            ("explicit_value", 20),
            ("thing_bottom", 50),
            ("thing_left", 60),
            ("thing_right", 40),
            ("thing_top", 30),
        ]
    )

    # A property can be set, retrieved and cleared using the attribute name
    node.style["thing-bottom"] = 10
    assert node.style["thing-bottom"] == 10
    del node.style["thing-bottom"]
    assert node.style["thing-bottom"] == 0

    # A property can be set, retrieved and cleared using the Python attribute name
    node.style["thing_bottom"] = 10
    assert node.style["thing_bottom"] == 10
    del node.style["thing_bottom"]
    assert node.style["thing_bottom"] == 0

    # Clearing a valid property isn't an error
    del node.style["thing_bottom"]
    assert node.style["thing_bottom"] == 0

    # Non-existent properties raise KeyError
    with pytest.raises(KeyError):
        node.style["no-such-property"] = "no-such-value"

    with pytest.raises(KeyError):
        node.style["no-such-property"]

    with pytest.raises(KeyError):
        del node.style["no-such-property"]
