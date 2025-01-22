from euchre.card import *
import pytest

def build_hand(cards, trump):     
    deck = Deck()
    deck.trump = trump
    hand = Hand()

    for card in cards:
        if isinstance(card, Card):
            hand.append(card)
        else:
            hand.append(deck.get_card(card))

    return (deck, hand)


@pytest.mark.parametrize("hand_cards, trump, phrase, expected", [
    (["9♠", "9♦", "A♣", "Q♥", "10♠"], "♠", "9 10", ["9♠", "9♦", "10♠"]),           # specified values, trump doesn't matter
    (["9♠", "9♦", "A♣", "Q♥", "10♠"], "♥", "9 10", ["9♠", "9♦", "10♠"]),           # specified values, trump doesn't matter
    (["9♠", "9♦", "A♣", "Q♥", "10♠"], "♠", "9 10 ♠", ["9♠", "10♠"]),               # specified 9 & 10 of trump ♠
    (["9♠", "9♥", "A♣", "Q♥", "10♥"], "♥", "9 10 ♠", ["9♥", "10♥"]),               # specified 9 & 10 of trump ♥    
    (["J♠", "9♦", "J♣", "Q♥", "10♣"], "♠", "J♣", ["J♣"]),                          # LB specifically
    (["J♠", "J♣", "J♦", "Q♥", "10♣"], "♥", "J♣", ["J♦"]),                          # LB specifically
    (["J♥", "J♣", "J♦", "Q♥", "10♣"], "♥", "J♠", ["J♥"]),                          # RB specifically
    (["9♠", "9♦", "A♣", "Q♥", "10♠"], "♠", "9♦ 10♠ Q♠", ["9♦", "10♠"]),            # specific cards only
    (["9♣", "10♦", "A♣", "Q♥", "10♠"], "♦", "9♦ 10♠ Q♠", ["9♣", "10♦"]),           # specific cards only ♦ -> ♣
    (["9♠", "9♦", "A♣", "Q♥", "10♠"], "♠", "♠", ["9♠", "10♠"]),                    # any trump ♠
    (["9♠", "9♦", "A♣", "Q♥", "10♠"], "♥", "♠", ["Q♥"]),                           # any trump ♥
    (["9♠", "A♦", "A♥", "Q♥", "10♠"], "♠", "♠ A♥ A♦", ["9♠", "A♦", "A♥", "10♠"]),  # any trump ♥ or opp ace
])
def test_query(hand_cards, trump, phrase, expected):
    (deck, hand) = build_hand(hand_cards, trump)
    q = Query(trump, hand, phrase).select()
    assert set(expected) == set(q)