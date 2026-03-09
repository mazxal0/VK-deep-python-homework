import collections
import functools
import typing
import time
from itertools import islice


class NotAliveError(Exception):
    """Custom error which raise when service is not alive"""
    pass


def circuit_breaker(
        state_count: int=20,
        error_count: int=5,
        network_errors:typing.Optional[list[type[Exception]]]=None,
        sleep_time_sec:int=10
) -> typing.Callable:
    if state_count <= 10:
        raise ValueError("state_count must be greater than 10")
    if error_count >= 10:
        raise ValueError("error_count must be less than 10")

    def decorator(func: typing.Callable) -> typing.Callable:
        actual_network_errors = tuple(network_errors) if network_errors is not None else (
            ConnectionError, TimeoutError
        )
        history_calls = collections.deque(maxlen=state_count)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> typing.Any:
            try:
                if len(history_calls) >= error_count:
                    current_slice = list(islice(history_calls, len(history_calls)-error_count, None))
                    if all(state is False for state in current_slice):
                        raise NotAliveError

                if history_calls and history_calls[-1] is False:
                    time.sleep(sleep_time_sec)

                res = func(*args, **kwargs)
                history_calls.append(True)
                return res
            except actual_network_errors:
                history_calls.append(False)
                raise

        return wrapper

    return decorator
