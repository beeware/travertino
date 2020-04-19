from unittest import TestCase
from unittest.mock import Mock, call

from travertino.declaration import Choices
from travertino.style_decorator import style
from travertino.style_properties import style_property, directional_property

VALUE1 = 'value1'
VALUE2 = 'value2'
VALUE3 = 'value3'
VALUE_CHOICES = Choices(VALUE1, VALUE2, VALUE3, None, integer=True)
DEFAULT_VALUE_CHOICES = Choices(VALUE1, VALUE2, VALUE3, integer=True, default=True)


@style
class Style:
    apply = Mock()

    # Some properties with explicit initial values
    explicit_const = style_property(choices=VALUE_CHOICES, initial=VALUE1)
    explicit_value = style_property(choices=VALUE_CHOICES, initial=0)
    explicit_none = style_property(choices=VALUE_CHOICES, initial=None)

    # A property with an implicit default value.
    # This usually means the default is platform specific.
    implicit = style_property(choices=DEFAULT_VALUE_CHOICES)

    thing_top = style_property(choices=VALUE_CHOICES, initial=0)
    thing_right = style_property(choices=VALUE_CHOICES, initial=0)
    thing_bottom = style_property(choices=VALUE_CHOICES, initial=0)
    thing_left = style_property(choices=VALUE_CHOICES, initial=0)
    thing = directional_property()


class TestNode:
    def __init__(self, style=None):
        if style is None:
            self.style = Style()
        else:
            self.style = style.copy(self)


