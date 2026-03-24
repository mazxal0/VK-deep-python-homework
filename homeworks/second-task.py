from typing import Any, List, Iterator


class StackIsEmpty(Exception):
    """Exception raised when a stack is empty"""
    pass


class Stack:
    def __init__(self) -> None:
        self._stack: List[Any] = []

    def __len__(self) -> int:
        return len(self._stack)

    def __str__(self) -> str:
        return f'Stack({", ".join(map(str, self._stack))})'

    def __repr__(self) -> str:
        return f"Stack({self._stack})"

    def __iter__(self) -> Iterator[Any]:
        yield from self._stack

    def __contains__(self, item: Any) -> bool:
        return item in self._stack

    def __getitem__(self, index: int) -> Any:
        if index >= len(self) or (index < 0 and index < -len(self)):
            raise IndexError("Stack index out of range")
        return self._stack[index]

    def __enter__(self) -> "Stack":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> bool:
        self._stack.clear()

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Stack):
            return NotImplemented

        if len(self) != len(other):
            return False

        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True

    def push(self, value: Any) -> None:
        self._stack.append(value)

    def pop(self) -> Any:
        if not self._stack:
            raise StackIsEmpty("Stack is empty")
        return self._stack.pop()
