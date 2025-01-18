from euchre.card.Card import Card

def test_equality_card_object_true():
    card0 = Card("♠", "10")
    card1 = Card("♠", "10")
    assert card0 == card1

def test_equality_card_object_false():
    card0 = Card("♠", "10")
    card1 = Card("♠", "9")
    assert card0 != card1

def test_equality_with_None():
    card0 = Card("♠", "10")
    assert card0 != None

def test_equality_with_string_true():
    card0 = Card("♠", "10")
    assert card0 == "10♠"

def test_equality_with_string_false():
    card0 = Card("♠", "10")
    assert card0 != "10♦"

def test_equality_with_not_card():
    card0 = Card("♠", "10")
    assert card0 != []

def test_suit_effective_eq():
    trump = '♦'
    card = Card('A♦')
    assert card.suit_effective(trump) == trump
    
def test_suit_effective_neq():
    trump = '♠'
    card = Card('A♦')
    assert card.suit_effective(trump) != trump

def test_suit_effective_rb():
    trump = '♠'
    card = Card('J♠')
    assert card.suit_effective(trump) == trump

def test_suit_effective_lb_1():
    trump = '♠'
    card = Card('J♣')
    assert card.suit_effective(trump) == trump

def test_suit_effective_lb_2():
    trump = '♣'
    card = Card('J♠')
    assert card.suit_effective(trump) == trump

def test_to_str():
    card = Card('J♣')
    assert str(card) == 'J♣'

def test_repr():
    card = Card('J♣')
    assert card.__repr__() == 'J♣'

def test_hash_equal():
    card1 = Card('J♣')
    card2 = Card('J♣')
    assert card1.__hash__() == card2.__hash__()

def test_hash_not_equal():
    card1 = Card('J♣')
    card2 = Card('J♠')
    assert card1.__hash__() != card2.__hash__()    

# Same card returns 1
def test_compare_same_card():
    card1 = Card('J♠')  # Right Bower (Trump Jack)
    assert card1.compare(card1, lead='♠', trump='♠') == 1  # Right Bower wins

# ✅ Right Bower (J of Trump) always wins
def test_compare_right_bower_vs_non_trump():
    card1 = Card('J♠')  # Right Bower (Trump Jack)
    card2 = Card('A♠')  # Non-trump Ace
    assert card1.compare(card2, lead='♠', trump='♠') == 1  # Right Bower wins

def test_compare_non_trump_vs_right_bower():
    card1 = Card('A♠')  # Non-trump Ace
    card2 = Card('J♠')  # Right Bower (Trump Jack)
    assert card1.compare(card2, lead='♠', trump='♠') == -1  # Right Bower wins

# ✅ Left Bower (J of same-color suit as trump) beats everything except Right Bower
def test_compare_left_bower_vs_non_trump():
    card1 = Card('J♣')  # Left Bower
    card2 = Card('A♠')  # Non-trump Ace
    assert card1.compare(card2, lead='♠', trump='♠') == 1  # Left Bower wins

def test_compare_non_trump_vs_left_bower():
    card1 = Card('A♠')  # Non-trump Ace
    card2 = Card('J♣')  # Left Bower
    assert card1.compare(card2, lead='♠', trump='♠') == -1  # Left Bower wins

def test_compare_left_bower_vs_right_bower():
    card1 = Card('J♣')  # Left Bower
    card2 = Card('J♠')  # Right Bower
    assert card1.compare(card2, lead='♠', trump='♠') == -1  # Right Bower wins

def test_compare_right_bower_vs_left_bower():
    card1 = Card('J♠')  # Right Bower
    card2 = Card('J♣')  # Left Bower
    assert card1.compare(card2, lead='♠', trump='♠') == 1  # Right Bower wins

# ✅ Any trump card beats any non-trump card
def test_compare_trump_vs_non_trump():
    card1 = Card('9♦')  # Trump suit
    card2 = Card('K♠')  # Non-trump
    assert card1.compare(card2, lead='♠', trump='♦') == 1  # Trump wins

def test_compare_non_trump_vs_trump():
    card1 = Card('K♠')  # Non-trump
    card2 = Card('9♦')  # Trump suit
    assert card1.compare(card2, lead='♠', trump='♦') == -1  # Trump wins

def test_compare_high_trump_vs_low_trump():
    card1 = Card('A♦')  # High trump
    card2 = Card('9♦')  # Low trump
    assert card1.compare(card2, lead='♠', trump='♦') == 1  # Higher trump wins

def test_compare_low_trump_vs_high_trump():
    card1 = Card('9♦')  # Low trump
    card2 = Card('A♦')  # High trump
    assert card1.compare(card2, lead='♠', trump='♦') == -1  # Higher trump wins

# ✅ Lead suit wins over a non-lead, non-trump card
def test_compare_lead_vs_non_lead():
    card1 = Card('10♠')  # Lead suit
    card2 = Card('K♦')   # Not lead, not trump
    assert card1.compare(card2, lead='♠', trump='♥') == 1  # Lead wins

def test_compare_non_lead_vs_lead():
    card1 = Card('K♦')   # Not lead, not trump
    card2 = Card('10♠')  # Lead suit
    assert card1.compare(card2, lead='♠', trump='♥') == -1  # Lead wins

# ✅ If both cards follow lead, highest wins
def test_compare_both_follow_lead():
    card1 = Card('K♠')  # Lead suit
    card2 = Card('10♠')  # Lower-ranked lead suit
    assert card1.compare(card2, lead='♠', trump='♦') == 1  # Higher card wins

def test_compare_both_follow_lead_low_vs_high():
    card1 = Card('10♠')  # Lower-ranked lead suit
    card2 = Card('K♠')  # Lead suit
    assert card1.compare(card2, lead='♠', trump='♦') == -1  # Higher card wins

# ✅ If neither follows suit and neither is trump, it's a tie (0)
def test_compare_both_off_suit_neither_trump():
    card1 = Card('Q♥')  # Off-suit, not lead or trump
    card2 = Card('10♣')  # Off-suit, not lead or trump
    assert card1.compare(card2, lead='♠', trump='♦') == 0  # Neither follows lead or is trump → Tie

def test_compare_both_off_suit_neither_trump_different_order():
    card1 = Card('10♣')  # Off-suit, not lead or trump
    card2 = Card('Q♥')  # Off-suit, not lead or trump
    assert card1.compare(card2, lead='♠', trump='♦') == 0  # Neither follows lead or is trump → Tie
