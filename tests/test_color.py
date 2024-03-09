import pytest

from travertino.colors import color, hsl, hsla, rgb, rgba


def assert_equal_color(actual, expected):
    assert actual.rgba.r == expected.rgba.r
    assert actual.rgba.g == expected.rgba.g
    assert actual.rgba.b == expected.rgba.b
    assert actual.rgba.a == expected.rgba.a


@pytest.mark.parametrize(
    "constructor, value, string",
    [
        (rgb, (10, 20, 30), "rgb(10, 20, 30)"),
        (rgba, (10, 20, 30, 0.5), "rgba(10, 20, 30, 0.5)"),
        (hsl, (10, 0.2, 0.3), "hsl(10, 0.2, 0.3)"),
        (hsla, (10, 0.2, 0.3, 0.5), "hsla(10, 0.2, 0.3, 0.5)"),
    ],
)
def test_repr(constructor, value, string):
    assert repr(constructor(*value)) == string


def test_rgb_hash():
    assert hash(rgb(10, 20, 30)) == hash(rgb(10, 20, 30))
    assert hash(rgb(10, 20, 30)) != hash(rgb(30, 20, 10))


def test_rgba_hash():
    assert hash(rgba(10, 20, 30, 0.5)) == hash(rgba(10, 20, 30, 0.5))
    assert hash(rgba(10, 20, 30, 1.0)) == hash(rgb(10, 20, 30))
    assert hash(rgb(10, 20, 30)) != hash(rgb(30, 20, 10))


def test_hsl_hash():
    assert hash(hsl(10, 0.2, 0.3)) == hash(hsl(10, 0.2, 0.3))
    assert hash(hsl(10, 0.3, 0.2)) != hash(hsl(10, 0.2, 0.3))


def test_hsla_hash():
    assert hash(hsla(10, 0.2, 0.3, 0.5)) == hash(hsla(10, 0.2, 0.3, 0.5))
    assert hash(hsla(10, 0.2, 0.3, 1.0)) == hash(hsl(10, 0.2, 0.3))
    assert hash(hsla(10, 0.3, 0.2, 0.5)) != hash(hsla(10, 0.2, 0.3, 0.5))
    assert hash(hsla(10, 0, 0, 0.5)) != hash(rgba(10, 0, 0, 0.5))


