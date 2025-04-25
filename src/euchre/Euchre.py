import json

from euchre.card import Card, Deck, Trick, playable
from euchre.Player import Player, PlayerList, Team

from .custom_json_serializer import custom_json_serializer
from .rotate import rotate_to

NUM_PLAYERS = 4
NUM_CARDS_PER_PLAYER = 5
NUM_TRICKS_PER_HAND = 5
REQUIRED_TRICKS_TO_WIN = 3

class EuchreError(Exception):
    """
    Custom exception class for Euchre-specific errors.
    """

    def __init__(self, msg: str) -> None:
        """
        Initialize the EuchreError with an error message.

        Args:
            msg (str): The error message.
        """
        super().__init__(msg)

    def to_json(self, indent=2):
        return json.dumps(self, indent=indent, default=custom_json_serializer)

    def __json__(self):
        return {"type": EuchreError.__name__, "message": str(self)}

class Euchre:
    """
    The core class representing a single game of Euchre.
    """

    def __init__(self, names: list[str], seed=None) -> None:
        """
        Initialize a new Euchre game instance.

        Args:
            names (List[str]): A list of player names, in seating order.
        """
        self.players = PlayerList(names)
        self._order: list[int] = [0, 1, 2, 3]
        self.current_player_index = self._order[0]
        self.dealer_index = self._order[3]
        self.lead_index = self._order[0]
        self.hand_count = 0
        self.win_condition = 10

        self._teams = []
        self._teams.append(Team([self.players[0], self.players[2]]))
        self._teams.append(Team([self.players[1], self.players[3]]))
        self.players[0].team = self._teams[0]
        self.players[1].team = self._teams[1]
        self.players[2].team = self._teams[0]
        self.players[3].team = self._teams[1]

        self.seed = seed
        self.deck = Deck(seed)
        self.__reset()
        self._tricks: list[Trick] = []

    @property
    def order(self):
        return self._order.copy()

    @order.setter
    def order(self, value):
        self._order = value.copy()
        self.current_player_index = self._order[0]
        self.dealer_index = self._order[3]
        self.lead_index = self._order[0]

    def __reset(self) -> None:
        """
        Reset the state for a new hand (e.g., on dealing a new hand).
        """
        self._up_card: Card | None = None
        self._down_card: Card | None = None
        self.discard: Card | None = None
        self.trump: str | None = None
        self.maker_index: int | None = None

    @property
    def lead_player(self) -> Player:
        return self.players[self.lead_index]

    @property
    def teams(self) -> list[int]:
        return self._teams.copy()

    @property
    def up_card(self) -> str:
        return self._up_card

    @up_card.setter
    def up_card(self, value):
        if value is None:
            self._up_card = None
        else:
            self._up_card = Card(self.deck, value)

    @property
    def down_card(self) -> str:
        return self._down_card

    @down_card.setter
    def down_card(self, value):
        if value is None:
            self._down_card = None
        else:
            self._down_card = Card(self.deck, value)

    @property
    def hands_played(self) -> int:
        """
        Get the number of hands that have been completed so far.

        Returns:
            int: The total number of hands completed in the game.
        """
        return self.hand_count

    @property
    def trump(self) -> str | None:
        """
        Get the suit that is trump for the current hand.

        Returns:
            Optional[str]: The trump suit as a string, or None if no trump is set yet.
        """
        return self.deck.trump

    @trump.setter
    def trump(self, value):
        if value not in ["♠", "♥", "♣", "♦", None]:
            raise Exception(f"Unexpected value: '{value}'")
        self.deck.trump = value

    @property
    def has_trick(self) -> bool:
        """
        Check if at least one trick has been started.

        Returns:
            bool: True if a trick is in progress or completed, False otherwise.
        """
        return len(self._tricks) > 0

    def add_trick(self) -> None:
        """
        Start a new trick for the current hand.

        Raises:
            EuchreException: If trump hasn't been declared, or if the previous trick is not finished.
        """
        if self.trump is None:
            raise EuchreError("Trump must be made before adding a trick.")
        if self.has_trick and not self.is_trick_finished:
            raise EuchreError("Previous trick not complete.")
        self._tricks.append(Trick(self.trump, self._order))

    @property
    def tricks(self) -> list[Trick]:
        """
        Get a copy of the list of Tricks played in this hand so far.

        Returns:
            List[Trick]: A copy of the current hand's tricks.
        """

        return self._tricks.copy()

    @property
    def current_trick(self) -> Trick:
        """
        Get the current (latest) trick.

        Returns:
            Trick: A copy of the latest trick.
        """
        if len(self.tricks) == 0:
            return None
        return self._tricks[-1]

    def shuffle_deck(self) -> None:
        """
        Shuffle the deck. Typically called after next_hand but before dealing.
        """

        self._down_card = None
        self._discard = None
        self._up_card = None

        for player in self.players:
            player.clear()

        # requires a new deck because cards are removed from the deck during dealing
        self.deck.shuffle()

    def next_hand(self) -> None:
        """
        Advance to the next hand if the current hand is finished.

        Raises:
            EuchreException: If the current hand is not yet finished.
        """
        if not self.is_hand_finished:
            raise EuchreError("Hand not finished.")

        self._tricks = []
        self.hand_count += 1
        self._order = []

        # the dealer is advanced by one
        self.dealer_index = (self.dealer_index + 1) % NUM_PLAYERS

        # current player is first after dealer
        # can not use old current, as it is set by trick winner see #score_trick
        self.current_player_index = (self.dealer_index + 1) % NUM_PLAYERS
        self.lead_index = self.current_player_index

        # Recompute the order, where the previous dealer is now the f
        for i in range(NUM_PLAYERS):
            self._order.append((self.current_player_index + i) % NUM_PLAYERS)

        self.__reset()

    def activate_next_player(self) -> Player:
        """
        Advance to the next player in the order (circularly) and return that player.

        Returns:
            Player: The player who is now active.
        """
        current_index = self._order.index(self.current_player_index)
        next_index = (current_index + 1) % len(self._order)
        self.current_player_index = self._order[next_index]
        return self.current_player

    @property
    def current_player(self) -> Player:
        """
        Retrieve the currently active player.

        Returns:
            Player: The player object for the current player.
        """
        return self.players[self.current_player_index]

    def get_player(self, index: int | str) -> Player:
        """
        Retrieve a player by playing order or name.

        Args:
            index (int): The index of the player in the list.

        Returns:
            Player: The player object at the given index.
        """

        if index is None:
            return None

        if isinstance(index, str):
            for player in self.players:
                if player.name == index:
                    return player
        else:
            return self.players[index]

    @property
    def maker(self) -> Player | None:
        """
        Retrieve the player who declared the trump suit (the maker).

        Returns:
            Optional[Player]: The player object representing the maker, or None if no trump suit is declared.
        """
        if self.maker_index is None:
            return None
        return self.players[self.maker_index]

    @property
    def first_player(self) -> Player:
        """
        Retrieve the player object for the first player (based on the current self.order).

        Returns:
            Player: The first player in the current order.
        """
        index = self._order[0]
        return self.players[index]

    @property
    def dealer(self) -> Player:
        """
        Retrieve the current dealer.

        Returns:
            Player: The dealer player object.
        """
        return self.players[self.dealer_index]

    def activate_dealer(self) -> None:
        """
        Make the dealer the current player.
        """
        self.current_player_index = self.dealer_index

    def activate_first_player(self) -> None:
        """
        Make the first player from the order the current player.
        """
        self.current_player_index = self._order[0]

    def reset_lead_player(self):
        self.lead_index = self.current_player_index

    def deal_cards(self) -> None:
        """
        Deal 5 cards to each player, then set the upCard from the top of the deck.
        """
        for _ in range(NUM_CARDS_PER_PLAYER):
            for player in self.players:
                card = self.deck.pop(0)
                player.hand.append(card)
        self._up_card = self.deck.pop(0)

    def go_alone(self) -> None:
        """
        Indicate that the current player goes alone, removing their partner from the play order.

        Raises:
            EuchreException: If trump is not set.
        """
        if self.trump is None:
            raise EuchreError("Trump must be made before going alone.")

        # Mark the current player as going alone
        self.current_player.alone = True
        partner_index = self.players.index(self.current_player.partner)
        self._order.remove(partner_index)

    def make_trump(self, suit: str) -> None:
        """
        Declare the trump suit.

        Args:
            suit (Optional[str]): The desired trump suit.

        Raises:
            EuchreException: Various conditions (mismatched downCard, missing upCard, etc.).
        """
        # Disallow trump if it matches the downCard's suit
        if self._down_card is not None and self._down_card._suit == suit:
            raise EuchreError("Trump can not match the down card.")

        self.maker_index = self.current_player_index
        self.trump = suit
        self.deck.trump = suit

    @property
    def is_trick_finished(self) -> bool:
        """
        Determine if the current trick has been completed
        (i.e., each remaining player in order has played).

        Raises:
            EuchreException: If there are no tricks yet.  Must call #add_trick

        Returns:
            bool: True if the current trick is complete, False otherwise.
        """
        if len(self._tricks) == 0:
            raise EuchreError("No tricks available.")

        return len(self._tricks[-1]) == len(self._order)

    def dealer_swap_card(self, card: Card) -> None:
        """
        Allow the dealer to swap one card from their hand with the upCard.

        Args:
            card (Card): The card to discard from the dealer's hand.

        Raises:
            EuchreException: If a discard is already set, or the card is not in the dealer's hand.
        """
        if self.discard is not None:
            raise EuchreError("Discard must be None to swap.")

        if card not in self.dealer.hand:
            raise EuchreError(f"Must swap card from hand: {card}")

        # Remove the given card, add the upCard to dealer's hand
        self.dealer.hand.remove(card)
        self.dealer.hand.append(self._up_card)
        self.discard = card
        # self.maker_index = self.dealer_index

    def turn_down_card(self) -> None:
        """
        Turn down the up card (pass on making trump if upCard is not desired).

        Raises:
            EuchreException: If a discard is already set.
        """
        if self.discard is not None:
            raise EuchreError("Discard must be None to turn down.")

        self._down_card = self._up_card
        self._up_card = None

    def play_card(self, card: Card) -> None:
        """
        Play a card from the current player's hand into the current trick.

        Args:
            card (Card): The card object or string representation of the card to be played.

        Raises:
            EuchreException: If trump isn't set, if the trick is finished, if the card isn't in the player's hand,
                             or if the suit cannot be followed.
        """
        if self.trump is None:
            raise EuchreError("Trump must be made before playing a card.")
        if self.is_trick_finished:
            raise EuchreError(f"Trick full, can't play card '{card}'.")

        # Convert string to Card if needed
        if isinstance(card, str):
            card = self.deck.get_card(card)

        player = self.current_player

        if card not in player.hand:
            raise EuchreError(f"Card '{card}' not in hand of '{player.name}'.")

        if card not in playable(self.current_trick, player.hand):
            lead_suit = self._tricks[-1].lead_suit
            raise EuchreError(f"Card '{card}' must follow suit '{lead_suit}'.")

        # Remove card from player's hand and move to played
        player.hand.remove(card)
        player.played.append(card)

        # Add to the current trick
        self._tricks[-1].append(card)

        # Advance to the next player
        self.activate_next_player()

    def score_trick(self) -> None:
        """
        Score the current (just-finished) trick:
          - Identify the winning card and its player.
          - Rotate self.order so the winner is first.
          - Increase the winner's trick count.

        Raises:
            EuchreException: If the trick is not yet finished.
        """
        if not self.is_trick_finished:
            raise EuchreError("Cannot score an unfinished trick.")

        # Determine the trick winner, update player data
        winner_pindex = self.current_trick.winner
        self.players[winner_pindex].tricks += 1

    def rotate_to_winner(self) -> None:
        winner_pindex = self.current_trick.winner

        # Move the winner to the front of the order
        rotate_to(self._order, winner_pindex)
        self.current_player_index = winner_pindex
        self.lead_index = winner_pindex

    @property
    def is_hand_finished(self) -> bool:
        """
        Check if the current hand is finished (i.e., 5 tricks played).

        Returns:
            bool: True if the hand is complete, False otherwise.
        """
        if len(self._tricks) < NUM_TRICKS_PER_HAND:
            return False
        return self.is_trick_finished

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

        maker_tricks = self.maker.team.tricks

        if maker_tricks == NUM_TRICKS_PER_HAND and self.maker.team.is_alone:
            self.maker.team.score = self.maker.team.score + 4
        elif maker_tricks == NUM_TRICKS_PER_HAND:
            self.maker.team.score = self.maker.team.score + 2
        elif maker_tricks >= REQUIRED_TRICKS_TO_WIN:
            self.maker.team.score = self.maker.team.score + 1
        else:
            for team in self._teams:
                if team != self.maker.team:
                    team.score = team.score + 2

    def calc_hand(self) -> int:
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

        maker_tricks = self.maker.team.tricks
        scores = {team: 0 for team in self._teams}

        if maker_tricks == NUM_TRICKS_PER_HAND and self.maker.team.is_alone:
            scores[self.maker.team] = 4
        elif maker_tricks == NUM_TRICKS_PER_HAND:
            scores[self.maker.team] = 2
        elif maker_tricks >= REQUIRED_TRICKS_TO_WIN:
            scores[self.maker.team] = 1
        else:
            for team in self._teams:
                if team != self.maker.team:
                    scores[team] = 2

        return scores

    def is_game_over(self) -> bool:
        """
        Determine if the game is over based on the current score.

        Args:`
            score (List[int]): A two-element list representing the team scores.

        Returns:
            bool: True if either team has reached or exceeded 10 points, otherwise False.
        """

        for team in self._teams:
            if team.score >= self.win_condition:
                return True
        return False

    def set_cards(self, player, cards):
        player = self.get_player(player)
        player.hand.clear()
        for card_string in cards:
            player.hand.append(self.deck.get_card(card_string))

    def __str__(self) -> str:  # pragma: no cover
        """
        String representation of the Euchre object, containing debug info.
        """
        sb = ""

        sb = sb + "players:\n"
        for player in self.players:
            sb = sb + "  " + str(player) + "\n"

        sb = sb + f"order: {self._order}" + "\n"
        sb = (
            sb + f"current: {self.current_player_index} -> {self.current_player}" + "\n"
        )
        sb = sb + f"dealer: {self.dealer_index} -> {self.dealer}" + "\n"
        sb = sb + f"hand count: {self.hand_count}" + "\n"
        sb = sb + f"up card: {self.up_card}" + "\n"
        sb = sb + f"down card: {self._down_card}" + "\n"
        sb = sb + f"discard: {self.discard}" + "\n"
        sb = sb + f"trump: {self.trump}" + "\n"
        sb = sb + f"maker: {self.maker_index} -> {self.maker}" + "\n"
        sb = sb + f"lead: {self.lead_index} -> {self.players[self.lead_index]}" + "\n"

        sb = sb + "tricks:\n"
        for trick in self.tricks:
            sb = sb + "  " + str(trick) + "\n"

        return sb

    def __json__(self):
        return {
            "players": self.players,
            "tricks": self.tricks,
            "deck": self.deck,
            "trump": self.trump,
            "order": self.order,
            "current_player": self.current_player_index,
            "dealer": self.dealer_index,
            "lead": self.lead_index,
            "maker": self.maker_index,
            "hand_count": self.hand_count,
            "up_card": self.up_card,
            "down_card": self.down_card,
            "discard": self.discard,
        }

__all__ = ["Euchre", "EuchreError"]
