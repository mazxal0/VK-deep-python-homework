import collections
import functools
import typing


class NotAliveError(Exception):
    """"""
    pass


def circuit_breaker(
        state_count: int=20,
        error_count: int=5,
        network_errors:typing.Optional[list[type[Exception]]]=None,
        sleep_time_sec:int=10
) -> typing.Callable:
    def decorator(func: typing.Callable) -> typing.Callable:
        actual_network_errors = tuple(network_errors) if network_errors is not None else None
        if actual_network_errors is None:
            actual_network_errors = tuple([ConnectionError, TimeoutError])

        history_calls = collections.deque(maxlen=state_count)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> typing.Any:
            try:
                res = func(*args, **kwargs)
                history_calls.append(True)
                return res
            except tuple(actual_network_errors):
                history_calls.append(False)
                raise
            except Exception:
                raise
        return wrapper
    return decorator
