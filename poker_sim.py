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
    return random.randint(1, 100)  # Placeholder for a proper hand evaluation function

def simulate_win_probability(player_hand, opponents_hands, community_cards=None, num_simulations=1000):
    """Simulate win probabilities using Monte Carlo simulations."""
    if community_cards is None:
        community_cards = []
    hands = [player_hand] + opponents_hands
    win_counts = {i: 0 for i in range(len(hands))}

    for _ in range(num_simulations):
        deck = Deck()
        in_play = [card for hand in hands for card in hand] + community_cards
        deck.cards = [card for card in deck.cards if card not in in_play]
        deck.shuffle()

        remaining_cards = 5 - len(community_cards)
        sim_community_cards = community_cards + deck.deal(remaining_cards)

        final_hands = [hand + sim_community_cards for hand in hands]
        hand_ranks = [evaluate_hand(hand) for hand in final_hands]

        best_rank = max(hand_ranks)
        winners = [i for i, rank in enumerate(hand_ranks) if rank == best_rank]

        for winner in winners:
            win_counts[winner] += 1 / len(winners)

    win_probabilities = {i: (win_counts[i] / num_simulations) * 100 for i in range(len(hands))}
    return win_probabilities

def play_game(deck, player_hand, opponents_hands):
    community_cards = []
    stages = ["Flop", "Turn", "River"]
    win_probabilities = simulate_win_probability(player_hand, opponents_hands, community_cards)
    
    print("\nInitial Hands and Win Probabilities:")
    print(f"Player: {player_hand} - {win_probabilities[0]:.2f}%")
    for i, hand in enumerate(opponents_hands, start=1):
        print(f"Opponent {i}: {hand} - {win_probabilities[i]:.2f}%")

    for stage in stages:
        input(f"Press Enter to reveal the {stage}...")
        num_cards = 3 if stage == "Flop" else 1
        community_cards.extend(deck.deal(num_cards))
        print(f"{stage}: {community_cards}")
        win_probabilities = simulate_win_probability(player_hand, opponents_hands, community_cards)
        
        print("\nUpdated Hands and Win Probabilities:")
        print(f"Player: {player_hand} - {win_probabilities[0]:.2f}%")
        for i, hand in enumerate(opponents_hands, start=1):
            print(f"Opponent {i}: {hand} - {win_probabilities[i]:.2f}%")

def main():
    mode = input("Choose mode: (1) Simulation (2) Game: ")
    if mode not in ["1", "2"]:
        print("Invalid mode selected. Exiting.")
        return

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

    if mode == "1":
        win_probabilities = simulate_win_probability(player_hand, opponents_hands)
        print("\nInitial Hands and Win Probabilities:")
        print(f"Player: {player_hand} - {win_probabilities[0]:.2f}%")
        for i, hand in enumerate(opponents_hands, start=1):
            print(f"Opponent {i}: {hand} - {win_probabilities[i]:.2f}%")
    else:
        play_game(deck, player_hand, opponents_hands)

if __name__ == "__main__":
    main()