@pytest.mark.parametrize(
    "value, expected",
    [
        # Blacks
        ((0, 0.0, 0.0), (0x00, 0x00, 0x00)),
        ((60, 0.0, 0.0), (0x00, 0x00, 0x00)),
        ((180, 0.0, 0.0), (0x00, 0x00, 0x00)),
        ((240, 0.0, 0.0), (0x00, 0x00, 0x00)),
        ((360, 0.0, 0.0), (0x00, 0x00, 0x00)),
        # Whites
        ((0, 0.0, 1.0), (0xFF, 0xFF, 0xFF)),
        ((60, 0.0, 1.0), (0xFF, 0xFF, 0xFF)),
        ((180, 0.0, 1.0), (0xFF, 0xFF, 0xFF)),
        ((240, 0.0, 1.0), (0xFF, 0xFF, 0xFF)),
        ((360, 0.0, 1.0), (0xFF, 0xFF, 0xFF)),
        # Grays
        ((0, 0.0, 0.2), (0x33, 0x33, 0x33)),
        ((0, 0.0, 0.4), (0x66, 0x66, 0x66)),
        ((0, 0.0, 0.5), (0x80, 0x80, 0x80)),
        ((0, 0.0, 0.6), (0x99, 0x99, 0x99)),
        ((0, 0.0, 0.8), (0xCC, 0xCC, 0xCC)),
        # Primaries
        ((0, 1.0, 0.5), (0xFF, 0x00, 0x00)),
        ((60, 1.0, 0.5), (0xFF, 0xFF, 0x00)),
        ((120, 1.0, 0.5), (0x00, 0xFF, 0x00)),
        ((180, 1.0, 0.5), (0x00, 0xFF, 0xFF)),
        ((240, 1.0, 0.5), (0x00, 0x00, 0xFF)),
        ((300, 1.0, 0.5), (0xFF, 0x00, 0xFF)),
        ((360, 1.0, 0.5), (0xFF, 0x00, 0x00)),
        # Muted
        ((0, 0.25, 0.25), (0x50, 0x30, 0x30)),
        ((60, 0.25, 0.25), (0x50, 0x50, 0x30)),
        ((120, 0.25, 0.25), (0x30, 0x50, 0x30)),
        ((180, 0.25, 0.25), (0x30, 0x50, 0x50)),
        ((240, 0.25, 0.25), (0x30, 0x30, 0x50)),
        ((300, 0.25, 0.25), (0x50, 0x30, 0x50)),
        ((360, 0.25, 0.25), (0x50, 0x30, 0x30)),
        ((0, 0.25, 0.75), (0xCF, 0xAF, 0xAF)),
        ((60, 0.25, 0.75), (0xCF, 0xCF, 0xAF)),
        ((120, 0.25, 0.75), (0xAF, 0xCF, 0xAF)),
        ((180, 0.25, 0.75), (0xAF, 0xCF, 0xCF)),
        ((240, 0.25, 0.75), (0xAF, 0xAF, 0xCF)),
        ((300, 0.25, 0.75), (0xCF, 0xAF, 0xCF)),
        ((360, 0.25, 0.75), (0xCF, 0xAF, 0xAF)),
        ((0, 0.75, 0.75), (0xEF, 0x8F, 0x8F)),
        ((60, 0.75, 0.75), (0xEF, 0xEF, 0x8F)),
        ((120, 0.75, 0.75), (0x8F, 0xEF, 0x8F)),
        ((180, 0.75, 0.75), (0x8F, 0xEF, 0xEF)),
        ((240, 0.75, 0.75), (0x8F, 0x8F, 0xEF)),
        ((300, 0.75, 0.75), (0xEF, 0x8F, 0xEF)),
        ((360, 0.75, 0.75), (0xEF, 0x8F, 0x8F)),
        ((0, 0.75, 0.25), (0x70, 0x10, 0x10)),
        ((60, 0.75, 0.25), (0x70, 0x70, 0x10)),
        ((120, 0.75, 0.25), (0x10, 0x70, 0x10)),
        ((180, 0.75, 0.25), (0x10, 0x70, 0x70)),
        ((240, 0.75, 0.25), (0x10, 0x10, 0x70)),
        ((300, 0.75, 0.25), (0x70, 0x10, 0x70)),
        ((360, 0.75, 0.25), (0x70, 0x10, 0x10)),
    ],
)
def test_hsl(value, expected):
    assert_equal_color(hsl(*value), rgb(*expected))


@pytest.mark.parametrize(
    "value, expected",
    [
        ((60, 0.0, 0.0, 0.3), (0x00, 0x00, 0x00, 0.3)),
        ((60, 0.0, 1.0, 0.3), (0xFF, 0xFF, 0xFF, 0.3)),
        ((60, 1.0, 0.5, 0.3), (0xFF, 0xFF, 0x00, 0.3)),
        ((60, 0.25, 0.25, 0.3), (0x50, 0x50, 0x30, 0.3)),
        ((60, 0.25, 0.75, 0.3), (0xCF, 0xCF, 0xAF, 0.3)),
        ((60, 0.75, 0.75, 0.3), (0xEF, 0xEF, 0x8F, 0.3)),
        ((60, 0.75, 0.25, 0.3), (0x70, 0x70, 0x10, 0.3)),
    ],
)
def test_hsl_alpha(value, expected):
    assert_equal_color(hsla(*value), rgba(*expected))


