"""
del_string.py

Utility function to convert a list of items into a single delimited string,
with optional wrapping around each item. Commonly used for formatting output
such as CSV-like lines, logging, or display in user interfaces.
"""


def del_string(a_list, delimiter=", ", wrap=""):
    """
    Convert a list into a single string with a delimiter between items.

    Args:
        a_list (list): The list of items to join.
        delimiter (str, optional): The delimiter to insert between items. Defaults to ", ".
        wrap (str, optional): A string to wrap around each item. Defaults to "".

    Returns:
        str: A delimited string of the list items.
    """
    sb = ""

    length = len(a_list) - 1
    if length < 0:
        return ""

    for i in range(length):
        item = a_list[i]
        sb = sb + wrap + str(item) + wrap + delimiter

    item = a_list[-1]
    sb = sb + wrap + str(item) + wrap

    return sb
