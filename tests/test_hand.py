def test_card_list(this):
        hand = Hand(['Q♣', '10♥', '10♠', 'Q♥', 'K♦'])
        this.assertEqual(5, len(hand))
        this.assertTrue(isinstance(hand[0], Card))

    def test_empty_card_list(this):
        hand = Hand()
        this.assertEqual(0, len(hand))

    def test_get_random_card(this):
        hand = Hand(['Q♣', '10♥', '10♠', 'Q♥', 'K♦'])
        item = hand.randomItem()
        this.assertTrue(item in hand)

    def test_get_random_card_empty(this):
        hand = Hand()
        item = hand.randomItem()
        this.assertEqual(item, None)

    def test_can_play0(this):
        hand = Hand(['Q♣', '10♥', '10♠', 'Q♥', 'K♦'])
        trick = Trick(trump = '♥')
        card = Card('Q♣')

        actual = trick.can_play(card)
        this.assertEqual(actual, True)

    def test_can_play_left_bower_must_follow_suit(this):
        hand = Hand(['J♥', '10♥', '10♣', 'Q♥', 'K♦'])
        trump = '♦'
        trick = Trick(['9♦'])
        card = Card('J♥')

        actual = trick.can_play(card)
        this.assertEqual(actual, True)

def test_cant_play_left_bower_must_follow_suit(this):
        trick = Trick(trump = '♦')
        trick.append(pIndex = 0, card = '9♥')
        card = Card('J♥')

        actual = trick.can_play(card)
        this.assertEqual(actual, False)

    def test_playable_empty_trick(this):
        hand = Hand(['Q♣', '10♥', '10♠', 'Q♥', 'K♦'])
        trick = Trick('♥')

        cards = hand.playable_cards(trick)
        this.assertEqual(len(cards), 5)

    def test_playable_mid_trick_only_bower(this):
        hand = Hand(['A♥','K♦','J♠','A♠','Q♥'])
        trick = Trick(trump = '♣')
        trick.append(pIndex = 0, card = 'Q♣')
        trick.append(pIndex = 1, card = 'A♣')        

        playable = hand.playable_cards(trick)
        this.assertEqual(len(playable), 1)
        this.assertTrue(Card('J♠') in playable)        