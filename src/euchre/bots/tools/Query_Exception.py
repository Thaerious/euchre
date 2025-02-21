
class Query_Exception(Exception):
    def __init__(self, query, original_exception=None):
        self.query = query
        self.original_exception = original_exception
        message = f"Error regarding query: {query}"

        if original_exception is not None:
            message += f" | Original Error: {original_exception}"

        super().__init__(message)