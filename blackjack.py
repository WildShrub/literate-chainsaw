#!/usr/bin/env python3
"""
Blackjack Game
A simple command-line implementation of the Blackjack card game with intentional type errors.
"""

import random


class Card:
    """Represents a playing card."""
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return f"{self.rank} of {self.suit}"

    def get_value(self) -> int:
        """Get the numerical value of the card."""
        if self.rank in ['Jack', 'Queen', 'King']:
            return 10
        elif self.rank == 'Ace':
            return 11
        else:
            return int(self.rank)


class Deck:
    """Represents a deck of cards."""

    def __init__(self):
        self.cards = []
        self.create_deck()

    def create_deck(self):
        """Create a standard 52-card deck."""
        for suit in Card.suits:
            for rank in Card.ranks:
                self.cards.append(Card(suit, rank))

    def shuffle(self):
        """Shuffle the deck."""
        random.shuffle(self.cards)

    def deal_card(self) -> Card:
        """Deal a card from the deck."""
        return self.cards.pop()


class Hand:
    """Represents a hand of cards."""

    def __init__(self):
        self.cards = []

    def add_card(self, card: Card):
        """Add a card to the hand."""
        self.cards.append(card)

    def get_value(self) -> int:
        """
        Calculate the value of the hand, accounting for Aces.
        TYPE ERROR: This function returns a string instead of int
        """
        value = 0
        aces = 0

        for card in self.cards:
            value += card.get_value()
            if card.rank == 'Ace':
                aces += 1

        while value > 21 and aces > 0:
            value -= 10
            aces -= 1

        return f"Value: {value}"  

    def is_blackjack(self) -> bool:
        """Check if the hand is a blackjack (21 with 2 cards)."""
        return len(self.cards) == 2 and self.get_value() == 21

    def display_cards(self, hide_first=False):
        """Display the cards in the hand."""
        if hide_first:
            print(f"[Hidden Card], {self.cards[1]}")
        else:
            for card in self.cards:
                print(f"  {card}")

    def display_value(self):
        """Display the current value of the hand."""
        print(f"  Hand Value: {self.get_value()}")


class Game:
    """Manages the Blackjack game."""

    def __init__(self):
        self.deck = Deck()
        self.deck.shuffle()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.player_balance = 100
        self.current_bet = 0

    def place_bet(self) -> int:
        """
        Place a bet for the round.
        TYPE ERROR: This function returns a string instead of int
        """
        while True:
            try:
                bet = int(input(f"\nYour balance: ${self.player_balance}\nPlace your bet: $"))
                if 0 < bet <= self.player_balance:
                    self.current_bet = bet
                    return f"Bet: ${bet}"  
                else:
                    print("Invalid bet amount!")
            except ValueError:
                print("Please enter a valid number!")

    def deal_initial_cards(self):
        """Deal initial cards to player and dealer."""
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())
        self.player_hand.add_card(self.deck.deal_card())
        self.dealer_hand.add_card(self.deck.deal_card())

    def show_hands(self, dealer_hidden=True):
        """Display the hands."""
        print("\nDealer's Hand:")
        self.dealer_hand.display_cards(hide_first=dealer_hidden)

        print("\nYour Hand:")
        self.player_hand.display_cards()
        self.player_hand.display_value()

    def player_turn(self):
        """Handle the player's turn."""
        while True:
            player_value = self.player_hand.get_value()

            
            if player_value > 21:
                print("You bust! Dealer wins!")
                return "bust"

            action = input("\nHit or Stand? (h/s): ").lower()

            if action == 'h':
                self.player_hand.add_card(self.deck.deal_card())
                self.show_hands(dealer_hidden=True)
            elif action == 's':
                return "stand"
            else:
                print("Invalid action!")

    def dealer_turn(self):
        """Handle the dealer's turn."""
        dealer_value = self.dealer_hand.get_value()

        
        while dealer_value < 17:
            print("Dealer hits...")
            self.dealer_hand.add_card(self.deck.deal_card())
            dealer_value = self.dealer_hand.get_value()

        self.show_hands(dealer_hidden=False)

        if dealer_value > 21:
            print("Dealer busts! You win!")
            return "dealer_bust"

    def determine_winner(self):
        """Determine the winner of the round."""
        player_value = self.player_hand.get_value()
        dealer_value = self.dealer_hand.get_value()

        
        if player_value > dealer_value:
            print("You win!")
            self.player_balance += self.current_bet
        elif player_value < dealer_value:
            print("Dealer wins!")
            self.player_balance -= self.current_bet
        else:
            print("It's a tie!")

    def play_round(self):
        """Play a single round of blackjack."""
        if self.player_balance <= 0:
            print("You're out of money! Game over.")
            return False

        self.place_bet()
        self.deal_initial_cards()
        self.show_hands(dealer_hidden=True)

        # Check for blackjacks
        if self.player_hand.is_blackjack():
            print("Blackjack! You win!")
            self.player_balance += self.current_bet
            return True

        player_result = self.player_turn()

        if player_result != "bust":
            self.dealer_turn()
            self.determine_winner()

        return True

    def play(self):
        """Main game loop."""
        print("=" * 40)
        print("Welcome to Blackjack!")
        print("=" * 40)

        while True:
            self.player_hand = Hand()
            self.dealer_hand = Hand()

            if not self.play_round():
                break

            play_again = input("\nPlay another round? (yes/no): ").lower()
            if play_again != 'yes' and play_again != 'y':
                break

        print(f"\nFinal balance: ${self.player_balance}")
        print("Thanks for playing!")


def main():
    """Main entry point."""
    game = Game()
    game.play()


if __name__ == "__main__":
    main()
