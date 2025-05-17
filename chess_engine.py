#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chess engine module for Widget Chess.
Provides an interface to the python-chess library.
"""

import chess
import config
from game_state import GameState

class ChessEngine:
    """Interface to the python-chess library."""

    def __init__(self):
        """Initialize the chess engine."""
        self.game_state = GameState()

    def get_board(self):
        """Get the current chess board.

        Returns:
            chess.Board: The current board
        """
        return self.game_state.board

    def get_legal_moves(self):
        """Get all legal moves for the current position.

        Returns:
            list: List of legal moves as chess.Move objects
        """
        return list(self.game_state.board.legal_moves)

    def get_legal_moves_for_square(self, square):
        """Get all legal moves for a specific square.

        Args:
            square: Chess square (0-63) or string (e.g., 'e2')

        Returns:
            list: List of legal moves as chess.Move objects
        """
        if isinstance(square, str):
            square = chess.parse_square(square)

        moves = []
        for move in self.game_state.board.legal_moves:
            if move.from_square == square:
                moves.append(move)

        return moves

    def make_move(self, move):
        """Make a move on the board.

        Args:
            move: A chess.Move object or UCI string (e.g., 'e2e4')

        Returns:
            bool: True if the move was successful, False otherwise
        """
        if isinstance(move, str):
            try:
                move = chess.Move.from_uci(move)
            except ValueError:
                return False

        return self.game_state.make_move(move)

    def make_move_from_squares(self, from_square, to_square, promotion=None):
        """Make a move from a source square to a destination square.

        Args:
            from_square: Source square (0-63) or string (e.g., 'e2')
            to_square: Destination square (0-63) or string (e.g., 'e4')
            promotion: Piece type for promotion (optional)

        Returns:
            bool: True if the move was successful, False otherwise
        """
        if isinstance(from_square, str):
            from_square = chess.parse_square(from_square)
        if isinstance(to_square, str):
            to_square = chess.parse_square(to_square)

        move = chess.Move(from_square, to_square, promotion)
        return self.game_state.make_move(move)

    def is_game_over(self):
        """Check if the game is over.

        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.game_state.is_game_over()

    def get_game_result(self):
        """Get the result of the game.

        Returns:
            str: Game result (1-0, 0-1, 1/2-1/2, or *)
        """
        return self.game_state.get_game_result()

    def get_current_turn(self):
        """Get the current player's turn.

        Returns:
            str: 'white' or 'black'
        """
        return self.game_state.get_current_turn()

    def get_piece_at(self, square):
        """Get the piece at a specific square.

        Args:
            square: Chess square (0-63) or string (e.g., 'e2')

        Returns:
            chess.Piece or None: The piece at the square, or None if empty
        """
        if isinstance(square, str):
            square = chess.parse_square(square)

        return self.game_state.board.piece_at(square)

    def get_piece_color(self, square):
        """Get the color of the piece at a specific square.

        Args:
            square: Chess square (0-63) or string (e.g., 'e2')

        Returns:
            bool or None: True for white, False for black, None if empty
        """
        piece = self.get_piece_at(square)
        if piece:
            return piece.color
        return None

    def get_piece_type(self, square):
        """Get the type of the piece at a specific square.

        Args:
            square: Chess square (0-63) or string (e.g., 'e2')

        Returns:
            int or None: Piece type (1-6) or None if empty
        """
        piece = self.get_piece_at(square)
        if piece:
            return piece.piece_type
        return None

    def get_piece_symbol(self, square):
        """Get the symbol of the piece at a specific square.

        Args:
            square: Chess square (0-63) or string (e.g., 'e2')

        Returns:
            str or None: Piece symbol (P, N, B, R, Q, K, p, n, b, r, q, k) or None if empty
        """
        piece = self.get_piece_at(square)
        if piece:
            return piece.symbol()
        return None

    def get_fen(self):
        """Get the FEN string for the current position.

        Returns:
            str: FEN string
        """
        return self.game_state.board.fen()

    def set_fen(self, fen):
        """Set the board position from a FEN string.

        Args:
            fen: FEN string

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.game_state.board.set_fen(fen)
            return True
        except ValueError:
            return False

    def new_game(self):
        """Start a new game."""
        self.game_state.new_game()

    def save_game(self):
        """Save the current game state."""
        return self.game_state.save_game()

    def load_game(self):
        """Load a saved game state.

        Returns:
            bool: True if successful, False otherwise
        """
        return self.game_state.load_game()

    def get_move_history(self):
        """Get the move history.

        Returns:
            list: List of move information dictionaries
        """
        return self.game_state.move_history

    def get_last_move(self):
        """Get the last move made.

        Returns:
            chess.Move or None: The last move, or None if no moves have been made
        """
        return self.game_state.last_move

    def is_in_check(self):
        """Check if the current player is in check.

        Returns:
            bool: True if the current player is in check, False otherwise
        """
        return self.game_state.board.is_check()

    def is_in_checkmate(self):
        """Check if the current player is in checkmate.

        Returns:
            bool: True if the current player is in checkmate, False otherwise
        """
        return self.game_state.board.is_checkmate()

    def reset_board(self):
        """Reset the board to the starting position without creating a new game."""
        self.game_state.board = chess.Board()
        self.game_state.move_history = []
        self.game_state.last_move = None

        # Auto-save if enabled
        if config.SETTINGS.get("auto_save", True):
            self.game_state.save_game()

        return True
