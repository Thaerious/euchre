# ObjectSerializer.py
class ObjectSerializer:
    @staticmethod
    def to_dict(obj):
        """
        Convert an object's properties into a dictionary.
        Handles nested objects and lists of objects recursively.
        """
        if isinstance(obj, dict):  # If already a dictionary, return as is
            return {k: ObjectSerializer.to_dict(v) for k, v in obj.items()}

        elif isinstance(obj, list | tuple | set):  # Handle iterable objects
            return [ObjectSerializer.to_dict(item) for item in obj]

        elif hasattr(obj, "__dict__"):  # If it's an object with attributes
            d = {}
            for k, v in obj.__dict__.items():
                if not k.startswith("__"):
                    d[k] = ObjectSerializer.to_dict(v)
            return d

        else:  # Base case: return the value as is
            return obj