class DeclarationTests(TestCase):

    def setUp(self):
        Style.apply.reset_mock()

    def test_invalid_style(self):
        with self.assertRaises(ValueError):
            # Define a style that has an invalid initial value on a validated property
            @style
            class BadStyle:
                apply = Mock()
                value = style_property(choices=VALUE_CHOICES, initial='something')

    def test_constructor(self):
        style_obj = Style(explicit_const=VALUE2, implicit=VALUE3)

        self.assertEqual(style_obj.explicit_const, VALUE2)
        self.assertEqual(style_obj.explicit_value, 0)
        self.assertEqual(style_obj.implicit, VALUE3)

    def test_create_and_copy(self):
        style_obj = Style(explicit_const=VALUE2, implicit=VALUE3)

        dup = style_obj.copy()
        self.assertEqual(dup.explicit_const, VALUE2)
        self.assertEqual(dup.explicit_value, 0)
        self.assertEqual(dup.implicit, VALUE3)

    def test_reapply(self):
        node = TestNode(style=Style(explicit_const=VALUE2, implicit=VALUE3))

        node.style.reapply()
        calls = [
            call('explicit_const', VALUE2),
            call('explicit_value', 0),
            call('explicit_none', None),
            call('implicit', VALUE3),
            call('thing_left', 0),
            call('thing_top', 0),
            call('thing_right', 0),
            call('thing_bottom', 0),
        ]
        for a_call in calls:
            node.style.apply.has_call(a_call)

    def test_property_with_explicit_const(self):
        node = TestNode()

        # Default value is VALUE1
        self.assertIs(node.style.explicit_const, VALUE1)
        node.style.apply.assert_not_called()

        # Modify the value
        node.style.explicit_const = 10

        self.assertEqual(node.style.explicit_const, 10)
        node.style.apply.assert_called_once_with('explicit_const', 10)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set the value to the same value.
        # No dirty notification is sent
        node.style.explicit_const = 10
        self.assertEqual(node.style.explicit_const, 10)
        node.style.apply.assert_not_called()

        # Set the value to something new
        # A dirty notification is set.
        node.style.explicit_const = 20
        self.assertEqual(node.style.explicit_const, 20)
        node.style.apply.assert_called_once_with('explicit_const', 20)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear the property
        del node.style.explicit_const
        self.assertIs(node.style.explicit_const, VALUE1)
        node.style.apply.assert_called_once_with('explicit_const', VALUE1)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear the property again.
        # The underlying attribute won't exist, so this
        # should be a no-op.
        del node.style.explicit_const
        self.assertIs(node.style.explicit_const, VALUE1)
        node.style.apply.assert_not_called()

    def test_property_with_explicit_value(self):
        node = TestNode()

        # Default value is 0
        self.assertEqual(node.style.explicit_value, 0)
        node.style.apply.assert_not_called()

        # Modify the value
        node.style.explicit_value = 10

        self.assertEqual(node.style.explicit_value, 10)
        node.style.apply.assert_called_once_with('explicit_value', 10)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set the value to the same value.
        # No dirty notification is sent
        node.style.explicit_value = 10
        self.assertEqual(node.style.explicit_value, 10)
        node.style.apply.assert_not_called()

        # Set the value to something new
        # A dirty notification is set.
        node.style.explicit_value = 20
        self.assertEqual(node.style.explicit_value, 20)
        node.style.apply.assert_called_once_with('explicit_value', 20)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear the property
        del node.style.explicit_value
        self.assertEqual(node.style.explicit_value, 0)
        node.style.apply.assert_called_once_with('explicit_value', 0)

    def test_property_with_explicit_none(self):
        node = TestNode()

        # Default value is None
        self.assertIsNone(node.style.explicit_none)
        node.style.apply.assert_not_called()

        # Modify the value
        node.style.explicit_none = 10

        self.assertEqual(node.style.explicit_none, 10)
        node.style.apply.assert_called_once_with('explicit_none', 10)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set the property to the same value.
        # No dirty notification is sent
        node.style.explicit_none = 10
        self.assertEqual(node.style.explicit_none, 10)
        node.style.apply.assert_not_called()

        # Set the property to something new
        # A dirty notification is set.
        node.style.explicit_none = 20
        self.assertEqual(node.style.explicit_none, 20)
        node.style.apply.assert_called_once_with('explicit_none', 20)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear the property
        del node.style.explicit_none
        self.assertIsNone(node.style.explicit_none)
        node.style.apply.assert_called_once_with('explicit_none', None)

    def test_property_with_implicit_default(self):
        node = TestNode()

        # Default value is None
        self.assertIsNone(node.style.implicit)
        node.style.apply.assert_not_called()

        # Modify the value
        node.style.implicit = 10

        self.assertEqual(node.style.implicit, 10)
        node.style.apply.assert_called_once_with('implicit', 10)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set the value to the same value.
        # No dirty notification is sent
        node.style.implicit = 10
        self.assertEqual(node.style.implicit, 10)
        node.style.apply.assert_not_called()

        # Set the value to something new
        # A dirty notification is set.
        node.style.implicit = 20
        self.assertEqual(node.style.implicit, 20)
        node.style.apply.assert_called_once_with('implicit', 20)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear the property
        del node.style.implicit
        self.assertIsNone(node.style.implicit)
        node.style.apply.assert_called_once_with('implicit', None)

    def test_directional_property(self):
        node = TestNode()

        # Default value is 0
        self.assertEqual(node.style.thing, (0, 0, 0, 0))
        self.assertEqual(node.style.thing_top, 0)
        self.assertEqual(node.style.thing_right, 0)
        self.assertEqual(node.style.thing_bottom, 0)
        self.assertEqual(node.style.thing_left, 0)
        node.style.apply.assert_not_called()

        # Set a value in one axis
        node.style.thing_top = 10

        self.assertEqual(node.style.thing, (10, 0, 0, 0))
        self.assertEqual(node.style.thing_top, 10)
        self.assertEqual(node.style.thing_right, 0)
        self.assertEqual(node.style.thing_bottom, 0)
        self.assertEqual(node.style.thing_left, 0)
        node.style.apply.assert_called_once_with('thing_top', 10)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set a value directly with a single item
        node.style.thing = (10,)

        self.assertEqual(node.style.thing, (10, 10, 10, 10))
        self.assertEqual(node.style.thing_top, 10)
        self.assertEqual(node.style.thing_right, 10)
        self.assertEqual(node.style.thing_bottom, 10)
        self.assertEqual(node.style.thing_left, 10)
        node.style.apply.assert_has_calls([
            call('thing_right', 10),
            call('thing_bottom', 10),
            call('thing_left', 10),
        ])

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set a value directly with a single item
        node.style.thing = 30

        self.assertEqual(node.style.thing, (30, 30, 30, 30))
        self.assertEqual(node.style.thing_top, 30)
        self.assertEqual(node.style.thing_right, 30)
        self.assertEqual(node.style.thing_bottom, 30)
        self.assertEqual(node.style.thing_left, 30)
        node.style.apply.assert_has_calls([
            call('thing_top', 30),
            call('thing_right', 30),
            call('thing_bottom', 30),
            call('thing_left', 30),
        ])

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set a value directly with a 2 values
        node.style.thing = (10, 20)

        self.assertEqual(node.style.thing, (10, 20, 10, 20))
        self.assertEqual(node.style.thing_top, 10)
        self.assertEqual(node.style.thing_right, 20)
        self.assertEqual(node.style.thing_bottom, 10)
        self.assertEqual(node.style.thing_left, 20)
        node.style.apply.assert_has_calls([
            call('thing_top', 10),
            call('thing_right', 20),
            call('thing_bottom', 10),
            call('thing_left', 20),
        ])

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set a value directly with a 3 values
        node.style.thing = (10, 20, 30)

        self.assertEqual(node.style.thing, (10, 20, 30, 20))
        self.assertEqual(node.style.thing_top, 10)
        self.assertEqual(node.style.thing_right, 20)
        self.assertEqual(node.style.thing_bottom, 30)
        self.assertEqual(node.style.thing_left, 20)
        node.style.apply.assert_called_once_with('thing_bottom', 30)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Set a value directly with a 4 values
        node.style.thing = (10, 20, 30, 40)

        self.assertEqual(node.style.thing, (10, 20, 30, 40))
        self.assertEqual(node.style.thing_top, 10)
        self.assertEqual(node.style.thing_right, 20)
        self.assertEqual(node.style.thing_bottom, 30)
        self.assertEqual(node.style.thing_left, 40)
        node.style.apply.assert_called_once_with('thing_left', 40)

        # Set a value directly with an invalid number of values
        with self.assertRaises(ValueError):
            node.style.thing = ()

        with self.assertRaises(ValueError):
            node.style.thing = (10, 20, 30, 40, 50)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear a value on one axis
        del node.style.thing_top

        self.assertEqual(node.style.thing, (0, 20, 30, 40))
        self.assertEqual(node.style.thing_top, 0)
        self.assertEqual(node.style.thing_right, 20)
        self.assertEqual(node.style.thing_bottom, 30)
        self.assertEqual(node.style.thing_left, 40)
        node.style.apply.assert_called_once_with('thing_top', 0)

        # Restore the top thing
        node.style.thing_top = 10

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Clear a value directly
        del node.style.thing

        self.assertEqual(node.style.thing, (0, 0, 0, 0))
        self.assertEqual(node.style.thing_top, 0)
        self.assertEqual(node.style.thing_right, 0)
        self.assertEqual(node.style.thing_bottom, 0)
        self.assertEqual(node.style.thing_left, 0)
        node.style.apply.assert_has_calls([
            call('thing_right', 0),
            call('thing_bottom', 0),
            call('thing_left', 0),
        ])

    def test_set_multiple_properties(self):
        node = TestNode()

        # Set a pair of properties
        node.style.update(explicit_value=20, explicit_none=10)

        self.assertIs(node.style.explicit_const, VALUE1)
        self.assertEqual(node.style.explicit_none, 10)
        self.assertEqual(node.style.explicit_value, 20)
        node.style.apply.assert_has_calls([
                call('explicit_value', 20),
                call('explicit_none', 10),
            ], any_order=True)

        # Set a different pair of properties
        node.style.update(explicit_const=VALUE2, explicit_value=30)

        self.assertIs(node.style.explicit_const, VALUE2)
        self.assertEqual(node.style.explicit_value, 30)
        self.assertEqual(node.style.explicit_none, 10)
        node.style.apply.assert_has_calls([
                call('explicit_const', VALUE2),
                call('explicit_value', 30),
            ], any_order=True)

        # Clear the applicator mock
        node.style.apply.reset_mock()

        # Setting a non-property
        with self.assertRaises(NameError):
            node.style.update(not_a_property=10)

        node.style.apply.assert_not_called()

    def test_str(self):
        node = TestNode()

        node.style.update(
            explicit_const=VALUE2,
            explicit_value=20,
            thing=(30, 40, 50, 60),
        )

        self.assertEqual(
            str(node.style),
            "explicit-const: value2; "
            "explicit-value: 20; "
            "explicit-none: None; "
            "implicit: None; "
            "thing-top: 30; "
            "thing-right: 40; "
            "thing-bottom: 50; "
            "thing-left: 60"
        )

    def test_dict(self):
        "Style declarations expose a dict-like interface"
        node = TestNode()

        node.style.update(
            explicit_const=VALUE2,
            explicit_value=20,
            thing=(30, 40, 50, 60),
        )

        self.assertEqual(
            node.style.keys(),
            {
                'explicit_const',
                'explicit_none',
                'explicit_value',
                'implicit',
                'thing_bottom',
                'thing_left',
                'thing_right',
                'thing_top'
            }
        )
        self.assertEqual(
            sorted(node.style.items()),
            sorted([
                ('explicit_const', 'value2'),
                ('explicit_none', None),
                ('explicit_value', 20),
                ('implicit', None),
                ('thing_bottom', 50),
                ('thing_left', 60),
                ('thing_right', 40),
                ('thing_top', 30),
            ])
        )

        # A property can be set, retrieved and cleared using the attribute name
        node.style['thing-bottom'] = 10
        self.assertEqual(node.style['thing-bottom'], 10)
        del node.style['thing-bottom']
        self.assertEqual(node.style['thing-bottom'], 0)

        # A property can be set, retrieved and cleared using the Python attribute name
        node.style['thing_bottom'] = 10
        self.assertEqual(node.style['thing_bottom'], 10)
        del node.style['thing_bottom']
        self.assertEqual(node.style['thing_bottom'], 0)

        # Clearing a valid property isn't an error
        del node.style['thing_bottom']
        self.assertEqual(node.style['thing_bottom'], 0)

        # Non-existent properties raise KeyError
        with self.assertRaises(KeyError):
            node.style['no-such-property'] = 'no-such-value'

        with self.assertRaises(KeyError):
            node.style['no-such-property']

        with self.assertRaises(KeyError):
            del node.style['no-such-property']
