"""
custom_json_serializer.py

Provides a custom JSON serializer function that supports objects
defining a `__json__()` method. Useful for serializing complex types
like game state, cards, or custom exceptions in a consistent way.
"""


def custom_json_serializer(obj):
    """Custom JSON serializer that looks for __json__()"""
    if hasattr(obj, "__json__"):
        return obj.__json__()  # Call __json__() if it exists
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
