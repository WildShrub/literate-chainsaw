#!/usr/bin/env python3
"""
Tic Tac Toe Game
A simple command-line implementation of the classic Tic Tac Toe game.
"""


class TicTacToe:
    def __init__(self):
        """Initialize the game board and state."""
        self.board = [' ' for _ in range(9)]
        self.current_player = 'X'
        self.game_over = False
        self.winner = None

    def print_board(self):
        """Display the current game board."""
        print("\n")
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]} ")
        print("---|---|---")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]} ")
        print("---|---|---")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]} ")
        print("\n")

    def print_positions(self):
        """Display position numbers for player reference."""
        print("Position numbers:")
        print(" 0 | 1 | 2 ")
        print("---|---|---")
        print(" 3 | 4 | 5 ")
        print("---|---|---")
        print(" 6 | 7 | 8 ")
        print()

    def is_winner(self, player):
        """Check if the specified player has won."""
        winning_combinations = [
            [0, 1, 2],
            [3, 4, 5],
            [6, 7, 8],
            [0, 3, 6],
            [1, 4, 7],
            [2, 5, 8],
            [0, 4, 8],
            [2, 4, 6]
        ]
        for combo in winning_combinations:
            if all(self.board[i] == player for i in combo):
                return True
        return False

    def is_board_full(self):
        """Check if the board is full."""
        return ' ' not in self.board

    def make_move(self, position):
        """
        Make a move at the specified position.
        Returns True if the move was valid, False otherwise.
        """
        if not isinstance(position, int) or position < 0 or position > 8:
            print("Invalid input! Please enter a number between 0 and 8.")
            return False

        if self.board[position] != ' ':
            print("That position is already taken!")
            return False

        self.board[position] = self.current_player
        return True

    def switch_player(self):
        """Switch to the other player."""
        self.current_player = 'O' if self.current_player == 'X' else 'X'

    def check_game_state(self):
        """Check if the game is over and set the winner or draw status."""
        if self.is_winner(self.current_player):
            self.game_over = True
            self.winner = self.current_player
            return True

        if self.is_board_full():
            self.game_over = True
            self.winner = 'Draw'
            return True

        return False

    def play(self):
        """Main game loop."""
        print("=" * 30)
        print("Welcome to Tic Tac Toe!")
        print("=" * 30)
        self.print_positions()

        while not self.game_over:
            self.print_board()
            print(f"Player {self.current_player}'s turn")

            while True:
                try:
                    position = int(input("Enter position (0-8): "))
                    if self.make_move(position):
                        break
                except ValueError:
                    print("Invalid input! Please enter a number between 0 and 8.")

            if self.check_game_state():
                self.print_board()
                if self.winner == 'Draw':
                    print("=" * 30)
                    print("It's a Draw! Game Over.")
                    print("=" * 30)
                else:
                    print("=" * 30)
                    print(f"Player {self.winner} Wins! Congratulations!")
                    print("=" * 30)
                break

            self.switch_player()

    def play_again(self):
        """Ask if players want to play again."""
        while True:
            choice = input("\nDo you want to play again? (yes/no): ").lower()
            if choice in ['yes', 'y']:
                return True
            elif choice in ['no', 'n']:
                return False
            else:
                print("Please enter 'yes' or 'no'.")


def main():
    """Main entry point."""
    while True:
        game = TicTacToe()
        game.play()

        if not game.play_again():
            print("\nThanks for playing! Goodbye!")
            break


if __name__ == "__main__":
    main()
