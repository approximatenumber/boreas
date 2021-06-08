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
        return value / 10 if _is_number(str(value)) else None
    return wrapped

def divide_by_100(func):
    """Divides function output value by 100."""
    def wrapped(self):
        value = func(self)
        return value / 100 if _is_number(str(value)) else None
    return wrapped

def multiply_by_10(func):
    """Mutiplies function output value by 10."""
    def wrapped(self):
        value = func(self)
        return value * 10 if _is_number(str(value)) else None
    return wrapped
