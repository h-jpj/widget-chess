#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game state management for Widget Chess.
Handles saving and loading game state to/from JSON.
"""

import os
import json
import time
import chess
from datetime import datetime

import config
from encryption import encrypt_data, decrypt_data

class GameState:
    """Manages the chess game state and persistence."""
    
    def __init__(self):
        """Initialize the game state."""
        self.board = chess.Board()
        self.move_history = []
        self.last_move = None
        self.last_save_time = None
        self.game_id = None
        self.white_player = "Player 1"
        self.black_player = "Player 2"
        self.game_start_time = datetime.now().isoformat()
        
    def make_move(self, move):
        """Make a move on the board and update the game state.
        
        Args:
            move: A chess.Move object
            
        Returns:
            bool: True if the move was successful, False otherwise
        """
        if move in self.board.legal_moves:
            # Record move in standard algebraic notation
            san_move = self.board.san(move)
            
            # Make the move
            self.board.push(move)
            
            # Update move history
            move_info = {
                "move": san_move,
                "uci": move.uci(),
                "timestamp": datetime.now().isoformat(),
                "fen": self.board.fen(),
                "turn": "black" if self.board.turn == chess.BLACK else "white"
            }
            self.move_history.append(move_info)
            self.last_move = move
            
            # Auto-save if enabled
            if config.SETTINGS.get("auto_save", True):
                self.save_game()
                
            return True
        return False
    
    def to_dict(self):
        """Convert the game state to a dictionary for serialization."""
        return {
            "game_id": self.game_id or datetime.now().strftime("%Y%m%d%H%M%S"),
            "fen": self.board.fen(),
            "move_history": self.move_history,
            "white_player": self.white_player,
            "black_player": self.black_player,
            "game_start_time": self.game_start_time,
            "last_save_time": datetime.now().isoformat()
        }
    
    def from_dict(self, data):
        """Load the game state from a dictionary.
        
        Args:
            data: Dictionary containing game state
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.game_id = data.get("game_id")
            self.board = chess.Board(data.get("fen"))
            self.move_history = data.get("move_history", [])
            self.white_player = data.get("white_player", "Player 1")
            self.black_player = data.get("black_player", "Player 2")
            self.game_start_time = data.get("game_start_time", datetime.now().isoformat())
            self.last_save_time = data.get("last_save_time")
            
            # Set last move if there's move history
            if self.move_history:
                last_move_uci = self.move_history[-1]["uci"]
                self.last_move = chess.Move.from_uci(last_move_uci)
            
            return True
        except Exception as e:
            print(f"Error loading game state: {e}")
            return False
    
    def save_game(self):
        """Save the current game state to a JSON file."""
        try:
            # Create config directory if it doesn't exist
            os.makedirs(os.path.dirname(config.SAVE_FILE), exist_ok=True)
            
            # Convert game state to dictionary
            game_data = self.to_dict()
            
            # Encrypt the data
            encrypted_data = encrypt_data(json.dumps(game_data))
            
            # Save to file
            with open(config.SAVE_FILE, 'w') as f:
                json.dump(encrypted_data, f, indent=4)
                
            self.last_save_time = datetime.now().isoformat()
            return True
        except Exception as e:
            print(f"Error saving game: {e}")
            return False
    
    def load_game(self):
        """Load a game state from a JSON file.
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not os.path.exists(config.SAVE_FILE):
            return False
        
        try:
            with open(config.SAVE_FILE, 'r') as f:
                encrypted_data = json.load(f)
            
            # Decrypt the data
            decrypted_data = decrypt_data(encrypted_data)
            game_data = json.loads(decrypted_data)
            
            # Load the game state
            return self.from_dict(game_data)
        except Exception as e:
            print(f"Error loading game: {e}")
            return False
    
    def new_game(self):
        """Start a new game."""
        self.board = chess.Board()
        self.move_history = []
        self.last_move = None
        self.game_id = datetime.now().strftime("%Y%m%d%H%M%S")
        self.game_start_time = datetime.now().isoformat()
        
        # Auto-save if enabled
        if config.SETTINGS.get("auto_save", True):
            self.save_game()
    
    def get_current_turn(self):
        """Get the current player's turn.
        
        Returns:
            str: 'white' or 'black'
        """
        return "white" if self.board.turn == chess.WHITE else "black"
    
    def is_game_over(self):
        """Check if the game is over.
        
        Returns:
            bool: True if the game is over, False otherwise
        """
        return self.board.is_game_over()
    
    def get_game_result(self):
        """Get the result of the game.
        
        Returns:
            str: Game result (1-0, 0-1, 1/2-1/2, or *)
        """
        if not self.is_game_over():
            return "*"
        return self.board.result()
