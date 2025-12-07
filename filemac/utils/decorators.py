class Decorators:
    @staticmethod
    def for_loop(iterable: list | tuple | str):
        """
        A for loop decorator that calls the decorated function with each element
        from the provided list or tuple.

        Args:
            data_list: A list, str or tuple of data to iterate over.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                for item in iterable:
                    func(item, *args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def while_loop(iterable: list | tuple | str):
        """
        A while loop decorator that calls the decorated function with each element
        from the provided list or tuple.

        Args:
            iterable: A list, str or tuple of data to iterate over.
        """

        def decorator(func):
            def wrapper(*args, **kwargs):
                index = 0
                while index <= len(iterable):
                    func(iterable[index], *args, **kwargs)
                    index += 1

            return wrapper

        return decorator

    def threading(self):
        ...


dcr = Decorators()
