from pydantic import validate_call, constr


class DuplicateIdentifier(Exception):
    """
    Exception raised when a duplicate identifier is encountered.
    """

    @validate_call
    def __init__(self, __message: constr(min_length=1) = "Duplicate identifier", /):
        super().__init__(__message)


__all__ = ("DuplicateIdentifier",)
