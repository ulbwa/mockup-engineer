class SingletonMeta(type):
    """
    A metaclass for creating singleton classes.
    """

    __instances = {}

    def __call__(cls, *args, **kwargs):
        """
        If an instance of the class does not already exist, create it and store it
        in the __instances dictionary. Otherwise, return the existing instance.

        :param args: Positional arguments to initialize the class.
        :param kwargs: Keyword arguments to initialize the class.

        :return: The singleton instance of the class.
        """
        if cls not in cls.__instances:
            cls.__instances[cls] = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls.__instances[cls]


__all__ = ("SingletonMeta",)
