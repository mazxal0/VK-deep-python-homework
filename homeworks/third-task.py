from typing import Any


class TypedProperty:
    def __init__(self, _type) -> None:
        self._type = _type

    def __set_name__(self, owner, name) -> None:
        self._name = name

    def __get__(self, instance, owner) -> Any:
        print(instance.__dict__)
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
        return super().__get__(instance, owner)

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


class RegistryMeta(type):
    registry = dict()

    def __new__(cls, name, bases, namespace):
        if name in cls.registry:
            raise AttributeError(f'class {name} has already been registered')

        new_class = super().__new__(cls, name, bases, namespace);

        cls.registry[name] = new_class
        return new_class


class ModelMeta(RegistryMeta):
    def __new__(cls, name, bases, namespace):
        _fields = dict()
        for attr, value in namespace.items():
            if isinstance(value, TypedProperty):
                _fields[attr] = value
        namespace['_fields'] = dict(_fields)
        return super().__new__(cls, name, bases, namespace)


class Model(metaclass=ModelMeta):
    pass
