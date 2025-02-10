# euchre/bots/__init__.py

# Import classes and functions to expose them at the package level
from .Bot_0 import Bot_0
from .Bot_1 import Bot_1
from .Bot_2 import Bot_2

# Define __all__ to specify what is exported when using 'from euchre import *'
__all__ = [
    'Bot_0',
    'Bot_1',
    'Bot_2',
]