import pytest

from tests.utils import prep_style_class
from travertino.constants import (
    BOLD,
    CURSIVE,
    FANTASY,
    ITALIC,
    MESSAGE,
    MONOSPACE,
    NORMAL,
    SANS_SERIF,
    SERIF,
    SMALL_CAPS,
    SYSTEM,
)
from travertino.declaration import (
    BaseStyle,
    Choices,
    composite_property,
    list_property,
    validated_property,
)

SYSTEM_DEFAULT_FONTS = {SYSTEM, MESSAGE, SERIF, SANS_SERIF, CURSIVE, FANTASY, MONOSPACE}


def _parse_font_str(font_str: str) -> tuple:
    """Parse a string into values for the font property alias"""
    split = font_str.split()

    for index, part in enumerate(split):
        try:
            Style.font_size.validate(part)
            break
        except ValueError:
            pass
    else:
        # No break; no size was found.
        raise ValueError(f"Invalid font string: {font_str}")

    # Size is the "delimiter". As long as we found it, we know everything after it is
    # the setting for font familes.
    optional, size, families = split[:index], part, split[index + 1 :]

    # Add back the spaces previously removed, then parse the whole string.
    families = " ".join(families)
    try:
        families = _parse_quotes(families)
    except ValueError:
        raise ValueError(f"Invalid string for font families: {families}")
    return (*optional, size, families)


def _parse_quotes(input_str: str) -> list[str]:
    """Break up a comma-delimited string, respecting quotes (and escaped quotes)"""

    def wordify(chars):
        return "".join(chars).strip()

    QUOTES = "'\""
    DELIMITER = ","
    ESCAPE = "\\"

    items = []
    current_item = []
    quote = None
    need_delimiter_next = False

    chars = list(reversed(input_str))
    while chars:
        char = chars.pop()

        if need_delimiter_next:
            if char == DELIMITER:
                need_delimiter_next = False
                continue
            elif char.isspace():
                continue
            else:
                raise ValueError("Content after quotes in item")

        if quote:
            if char == ESCAPE:
                if (escaped_char := chars.pop()) in QUOTES:
                    current_item.append(escaped_char)
                else:
                    raise ValueError("Unrecognized escape sequence")
            elif char == quote:
                quote = None
                items.append(wordify(current_item))
                current_item = []
                need_delimiter_next = True
            else:
                current_item.append(char)

        else:
            if char in QUOTES:
                if current_item and wordify(current_item):
                    raise ValueError("Quote not at beginning of item")
                quote = char
            elif char == DELIMITER:
                items.append(wordify(current_item))
                current_item = []
            else:
                current_item.append(char)

    if current_item:
        items.append(wordify(current_item))

    return items


@prep_style_class
class Style(BaseStyle):
    font_style: str = validated_property(Choices(NORMAL, ITALIC, BOLD), initial=NORMAL)
    font_variant: str = validated_property(Choices(NORMAL, SMALL_CAPS), initial=NORMAL)
    font_weight: str = validated_property(Choices(NORMAL, BOLD), initial=NORMAL)

    font_size: int = validated_property(Choices(integer=True), initial=-1)
    font_family: list[str] = list_property(
        Choices(*SYSTEM_DEFAULT_FONTS, string=True), initial=[SYSTEM]
    )

    font: tuple = composite_property(
        optional=("font_style", "font_variant", "font_weight"),
        required=("font_size", "font_family"),
        parse_str=_parse_font_str,
    )


def assert_font(style, values):
    # Test against retrieving the composite property
    assert style.font == values

    # Also test against the underlying individual properties
    (font_style, font_variant, font_weight, font_size, font_family) = values

    assert style.font_style == font_style
    assert style.font_variant == font_variant
    assert style.font_weight == font_weight
    assert style.font_size == font_size
    assert style.font_family == font_family


def test_default_values():
    assert_font(Style(), (NORMAL, NORMAL, NORMAL, -1, [SYSTEM]))


@pytest.mark.parametrize(
    "value",
    [
        (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", SANS_SERIF]),
        # Should also work with optionals reordered
        (SMALL_CAPS, BOLD, ITALIC, 12, ["Comic Sans", SANS_SERIF]),
        (BOLD, SMALL_CAPS, ITALIC, 12, ["Comic Sans", SANS_SERIF]),
    ],
)
def test_assign_all_non_default(value):
    style = Style()
    style.font = value

    assert_font(style, (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", SANS_SERIF]))


@pytest.mark.parametrize(
    "value",
    [
        # Full assignment, in order and out of order
        (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]),
        (NORMAL, NORMAL, SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
        # Only the non-default
        (SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
        # One NORMAL
        (SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]),
        (NORMAL, SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
    ],
)
def test_assign_one_non_default(value):
    style = Style()
    style.font = value

    assert_font(style, (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]))


@pytest.mark.parametrize(
    "value",
    [
        # Full assignment, in order and out of order
        (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]),
        (NORMAL, NORMAL, SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
        # Only the non-default
        (SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
        # One NORMAL
        (SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]),
        (NORMAL, SMALL_CAPS, 12, ["Comic Sans", SANS_SERIF]),
    ],
)
def test_assign_one_non_default_after_setting(value):
    style = Style()
    style.font_weight = BOLD
    style.font_style = ITALIC

    style.font = value

    assert_font(style, (NORMAL, SMALL_CAPS, NORMAL, 12, ["Comic Sans", SANS_SERIF]))


@pytest.mark.parametrize(
    "value, result",
    [
        (
            "italic small-caps bold 12 Comic Sans, sans-serif",
            (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", SANS_SERIF]),
        ),
        (
            'italic small-caps bold 12 "Comic Sans", sans-serif',
            (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", SANS_SERIF]),
        ),
        (
            # Gotta escape the escape sequence...
            "italic small-caps bold 12 \"Comic Sans\", 'George\\'s Font', sans-serif",
            (ITALIC, SMALL_CAPS, BOLD, 12, ["Comic Sans", "George's Font", SANS_SERIF]),
        ),
    ],
)
def test_string_parsing(value, result):
    style = Style()
    style.font = value

    assert_font(style, result)
