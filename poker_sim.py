import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return f"{self.rank}{self.suit}"

class Deck:
    def __init__(self):
        suits = ['♠', '♥', '♦', '♣']  # Spades, Hearts, Diamonds, Clubs
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self, num_cards):
        if num_cards > len(self.cards):
            raise ValueError("Not enough cards left to deal.")
        dealt_cards = self.cards[:num_cards]
        self.cards = self.cards[num_cards:]
        return dealt_cards

def evaluate_hand(hand):
    """Evaluate the strength of a poker hand."""
    rank_order = {str(i): i for i in range(2, 11)}
    rank_order.update({"J": 11, "Q": 12, "K": 13, "A": 14})

    # Sort cards by rank
    sorted_hand = sorted(hand, key=lambda card: rank_order[card.rank], reverse=True)

    # Count occurrences of each rank
    rank_counts = {}
    for card in hand:
        rank_counts[card.rank] = rank_counts.get(card.rank, 0) + 1

    counts = list(rank_counts.values())
    is_flush = len(set(card.suit for card in hand)) == 1
    is_straight = (
        len(rank_counts) == len(hand) and 
        rank_order[sorted_hand[0].rank] - rank_order[sorted_hand[-1].rank] == len(hand) - 1
    )

    if is_straight and is_flush:
        return "Straight Flush"
    elif 4 in counts:
        return "Four of a Kind"
    elif 3 in counts and 2 in counts:
        return "Full House"
    elif is_flush:
        return "Flush"
    elif is_straight:
        return "Straight"
    elif 3 in counts:
        return "Three of a Kind"
    elif counts.count(2) == 2:
        return "Two Pair"
    elif 2 in counts:
        return "One Pair"
    else:
        return "High Card"

def simulate_win_probability(player_hand, opponents_hands, num_simulations=1000):
    """Simulate win probabilities using Monte Carlo simulations."""
    hands = [player_hand] + opponents_hands
    win_counts = {i: 0 for i in range(len(hands))}

    for _ in range(num_simulations):
        deck = Deck()
        in_play = [card for hand in hands for card in hand]
        deck.cards = [card for card in deck.cards if card not in in_play]
        deck.shuffle()

        try:
            community_cards = deck.deal(5)
        except ValueError:
            continue

        final_hands = [hand + community_cards for hand in hands]
        hand_ranks = [evaluate_hand(hand) for hand in final_hands]

        best_rank = max(hand_ranks)
        winners = [i for i, rank in enumerate(hand_ranks) if rank == best_rank]

        for winner in winners:
            win_counts[winner] += 1 / len(winners)

    win_probabilities = {i: (win_counts[i] / num_simulations) * 100 for i in range(len(hands))}
    return win_probabilities

def main():
    while True:
        try:
            num_opponents = int(input("Enter the number of opponents (1-8): "))
            if 1 <= num_opponents <= 8:
                break
            else:
                print("Please enter a number between 1 and 8.")
        except ValueError:
            print("Invalid input. Please enter a number between 1 and 8.")

    deck = Deck()
    deck.shuffle()

    player_hand = deck.deal(2)
    opponents_hands = [deck.deal(2) for _ in range(num_opponents)]

    print("\nInitial Hands:")
    print("Player: ", player_hand)
    for i, hand in enumerate(opponents_hands, start=1):
        print(f"Opponent {i}: {hand}")

    win_probabilities = simulate_win_probability(player_hand, opponents_hands)
    print("\nWin Probabilities:")
    print(f"Player: {win_probabilities[0]:.2f}%")
    for i in range(1, num_opponents + 1):
        print(f"Opponent {i}: {win_probabilities[i]:.2f}%")

if __name__ == "__main__":
    main()
