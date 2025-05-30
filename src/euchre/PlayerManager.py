from euchre.EuchreError import EuchreError
from euchre.player import Player, Team
from euchre.utility.rotate import rotate

class PlayerManager:
    def __init__(self, names: list[str], has_trump):
        if not hasattr(has_trump, "trump"):
            raise TypeError("Parameter must have a to_json method")

        self._players = [Player(name, i) for i, name in enumerate(names)]
        self._order: list[int] = [0, 1, 2, 3]
        self._dealer_index = self._order[3]
        self._current_player_index = self._order[0]
        self._lead_index = self._order[0]
        self._has_trump = has_trump

    @property
    def order(self) -> list[int]:
        """
        Get the current play order of players.

        Returns:
            List[int]: A copy of the list representing player indices in current order.
        """
        return self._order.copy()

    @property
    def lead_player(self) -> Player:
        """
        Retrieve the player who is leading the current trick.

        Returns:
            Player: The player in the lead position for the current trick.
        """
        return self._players[self._lead_index]
    
    @property
    def dealer(self) -> Player:
        """
        Retrieve the current dealer.

        Returns:
            Player: The dealer player object.
        """
        return self._players[self._dealer_index]

    @property
    def current_player(self) -> Player:
        """
        Retrieve the currently active player.

        Returns:
            Player: The player object for the current player.
        """
        return self._players[self._current_player_index]

    def rotate(self) -> None:
        """
        Make the player after the current player current, 
        updates the order, dealer, current player, and lead player.
        """
        rotate(self._order)
        self._dealer_index = self._order[3]
        self._current_player_index = self._order[0]
        self._lead_index = self._order[0]

    def activate_dealer(self) -> None:
        """
        Make the dealer the current player.
        """
        self._current_player_index = self._dealer_index

    def activate_first_player(self) -> None:
        """
        Make the first player from the order the current player.
        """
        self._current_player_index = self._order[0]

    def reset_lead_player(self):
        """
        Reset the lead player to be the current player.
        Used to explicitly set the player who will lead the next trick.
        """
        self._lead_index = self._current_player_index    

    def go_alone(self) -> None:
        """
        Indicate that the current player goes alone, removing their partner from the play order.

        Raises:
            EuchreException: If trump is not set.
        """
        if self._has_trump.trump is None:
            raise EuchreError("Trump must be made before going alone.")

        # Mark the current player as going alone
        self.current_player.alone = True
        partner_index = (self._current_player_index + 2) % 4
        self._order.remove(partner_index)

    def get_player(self, index: int | str) -> Player:
        """
        Retrieve a player by playing order or name.

        Args:
            index (int): The index of the player in the list.

        Returns:
            Player: The player object at the given index.
        """

        if index is None:
            raise TypeError("Index must be an int or str, not None")

        if isinstance(index, str):
            for player in self._players:
                if player.name == index:
                    return player
            raise ValueError(f"No player with name '{index}'")

        return self._players[index]        