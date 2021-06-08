def divide_by_10(func):
    """Divides function output value by 10."""
    def wrapped(args, **kwargs):
        value = func()
        return value / 10 if value else None
    return wrapped

def divide_by_100(func):
    """Divides function output value by 100."""
    def wrapped(args, **kwargs):
        value = func()
        return value / 100 if value else None
    return wrapped
