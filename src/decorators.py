import datetime
import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable[[Callable], Callable]:
    """
    Decorator for logging function calls.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Wrapper around the function for logging its calls.
            """
            # Get the current time and format it as a string
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Prepare string for positional arguments
            func_args = ", ".join(map(repr, args))
            # Prepare string for keyword arguments
            func_kwargs = ", ".join(f"{k}={v!r}" for k, v in kwargs.items())
            # Combine positional and keyword arguments into one string
            all_args = ", ".join(filter(None, [func_args, func_kwargs]))

            try:
                # Call the original function
                result = func(*args, **kwargs)
                # Create a log message for successful call
                log_message = f"{timestamp} - {func.__name__}({all_args}) -> {result}\n"
            except Exception as e:
                # Create a log message for errors
                log_message = f"{timestamp} - ERROR in {func.__name__}({all_args}): {e}\n"
                # Write the log message to a file or print it
                if filename:
                    with open(filename, "a") as file:
                        file.write(log_message)
                else:
                    print(log_message)
                raise

            # Write the log message to a file or print it
            if filename:
                with open(filename, "a") as file:
                    file.write(log_message)
            else:
                print(log_message)
            return result  # Return the result of the function call

        return wrapper  # Return the wrapper function

    return decorator  # Return the decorator function
