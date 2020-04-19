__all__ = ["style_property"]


class style_property:
    def __init__(self, choices, initial=None, validated=True):
        if validated:
            try:
                initial = choices.validate(initial)
            except ValueError:
                raise ValueError(
                    "Invalid initial value '{}' for property".format(initial))
        self.choices = choices
        self.initial = initial
        self.validated = validated

    def getter(self, name):

        def actual_getter(item):
            return getattr(item, self._actual_name(name), self.initial)

        return actual_getter

    def setter(self, name):

        def actual_setter(item, value):
            if self.validated:
                try:
                    value = self.choices.validate(value)
                except ValueError:
                    raise ValueError(
                        "Invalid value '{}' for property '{}'; Valid values are: {}".format(
                            value, name, self.choices
                        )
                    )

            try:
                existing_value = getattr(item, self._actual_name(name))
                if value != existing_value:
                    setattr(item, self._actual_name(name), value)
                    item.apply(name, value)
            except AttributeError:
                setattr(item, self._actual_name(name), value)

        return actual_setter

    def deleter(self, name):

        def actual_deleter(item):
            try:
                value = getattr(item, self._actual_name(name), self.initial)
                delattr(item, self._actual_name(name))
                if value != self.initial:
                    item.apply(name, self.initial)
            except AttributeError:
                # Attribute doesn't exist
                pass

        return actual_deleter

    @classmethod
    def _actual_name(cls, name):
        return "_" + name


class directional_property:

    def getter(self, name):
        
        def actual_getter(item):
            return (
                getattr(item, self.top_name(name)),
                getattr(item, self.right_name(name)),
                getattr(item, self.bottom_name(name)),
                getattr(item, self.left_name(name)),
            )
        
        return actual_getter
    
    def setter(self, name):
        
        def actual_setter(item, value):
            if isinstance(value, tuple):
                if len(value) == 4:
                    setattr(item, self.top_name(name), value[0])
                    setattr(item, self.right_name(name), value[1])
                    setattr(item, self.bottom_name(name), value[2])
                    setattr(item, self.left_name(name), value[3])
                elif len(value) == 3:
                    setattr(item, self.top_name(name), value[0])
                    setattr(item, self.right_name(name), value[1])
                    setattr(item, self.bottom_name(name), value[2])
                    setattr(item, self.left_name(name), value[1])
                elif len(value) == 2:
                    setattr(item, self.top_name(name), value[0])
                    setattr(item, self.right_name(name), value[1])
                    setattr(item, self.bottom_name(name), value[0])
                    setattr(item, self.left_name(name), value[1])
                elif len(value) == 1:
                    setattr(item, self.top_name(name), value[0])
                    setattr(item, self.right_name(name), value[0])
                    setattr(item, self.bottom_name(name), value[0])
                    setattr(item, self.left_name(name), value[0])
                else:
                    raise ValueError("Invalid value for '{}'; value must be an number, or a 1-4 tuple.".format(name))
            else:
                setattr(item, self.top_name(name), value)
                setattr(item, self.right_name(name), value)
                setattr(item, self.bottom_name(name), value)
                setattr(item, self.left_name(name), value)
        
        return actual_setter
    
    def deleter(self, name):

        def actual_deleter(item):
            delattr(item, self.top_name(name))
            delattr(item, self.right_name(name))
            delattr(item, self.bottom_name(name))
            delattr(item, self.left_name(name))
        
        return actual_deleter
    
    @classmethod
    def top_name(cls, name):
        return name + "_top"

    @classmethod
    def right_name(cls, name):
        return name + "_right"

    @classmethod
    def bottom_name(cls, name):
        return name + "_bottom"

    @classmethod
    def left_name(cls, name):
        return name + "_left"
