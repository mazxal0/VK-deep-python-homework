class TypedProperty:
    def __init__(self, _type):
        self._type = _type

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, self._type):
            raise TypeError('%r should be other type: %r' % (self._name, self._type))
        instance.__dict__[self._name] = value
