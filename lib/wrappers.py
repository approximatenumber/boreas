from functools import wraps
import logging
import time


logger = logging.getLogger("wrappers")


def _is_number(n):
    try:
        float(n)   # Type-casting the string to `float`.
                   # If string is not a valid `float`, 
                   # it'll raise `ValueError` exception
    except ValueError:
        return False
    return True


def divide_by_10(func):
    """Divides function output value by 10."""
    def wrapped(self):
        value = func(self)
        return value / 10 if _is_number(str(value)) else value
    return wrapped


def divide_by_100(func):
    """Divides function output value by 100."""
    def wrapped(self):
        value = func(self)
        return value / 100 if _is_number(str(value)) else value
    return wrapped


def multiply_by_10(func):
    """Mutiplies function output value by 10."""
    def wrapped(self):
        value = func(self)
        return value * 10 if _is_number(str(value)) else value
    return wrapped


def retry(retries=5, time_between_retries=0, exception_class=Exception):
    if callable(retries):
        original_decorated_function = retries
        retries = 5
    else:
        original_decorated_function = None

    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            current_try = retries
            logger.debug(f"Will execute '{func.__name__}' for {retries} times")
            while True:
                try:
                    return func(*args, **kwargs)
                except exception_class as e:
                    if current_try > 0:
                        logger.error(f"Exception {type(e)}: {e} occurred. Retrying for {current_try - 1}")
                        current_try -= 1
                        time.sleep(time_between_retries)
                    else:
                        logger.error("Retry limit exhausted, raising")
                        raise

        return wrapped

    if original_decorated_function is not None:
        return wrapper(original_decorated_function)
    else:
        return wrapper
