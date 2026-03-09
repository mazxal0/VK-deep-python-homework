import collections
import functools
import typing


class NotAliveError(Exception):
    """Custom error which raise when service is not alive"""
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
                if len(history_calls) >= error_count:
                    current_slice = list(history_calls)[-error_count:]
                    if all(state is False for state in current_slice):
                        raise NotAliveError

                res = func(*args, **kwargs)
                history_calls.append(True)
                return res
            except actual_network_errors:
                history_calls.append(False)
                raise
            except Exception:
                raise
        return wrapper
    return decorator
