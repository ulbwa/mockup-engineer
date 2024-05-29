from pydantic import validate_call, constr


class TemplateNotFound(Exception):
    """
    Exception raised when a template is not found.
    """

    @validate_call
    def __init__(self, __message: constr(min_length=1) = "Template not found", /):
        super().__init__(__message)


__all__ = ("TemplateNotFound",)
