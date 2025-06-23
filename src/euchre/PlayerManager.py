from euchre.EuchreError import EuchreError
from euchre.player import Player, Team
from euchre.utility.rotate import rotate_to
import euchre.constants as const
import json

class PlayerManager:
    def __init__(self, names: list[str], has_trump):
        if not hasattr(has_trump, "trump"):
            raise TypeError("Parameter must have a trump method")

        self._players = [Player(name, i) for i, name in enumerate(names)]
        self._order: list[int] = [0, 1, 2, 3]
        self._dealer_index = self._order[3]
        self._current_player_index = self._order[0]
        self._lead_index = self._order[0]
        self._maker_index = None
        self._has_trump = has_trump
        self._teams = []
        
        self._teams.append(Team([self._players[0], self._players[2]]))
        self._teams.append(Team([self._players[1], self._players[3]]))
        self._players[0].team = self._teams[0]
        self._players[1].team = self._teams[1]
        self._players[2].team = self._teams[0]
        self._players[3].team = self._teams[1]

    def __getitem__(self, key):
        return self.get(key)

    def __str__(self):
        sb = ""
        for p in self._players:
            sb = sb + (str)(p) + "\n"
        
        for i, t in enumerate(self.teams):
            sb = sb + f"Team {i} {[p.name for p in t.players]} "
            sb = sb + f"{t.score}"
            sb = sb + "\n"

        sb = sb + f"order: {self._order}" + "\n"
        sb = sb + f"current: {self._current_player_index}" + "\n"
        sb = sb + f"lead: {self._lead_index}" + "\n"
        sb = sb + f"dealer: {self._dealer_index}" + "\n"
        sb = sb + f"maker: {self._maker_index}"

        return sb

    def __iter__(self):
        return iter(self._players)   

    @property
    def teams(self) -> list[Team]:
        return self._teams.copy()

    @property
    def order(self) -> list[int]:
        """
        Get the current play order of players.

        Returns:
            List[int]: A copy of the list representing player indices in current order.
        """
        return self._order.copy()

    @property
    def maker(self) -> Player:
        if self._maker_index is None:
            raise EuchreError("Maker not set.")

        return self._players[self._maker_index]

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
    def current(self) -> Player:
        """
        Retrieve the currently active player.

        Returns:
            Player: The player object for the current player.
        """
        return self._players[self._current_player_index]

    def rotate_to_player(self, index):
        if isinstance(index, Player):
            index = index.index

        rotate_to(self._order, index)
        self.current_player_index = index
        self.lead_index = index

    def set_maker(self):
        self._maker_index = self._current_player_index

    def get_opposite_team(self, team: Team):
        if self._teams[0] == team:
            return self._teams[1]
        return self._teams[0]

    def clear(self) -> None:        
        for player in self._players:
            player.clear()

    def rotate(self) -> None:
        """
        Make the player after the current player current, 
        updates the order, dealer, current player, and lead player.
        """
        rotate(self._order)
        self._dealer_index = self._order[3]
        self._current_player_index = self._order[0]
        self._lead_index = self._order[0]
        self._maker_index = None

    def activate_next_player(self) -> Player:
        """
        Advance to the next player in the order (circularly) and return that player.

        Returns:
            Player: The player who is now active.
        """
        current_index = self._order.index(self._current_player_index)
        next_index = (current_index + 1) % len(self._order)
        self._current_player_index = self._order[next_index]
        return self.current

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
        self.current.alone = True
        partner_index = (self._current_player_index + 2) % 4
        self._order.remove(partner_index)

    def has(self, index: int | str) -> bool:
        if index is None:
            raise TypeError("Index must be an int or str, not None")

        if isinstance(index, str):
            for player in self._players:
                if player.name == index:
                    return True
            return False

        return index in self._players

    def get(self, index: int | str) -> Player:
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
    
    def score_hand(self) -> int:
        """
        Score a completed Euchre hand based on the tricks won by each side.

        Args:
            maker (int): Index of the player who made trump.
            tricks (List[int]): Number of tricks won, indexed by each of the four players.
            isAlone (bool): True if the maker's team played alone, otherwise False.

        Returns:
            int:
                4 if the maker's team took all 5 tricks alone,
                2 if the maker's team took all 5 tricks (not alone),
                1 if the maker's team took 3 or 4 tricks,
                -2 if the opposing team took 3 or more tricks.

        Raises:
            EuchreException: If the total number of tricks does not sum to 5.
        """

        maker = self.players.maker        
        maker_tricks = maker.tricks
        defending_team = self.players.get_opposite_team(maker.team)
        
        if maker_tricks >= const.REQUIRED_TRICKS_TO_WIN:
            self.won_last_hand = maker.team
        else:
            self.won_last_hand = defending_team

        if maker_tricks == const.NUM_TRICKS_PER_HAND and maker.team.has_alone:
            maker.team.score = maker.team.score + 4
        elif maker_tricks == const.NUM_TRICKS_PER_HAND:
            maker.team.score = maker.team.score + 2
        elif maker_tricks >= const.REQUIRED_TRICKS_TO_WIN:
            maker.team.score = maker.team.score + 1
        else:
            defending_team.score += 2         

    def __json__(self):
        return {
            "players": self._players,
            "order": self._order,
            "dealer": self._dealer_index,
            "lead": self._lead_index,
            "maker": self._maker_index,
            "teams": self.teams
        }