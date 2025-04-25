def custom_json_serializer(obj):
    """Custom JSON serializer that looks for __json__()"""
    if hasattr(obj, "__json__"):
        return obj.__json__()  # Call __json__() if it exists
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")