@pytest.mark.parametrize(
    "constructor, value, name, min, max, actual",
    [
        (rgb, (-1, 120, 10), "red", 0, 255, -1),
        (rgb, (256, 120, 10), "red", 0, 255, 256),
        (rgb, (120, -1, 10), "green", 0, 255, -1),
        (rgb, (120, 256, 10), "green", 0, 255, 256),
        (rgb, (120, 10, -1), "blue", 0, 255, -1),
        (rgb, (120, 10, 256), "blue", 0, 255, 256),
        (rgba, (-1, 120, 10, 0.5), "red", 0, 255, -1),
        (rgba, (256, 120, 10, 0.5), "red", 0, 255, 256),
        (rgba, (120, -1, 10, 0.5), "green", 0, 255, -1),
        (rgba, (120, 256, 10, 0.5), "green", 0, 255, 256),
        (rgba, (120, 10, -1, 0.5), "blue", 0, 255, -1),
        (rgba, (120, 10, 256, 0.5), "blue", 0, 255, 256),
        (rgba, (120, 10, 60, -0.5), "alpha", 0, 1, -0.5),
        (rgba, (120, 10, 60, 1.1), "alpha", 0, 1, 1.1),
        (hsl, (-1, 0.5, 0.8), "hue", 0, 360, -1),
        (hsl, (361, 0.5, 0.8), "hue", 0, 360, 361),
        (hsl, (120, -0.1, 0.8), "saturation", 0, 1, -0.1),
        (hsl, (120, 1.1, 0.8), "saturation", 0, 1, 1.1),
        (hsl, (120, 0.8, -0.1), "lightness", 0, 1, -0.1),
        (hsl, (120, 0.8, 1.1), "lightness", 0, 1, 1.1),
        (hsla, (-1, 0.5, 0.8, 0.5), "hue", 0, 360, -1),
        (hsla, (361, 0.5, 0.8, 0.5), "hue", 0, 360, 361),
        (hsla, (120, -0.1, 0.8, 0.5), "saturation", 0, 1, -0.1),
        (hsla, (120, 1.1, 0.8, 0.5), "saturation", 0, 1, 1.1),
        (hsla, (120, 0.8, -0.1, 0.5), "lightness", 0, 1, -0.1),
        (hsla, (120, 0.8, 1.1, 0.5), "lightness", 0, 1, 1.1),
        (hsla, (120, 0.8, 0.5, -0.1), "alpha", 0, 1, -0.1),
        (hsla, (120, 0.8, 0.5, 1.1), "alpha", 0, 1, 1.1),
    ],
)
def test_invalid_color_constructor(constructor, value, name, min, max, actual):
    with pytest.raises(
        ValueError,
        match=rf"^{name} value should be between {min}-{max}\. Got {actual}$",
    ):
        constructor(*value)


###############
# Color parsing
###############


def assert_equal_hsl(value, expected):
    # Nothing fancy - a color is equal if the attributes are all the same
    actual = color(value)
    assert actual.h == expected.h
    assert actual.s == expected.s
    assert actual.l == expected.l
    assert actual.a == pytest.approx(expected.a, abs=0.001)


def assert_equal_rgb(value, expected):
    # Nothing fancy - a color is equal if the attributes are all the same
    actual = color(value)
    assert actual.r == expected.r
    assert actual.g == expected.g
    assert actual.b == expected.b
    assert actual.a == pytest.approx(expected.a, abs=0.001)


def test_noop():
    assert_equal_rgb(rgba(1, 2, 3, 0.5), rgba(1, 2, 3, 0.5))
    assert_equal_hsl(hsl(1, 0.2, 0.3), hsl(1, 0.2, 0.3))


@pytest.mark.parametrize(
    "value, expected",
    [
        ("rgb(1,2,3)", (1, 2, 3)),
        ("rgb(1, 2, 3)", (1, 2, 3)),
        ("rgb( 1 , 2 , 3)", (1, 2, 3)),
        ("#123", (0x11, 0x22, 0x33)),
        ("#112233", (0x11, 0x22, 0x33)),
        ("#abc", (0xAA, 0xBB, 0xCC)),
        ("#ABC", (0xAA, 0xBB, 0xCC)),
        ("#abcdef", (0xAB, 0xCD, 0xEF)),
        ("#ABCDEF", (0xAB, 0xCD, 0xEF)),
    ],
)
def test_parse_rgb(value, expected):
    assert_equal_rgb(value, rgb(*expected))


