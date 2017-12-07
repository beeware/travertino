
class at_least:
    "An annotation to wrap around a value to describe that it is a minimum bound"
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'at least {0}'.format(self.value)

    def __eq__(self, other):
        try:
            return self.value == other.value
        except AttributeError:
            return False


class IntrinsicSize:
    """Representation of the intrinsic size of an object.


    width: The width of the node.
    height: The height of the node.
    ratio: The height between height and width. width = height * ratio
    """
    def __init__(self, layout=None):
        self._layout = layout
        self._width = None
        self._height = None

        self._ratio = None

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        if self._width != value:
            self._width = value

            if self._layout:
                self._layout.dirty(intrinsic_width=value)

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        if self._height != value:
            self._height = value

            if self._layout:
                self._layout.dirty(intrinsic_height=value)

    @property
    def ratio(self):
        return self._ratio

    @ratio.setter
    def ratio(self, value):
        if self._ratio != value:
            self._ratio = value
            if self._layout:
                self._layout.dirty(intrinsic_ratio=value)
