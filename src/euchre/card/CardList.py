from euchre.delString import delString
import Card
from typing import List

class CardList(list):
    """
    A list-like class that holds multiple `Card` objects and provides helper methods for working with them.
    """

    def __init__(self, stringList: List[str] = []):
        """
        Initialize a CardList from a list of card strings.

        Args:
            stringList (List[str]): A list of card representations as strings (e.g., ["10♥", "J♠"]).
        """
        super().__init__(Card(string) for string in stringList)  # Ensures only `Card` objects are added

    def __str__(self) -> str:
        """
        Return a formatted string representation of the CardList.

        Uses `delString()` to create a clean, formatted output.
        """
        return delString(self)