@pytest.mark.parametrize(
    "value", ["10, 20", "a, 10, 20", "10, b, 20", "10, 20, c", "10, 20, 30, 0.5"]
)
def test_parse_rgb_invalid(value):
    with pytest.raises(ValueError):
        color(f"rgb({value})")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("rgba(1,2,3,0.5)", (1, 2, 3, 0.5)),
        ("rgba(1, 2, 3, 0.5)", (1, 2, 3, 0.5)),
        ("rgba( 1 , 2 , 3 , 0.5)", (1, 2, 3, 0.5)),
        ("#1234", (0x11, 0x22, 0x33, 0.2666)),
        ("#11223344", (0x11, 0x22, 0x33, 0.2666)),
        ("#abcd", (0xAA, 0xBB, 0xCC, 0.8666)),
        ("#ABCD", (0xAA, 0xBB, 0xCC, 0.8666)),
        ("#abcdefba", (0xAB, 0xCD, 0xEF, 0.7294)),
        ("#ABCDEFBA", (0xAB, 0xCD, 0xEF, 0.7294)),
    ],
)
def test_parse_rgba(value, expected):
    assert_equal_rgb(value, rgba(*expected))


@pytest.mark.parametrize(
    "value",
    [
        "10, 20, 30",
        "a, 10, 20, 0.5",
        "10, b, 20, 0.5",
        "10, 20, c, 0.5",
        "10, 20, 30, c",
        "10, 20, 30, 0.5, 5",
    ],
)
def test_parse_rgba_invalid(value):
    with pytest.raises(ValueError):
        color(f"rgba({value})")


@pytest.mark.parametrize("value", ["1,20%,30%", "1, 20%, 30%", "1, 20% , 30%"])
def test_parse_hsl(value):
    assert_equal_hsl(f"hsl({value})", hsl(1, 0.2, 0.3))


@pytest.mark.parametrize(
    "value",
    ["1, 20%", "a, 20%, 30%", "1, a, 30%", "1, 20%, a)", "1, 20%, 30%, 0.5)"],
)
def test_parse_hsl_invalid(value):
    with pytest.raises(ValueError):
        color(value)


@pytest.mark.parametrize(
    "value", ["1,20%,30%,0.5", "1, 20%, 30%, 0.5", " 1, 20% , 30% , 0.5"]
)
def test_parse_hsla(value):
    assert_equal_hsl(f"hsla({value})", hsla(1, 0.2, 0.3, 0.5))


@pytest.mark.parametrize(
    "value",
    [
        "1, 20%, 30%",
        "a, 20%, 30%, 0.5",
        "1, a, 30%, 0.5",
        "1, 20%, a, 0.5",
        "1, 20%, 30%, a",
        "1, 20%, 30%, 0.5, 5",
    ],
)
def test_parse_hsla_invalid(value):
    with pytest.raises(ValueError):
        color(f"hsla({value})")


@pytest.mark.parametrize(
    "value, expected",
    [
        ("Red", (0xFF, 0, 0)),
        ("RED", (0xFF, 0, 0)),
        ("red", (0xFF, 0, 0)),
        ("rEd", (0xFF, 0, 0)),
        ("CornflowerBlue", (0x64, 0x95, 0xED)),
        ("cornflowerblue", (0x64, 0x95, 0xED)),
        ("CORNFLOWERBLUE", (0x64, 0x95, 0xED)),
        ("Cornflowerblue", (0x64, 0x95, 0xED)),
        ("CoRnFlOwErBlUe", (0x64, 0x95, 0xED)),
    ],
)
def test_parse_named_color(value, expected):
    assert_equal_rgb(value, rgb(*expected))


def test_parse_named_color_invalid():
    with pytest.raises(ValueError):
        color("not a color")
