import timeit
from euchre.card.Card import Card

# List Comprehension Approach
def init_deck_list_comprehension():
    return [Card(suit, value) for suit in Card.suits for value in Card.values]

# For-Loop Approach
def init_deck_for_loop():
    deck = []
    for suit in Card.suits:
        for value in Card.values:
            deck.append(Card(suit, value))
    return deck

# Timing the Performance
if __name__ == "__main__":
    num_trials = 1000000  # Run each method multiple times to get an accurate comparison

    list_comprehension_time = timeit.timeit(init_deck_list_comprehension, number=num_trials)
    for_loop_time = timeit.timeit(init_deck_for_loop, number=num_trials)

    print(f"List Comprehension Time: {list_comprehension_time:.5f} seconds")
    print(f"For Loop Time: {for_loop_time:.5f} seconds")

    speedup = for_loop_time / list_comprehension_time
    print(f"List comprehension is ~{speedup:.2f}x faster than the for-loop.")
