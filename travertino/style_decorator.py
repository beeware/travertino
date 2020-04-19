__all__ = ["style"]

from travertino.style_properties import style_property, directional_property


def reapply(self):
    for style in self._PROPERTIES:
        self.apply(style, getattr(self, style))


def update(self, **styles):
    "Set multiple styles on the style definition."
    for name, value in styles.items():
        name = name.replace("-", "_")
        if not (name in self._PROPERTIES or name in self._DIRECTIONAL_PROPERTIES):
            raise NameError("Unknown style '{}'".format(name))

        setattr(self, name, value)


def copy(self, applicator=None):
    "Create a duplicate of this style declaration."
    dup = self.__class__()
    dup._applicator = applicator
    for prop_name in self._PROPERTIES:
        setattr(dup, prop_name, getattr(self, prop_name))
    return dup


def get_item(self, name):
    name = name.replace("-", "_")
    if name in self._PROPERTIES:
        return getattr(self, name)
    raise KeyError(name)


def set_item(self, name, value):
    name = name.replace("-", "_")
    if name in self._PROPERTIES:
        setattr(self, name, value)
    else:
        raise KeyError(name)


def del_item(self, name):
    name = name.replace("-", "_")
    if name in self._PROPERTIES:
        delattr(self, name)
    else:
        raise KeyError(name)


def items(self):
    result = []
    for name in self._PROPERTIES:
        try:
            result.append((name, getattr(self, "_%s" % name)))
        except AttributeError:
            pass
    return result


def keys(self):
    return set(self._PROPERTIES)


######################################################################
# Get the rendered form of the style declaration
######################################################################
def str_impl(self):
    return "; ".join(
        "{}: {}".format(name.replace("_", "-"), getattr(self, name))
        for name in sorted(self._PROPERTIES)
    )


def init_impl(style_properties, directional_properties, post_init=None):
    def init(self, **kwargs):
        for prop_name, prop in style_properties.items():
            if prop_name in kwargs:
                setattr(self, prop_name, kwargs[prop_name])
            else:
                setattr(self, prop_name, prop.initial)
        for prop_name, prop in directional_properties.items():
            if prop_name in kwargs:
                setattr(self, prop_name, kwargs[prop_name])

        if post_init is not None:
            post_init()

    return init


def style(cls):
    cls._PROPERTIES = []
    cls._DIRECTIONAL_PROPERTIES = []
    if not hasattr(cls, "apply"):
        raise AttributeError("Style must define an apply method")

    style_properties = {}
    directional_properties = {}
    for key, value in vars(cls).items():
        if isinstance(value, style_property):
            style_properties[key] = value
            setattr(
                cls,
                key,
                property(
                    fget=value.getter(key),
                    fset=value.setter(key),
                    fdel=value.deleter(key),
                ),
            )
            cls._PROPERTIES.append(key)
        if isinstance(value, directional_property):
            directional_properties[key] = value
            setattr(
                cls,
                key,
                property(
                    fget=value.getter(key),
                    fset=value.setter(key),
                    fdel=value.deleter(key),
                ),
            )
            cls._DIRECTIONAL_PROPERTIES.append(key)

    cls.reapply = reapply
    cls.update = update
    cls.copy = copy
    cls.__getitem__ = get_item
    cls.__setitem__ = set_item
    cls.__delitem__ = del_item
    cls.items = items
    cls.keys = keys
    cls.__str__ = str_impl
    post_init = getattr(cls, "__post_init__", None)
    cls.__init__ = init_impl(
        style_properties=style_properties,
        directional_properties=directional_properties,
        post_init=post_init,
    )
    return cls
