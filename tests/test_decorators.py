import datetime
import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """
    Декоратор для логирования вызовов функций.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обертка вокруг функции для логирования её вызовов.
            """
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_args = ", ".join(map(repr, args))
            func_kwargs = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            all_args = ", ".join(filter(None, [func_args, func_kwargs]))

            try:
                result = func(*args, **kwargs)
                log_message = f"{timestamp} - {func.__name__}({all_args}) -> {result}\n"
            except Exception as e:
                log_message = f"{timestamp} - ERROR in {func.__name__}({all_args}): {e}\n"
                if filename:
                    with open(filename, "a") as file:
                        file.write(log_message)
                else:
                    print(log_message)
                raise

            if filename:
                with open(filename, "a") as file:
                    file.write(log_message)
            else:
                print(log_message)

            return result

        return wrapper

    return decorator
