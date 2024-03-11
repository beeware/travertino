import pytest

from travertino.constants import (
    BOLD,
    ITALIC,
    NORMAL,
    OBLIQUE,
    SMALL_CAPS,
    SYSTEM_DEFAULT_FONT_SIZE,
)
from travertino.fonts import Font, font


def assert_font(font, family, size, style, variant, weight):
    assert font.family == family
    assert font.size == size
    assert font.style == style
    assert font.variant == variant
    assert font.weight == weight


def test_equality():
    assert Font("Comic Sans", "12 pt") == Font("Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_hash():
    assert hash(Font("Comic Sans", 12)) == hash(Font("Comic Sans", 12))

    assert hash(Font("Comic Sans", 12, weight=BOLD)) != hash(Font("Comic Sans", 12))


@pytest.mark.parametrize(
    "size, kwargs, string",
    [
        (12, {}, "12pt"),
        (12, {"style": ITALIC}, "italic 12pt"),
        (12, {"style": ITALIC, "variant": SMALL_CAPS}, "italic small-caps 12pt"),
        (
            12,
            {"style": ITALIC, "variant": SMALL_CAPS, "weight": BOLD},
            "italic small-caps bold 12pt",
        ),
        (12, {"variant": SMALL_CAPS, "weight": BOLD}, "small-caps bold 12pt"),
        (12, {"weight": BOLD}, "bold 12pt"),
        (12, {"style": ITALIC, "weight": BOLD}, "italic bold 12pt"),
        # Check system default size handling
        (SYSTEM_DEFAULT_FONT_SIZE, {}, "system default size"),
        (SYSTEM_DEFAULT_FONT_SIZE, {"style": ITALIC}, "italic system default size"),
    ],
)
def test_repr(size, kwargs, string):
    assert repr(Font("Comic Sans", size, **kwargs)) == f"<Font: {string} Comic Sans>"


@pytest.mark.parametrize("size", [12, "12", "12pt", "12 pt"])
def test_simple_construction(size):
    assert_font(Font("Comic Sans", size), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_invalid_construction():
    with pytest.raises(ValueError):
        Font("Comic Sans", "12 quatloos")


@pytest.mark.parametrize(
    "family",
    [
        "Comics Sans",
        "Wingdings",
        "'Comic Sans'",
        '"Comic Sans"',
    ],
)
def test_family(family):
    normalized_family = family.replace("'", "").replace('"', "")
    assert_font(Font(family, 12), normalized_family, 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "style, result_style",
    [
        (ITALIC, ITALIC),
        ("italic", ITALIC),
        (OBLIQUE, OBLIQUE),
        ("oblique", OBLIQUE),
        ("something else", NORMAL),
    ],
)
def test_style(style, result_style):
    assert_font(
        Font("Comic Sans", 12, style=style),
        "Comic Sans",
        12,
        result_style,
        NORMAL,
        NORMAL,
    )


@pytest.mark.parametrize(
    "kwargs",
    [
        {},
        {"style": ITALIC},
    ],
)
def test_make_normal_style(kwargs):
    f = Font("Comic Sans", 12, **kwargs)
    assert_font(f.normal_style(), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "method, result",
    [
        ("italic", ITALIC),
        ("oblique", OBLIQUE),
    ],
)
def test_make_slanted(method, result):
    f = Font("Comic Sans", 12)
    assert_font(getattr(f, method)(), "Comic Sans", 12, result, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "variant, result",
    [
        (SMALL_CAPS, SMALL_CAPS),
        ("small-caps", SMALL_CAPS),
        ("something else", NORMAL),
    ],
)
def test_variant(variant, result):
    assert_font(
        Font("Comic Sans", 12, variant=variant),
        "Comic Sans",
        12,
        NORMAL,
        result,
        NORMAL,
    )


@pytest.mark.parametrize("kwargs", [{}, {"variant": SMALL_CAPS}])
def test_make_normal_variant(kwargs):
    f = Font("Comic Sans", 12, **kwargs)
    assert_font(f.normal_variant(), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_make_small_caps():
    f = Font("Comic Sans", 12)
    assert_font(f.small_caps(), "Comic Sans", 12, NORMAL, SMALL_CAPS, NORMAL)


@pytest.mark.parametrize(
    "weight, result",
    [
        (BOLD, BOLD),
        ("bold", BOLD),
        ("something else", NORMAL),
    ],
)
def test_weight(weight, result):
    assert_font(
        Font("Comic Sans", 12, weight=weight),
        "Comic Sans",
        12,
        NORMAL,
        NORMAL,
        result,
    )


@pytest.mark.parametrize("kwargs", [{}, {"weight": BOLD}])
def test_make_normal_weight(kwargs):
    f = Font("Comic Sans", 12, **kwargs)
    assert_font(f.normal_weight(), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_make_bold():
    f = Font("Comic Sans", 12)
    assert_font(f.bold(), "Comic Sans", 12, NORMAL, NORMAL, BOLD)


###############
# Parsing fonts
###############


def test_parse_font_instance():
    f = Font("Comic Sans", 12)

    parsed = font(f)

    assert f == parsed
    assert f is parsed


@pytest.mark.parametrize(
    "string, style, variant, weight",
    [
        ("12pt Comic Sans", NORMAL, NORMAL, NORMAL),
        ("italic 12pt Comic Sans", ITALIC, NORMAL, NORMAL),
        ("italic small-caps 12pt Comic Sans", ITALIC, SMALL_CAPS, NORMAL),
        ("italic small-caps bold 12pt Comic Sans", ITALIC, SMALL_CAPS, BOLD),
        ("small-caps bold 12pt Comic Sans", NORMAL, SMALL_CAPS, BOLD),
        ("italic bold 12 pt Comic Sans", ITALIC, NORMAL, BOLD),
        ("bold 12 pt Comic Sans", NORMAL, NORMAL, BOLD),
    ],
)
def test_parse_successful_combinations(string, style, variant, weight):
    assert_font(font(string), "Comic Sans", 12, style, variant, weight)


@pytest.mark.parametrize(
    "string",
    ["12pt Comic Sans", "12 pt Comic Sans", "12 Comic Sans"],
)
def test_parse_font_sizes(string):
    assert_font(font(string), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


def test_parse_invalid_size():
    with pytest.raises(ValueError):
        font("12quatloo Comic Sans")


@pytest.mark.parametrize("string", ["12pt 'Comic Sans'", '12pt "Comic Sans"'])
def test_parse_font_family(string):
    assert_font(font(string), "Comic Sans", 12, NORMAL, NORMAL, NORMAL)


@pytest.mark.parametrize(
    "string, style, variant",
    [
        ("normal 12pt Comic Sans", NORMAL, NORMAL),
        ("italic normal 12pt Comic Sans", ITALIC, NORMAL),
        ("italic small-caps normal 12pt Comic Sans", ITALIC, SMALL_CAPS),
    ],
)
def test_parse_normal(string, style, variant):
    assert_font(font(string), "Comic Sans", 12, style, variant, NORMAL)


@pytest.mark.parametrize(
    "string, style",
    [
        ("italic 12pt Comic Sans", ITALIC),
        ("oblique 12pt Comic Sans", OBLIQUE),
    ],
)
def test_parse_style(string, style):
    assert_font(font(string), "Comic Sans", 12, style, NORMAL, NORMAL)


def test_parse_invalid_style():
    with pytest.raises(ValueError):
        font("wiggly small-caps bold 12pt Comic Sans")


def test_parse_variant():
    assert_font(
        font("italic small-caps 12pt Comic Sans"),
        "Comic Sans",
        12,
        ITALIC,
        SMALL_CAPS,
        NORMAL,
    )

    with pytest.raises(ValueError):
        font("italic wiggly bold 12pt Comic Sans")


def test_parse_weight():
    assert_font(
        font("italic small-caps bold 12pt Comic Sans"),
        "Comic Sans",
        12,
        ITALIC,
        SMALL_CAPS,
        BOLD,
    )

    with pytest.raises(ValueError):
        font("italic small-caps wiggly 12pt Comic Sans")


@pytest.mark.parametrize(
    "string",
    [
        "oblique italic 12pt Comic Sans",
        "italic small-caps oblique 12pt Comic Sans",
        "italic small-caps bold small-caps 12pt Comic Sans",
        "bold bold 12pt Comic Sans",
    ],
)
def test_parse_duplicates(string):
    with pytest.raises(ValueError):
        font(string)


def test_parse_invaid():
    with pytest.raises(ValueError):
        font(42)
