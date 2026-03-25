from typing import Any


class TypedProperty:
    def __init__(self, _type) -> None:
        self._type = _type

    def __set_name__(self, owner, name) -> None:
        self._name = name

    def __get__(self, instance, owner) -> Any:
        return instance.__dict__[self._name]

    def __set__(self, instance, value) -> None:
        if not isinstance(value, self._type):
            raise TypeError('%r should be other type: %r' % (self._name, self._type))
        instance.__dict__[self._name] = value

class ValidatedProperty(TypedProperty):
    def __init__(self, expected_type, _max=None, _min=None, min_length=None) -> None:
        super().__init__(expected_type)
        self._max = _max
        self._min = _min
        self._min_length = min_length

    def __get__(self, instance, owner) -> Any:
        return instance.__dict__[self._name]

    def __set__(self, instance, value) -> None:
        if isinstance(value, int):
            if self._min is not None and value < self._min:
                raise ValueError(f'{self._name} must be >= {self._min}')
            if self._max is not None and value > self._max:
                raise ValueError(f'{self._name} must be <= {self._max}')

        if isinstance(value, str):
            if self._min_length is not None and len(value) < self._min_length:
                raise ValueError(f'len of {self._name} must be >= {self._min_length}')

        super().__set__(instance, value)

