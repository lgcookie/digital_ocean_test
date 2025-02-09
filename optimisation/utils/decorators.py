def add_to_dict(dict_name):
    def decorator(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            getattr(self, dict_name).update(result)
            return result
        return wrapper
    return decorator