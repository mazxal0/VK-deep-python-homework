from typing import Any, List


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

    def push(self, value: Any) -> None:
        self._stack.append(value)

    def pop(self) -> Any:
        if not self._stack:
            raise StackIsEmpty("Stack is empty")
        return self._stack.pop()
