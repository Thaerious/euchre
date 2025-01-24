class class_getter:
    def __init__(self, func):
        self.fget = func

    def __get__(self, _, __):
        return self.fget()
    
__all__ = ["class_getter"]    