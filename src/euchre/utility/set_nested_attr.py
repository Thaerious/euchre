from .log import get_logger
logger = get_logger(__name__)

def set_nested_attr(obj, path, value):
    """
    Set the value of a nested attribute on an object using a dotted path.
    It lets you handle dotted paths where intermediate objects are unknown at compile time.

    This function allows modifying deeply nested attributes dynamically.
    For example, given:
        class A: pass
        a = A(); a.b = A(); a.b.c = 10
        set_nested_attr(a, "b.c", 99)
    The attribute `a.b.c` will be updated to 99.

    Args:
        obj (object): The root object on which to set the attribute.
        path (str):  A dot-separated string representing the attribute path
                    (e.g., "b.c.d").
        value (Any): The value to assign to the final attribute.

    Prints:
        Debug information showing the path traversal and the final assignment.
    """    

    logger.debug(f"set_nested_attr({path}, {value})", stacklevel=3)
    attrs = path.split(".")
    for attr in attrs[:-1]:
        obj = getattr(obj, attr)

    setattr(obj, attrs[-1], value)
