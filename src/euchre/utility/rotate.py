"""
rotate.py

Provides list rotation utilities for in-place reordering:
- `rotate`: moves the first item to the end of the list.
- `rotate_to`: rotates the list until the specified target is at the front.

Useful for managing turn order or circular sequences in games and simulations.
"""


def rotate(items):
    """Move the last item to the first
    Modifies the list.
    """
    items.append(items.pop(0))
    return items


def rotate_to(items, target):
    """repeatedly move the last item to the first until target is first"""
    if target not in items:
        raise ValueError("Can not rotate list, target not present.")
    while items[0] != target:
        items.append(items.pop(0))

    return items
