from euchre.card.Trick import Trick
import pytest

def test_trick_initialization():
    """Test Trick initialization with a valid set of cards."""
    trick = Trick.build("♠", ["9♥", "K♥", "J♠", "9♣"], [0, 1, 2, 3])  # ✅ Corrected order

    assert trick.trump == "♠", "Trump suit should be ♠"
    assert trick.best_card == "J♠", "Best card should be the Right Bower J♠"
    assert trick.winner == 2, "Winner should be player 2 who played J♠"
    assert trick.lead_suit == "♥", "Lead suit should be ♥ from the first played card"

def test_trick_winner_no_cards():
    """Test winner() when no cards are played."""
    trick = Trick("♠")
    assert trick.winner is None, "Winner should be None if no cards are played"

def test_trick_winner_one_card():
    """Test that a single played card is automatically the winner."""
    trick = Trick("♠")
    trick.append(0, "A♠")

    assert trick.winner == 0, "Single player should be the winner"

def test_trick_append():
    """Test adding cards to a trick."""
    trick = Trick("♠")
    trick.append(0, "10♥")
    trick.append(1, "J♠")

    assert len(trick) == 2, "Trick should contain 2 cards after two plays"
    assert str(trick[0]) == "10♥", "First played card should be 10♥"
    assert str(trick[1]) == "J♠", "Second played card should be J♠"
    assert trick.trump == "♠", "Trump suit should be ♠"
    assert trick.best_card == "J♠", "Best card should be the Right Bower J♠"
    assert trick.winner == 1, "Winner should be player 2 who played J♠"
    assert trick.lead_suit == "♥", "Lead suit should be ♥ from the first played card"    

def test_trick_build_invalid_length():
    """Test Trick.build() raises an error when cards and order lists do not match."""
    with pytest.raises(Exception, match="Cards and order lists sizes must match."):
        Trick.build("♠", ["9♥", "K♥"], [0])  # Mismatch in sizes

def test_trick_best_card_with_mixed_trump():
    """Test best_card when trick contains trump and non-trump cards."""
    trick = Trick.build("♣", ["A♥", "K♣", "J♣", "9♠"], [0, 1, 2, 3])

    assert trick.best_card == "J♣", "Best card should be the Right Bower J♣"
    assert trick.winner == 2, "Winner should be player 2 who played J♣"
    assert trick.lead_suit == "♥", "Lead suit should be ♥ from the first played card"

def test_trick_winner_with_no_trump():
    """Test winner when no trump cards are played."""
    trick = Trick.build("♠", ["9♦", "Q♦", "K♦", "J♦"], [0, 1, 2, 3])

    assert trick.best_card == "K♦", "Best card should be the highest non-trump card"
    assert trick.winner == 2, "Winner should be player 3 who played J♦"
    assert trick.lead_suit == "♦", "Lead suit should be ♦ from the first played card"            

def test_trick_winner_with_left_bower():
    """Test winner when Left Bower is played in a trick."""
    trick = Trick.build("♣", ["A♠", "J♠", "K♣", "Q♣"], [0, 1, 2, 3])

    assert trick.best_card == "J♠", "Best card should be Left Bower J♠ (acts as ♣)"
    assert trick.winner == 1, "Winner should be player 1 who played J♠"
    assert trick.lead_suit == "♠", "Lead suit should be ♠ from the first played card"    

def test_trick_winner_with_only_one_card():
    """Test winner when only one card is played."""
    trick = Trick("♠")
    trick.append(0, "K♠")

    assert trick.winner == 0, "Single player should be the winner"
    assert trick.best_card == "K♠", "Best card should be K♠"
    assert trick.lead_suit == "♠", "Lead suit should be ♠ from the only card"    