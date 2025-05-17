#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chess widget for Widget Chess.
Provides a translucent chess board widget with piece movement.
"""

import os
import chess
from PyQt6.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QGraphicsDropShadowEffect, QSizePolicy, QFrame,
    QMessageBox, QPushButton
)
from PyQt6.QtCore import Qt, QSize, QPoint, QRect, pyqtSignal, QTimer
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QBrush, QPen,
    QFont, QRadialGradient, QPainterPath
)

import config
from chess_engine import ChessEngine
from move_log import MoveLogWidget
from connection_panel import ConnectionPanel

class ChessWidget(QWidget):
    """Translucent chess board widget."""

    # Signals
    move_made = pyqtSignal(chess.Move)
    game_over = pyqtSignal(str)  # Game result
    connection_status_changed = pyqtSignal(bool, str)  # Connected, peer name

    def __init__(self, parent=None):
        """Initialize the chess widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Set up the widget
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Initialize the chess engine
        self.engine = ChessEngine()

        # Set up the widget size
        self.square_size = config.SQUARE_SIZE
        self.board_size = config.BOARD_SIZE
        self.setMinimumSize(self.board_size, self.board_size)

        # Create the layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)

        # Create the board container
        self.board_container = QWidget()
        self.board_container.setFixedSize(self.board_size, self.board_size)
        self.board_container.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create the turn indicator
        self.turn_indicator = QLabel()
        self.turn_indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial")
        font.setPointSize(14)
        font.setWeight(QFont.Weight.Bold)
        self.turn_indicator.setFont(font)
        self.turn_indicator.setStyleSheet("color: white;")
        self.turn_indicator.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # Add glow effect to turn indicator
        self.glow_effect = QGraphicsDropShadowEffect()
        self.glow_effect.setBlurRadius(config.GLOW_RADIUS)
        self.glow_effect.setOffset(0, 0)
        self.turn_indicator.setGraphicsEffect(self.glow_effect)

        # Create the connection panel
        self.connection_panel = ConnectionPanel()
        self.connection_panel.connection_requested.connect(self.on_connection_requested)

        # Create the move log
        self.move_log = MoveLogWidget()

        # Create the main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(10)

        # Create the reset button (initially hidden)
        self.reset_button = QPushButton("Reset Game")
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
            QPushButton:pressed {
                background-color: #a93226;
            }
        """)
        self.reset_button.clicked.connect(self.reset_all)
        self.reset_button.setVisible(False)  # Hide initially

        # Create the board layout
        board_layout = QVBoxLayout()
        board_layout.setContentsMargins(0, 0, 0, 0)
        board_layout.setSpacing(10)
        board_layout.addWidget(self.turn_indicator)
        board_layout.addWidget(self.board_container)
        board_layout.addWidget(self.reset_button)

        # Create the right side layout
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.setSpacing(10)

        # Add connection panel
        right_layout.addWidget(self.connection_panel)

        # Add a separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #555555;")
        right_layout.addWidget(separator)

        # Add move log
        right_layout.addWidget(self.move_log)

        # Set stretch factors to make move log take more space
        right_layout.setStretchFactor(self.connection_panel, 1)
        right_layout.setStretchFactor(self.move_log, 3)

        # Add layouts to the main layout
        main_layout.addLayout(board_layout)
        main_layout.addLayout(right_layout)

        # Add the main layout to the widget
        self.layout.addLayout(main_layout)

        # Network connection status
        self.connected = False
        self.peer_name = None

        # Initialize variables
        self.selected_square = None
        self.highlighted_squares = []
        self.dragging = False
        self.drag_piece = None
        self.drag_start_pos = None
        self.drag_current_pos = None

        # Load the game state
        self.load_game()

        # Set up the glow animation timer
        self.glow_timer = QTimer(self)
        self.glow_timer.timeout.connect(self.update_glow)
        self.glow_timer.start(50)  # Update every 50ms
        self.glow_intensity = 0
        self.glow_increasing = True

    def load_game(self):
        """Load the game state."""
        # Try to load a saved game
        if not self.engine.load_game():
            # If no saved game, start a new one
            self.engine.new_game()

        # Update the move log
        self.move_log.update_moves(self.engine.get_move_history())

        # Update the turn indicator
        self.update_turn_indicator()

        # Repaint the board
        self.update()

    def save_game(self):
        """Save the game state."""
        self.engine.save_game()

    def update_turn_indicator(self):
        """Update the turn indicator based on the current turn, check, and checkmate status."""
        current_turn = self.engine.get_current_turn()

        if self.engine.is_game_over():
            result = self.engine.get_game_result()
            if result == "1-0":
                self.turn_indicator.setText("GAME OVER - WHITE WINS")
                self.turn_indicator.setStyleSheet("color: white; font-weight: bold;")
                self.glow_effect.setColor(QColor(255, 255, 255, 150))
                # Show reset button for game over
                self.show_reset_button()
            elif result == "0-1":
                self.turn_indicator.setText("GAME OVER - BLACK WINS")
                self.turn_indicator.setStyleSheet("color: white; font-weight: bold;")
                self.glow_effect.setColor(QColor(0, 0, 0, 150))
                # Show reset button for game over
                self.show_reset_button()
            else:
                self.turn_indicator.setText("GAME OVER - DRAW")
                self.turn_indicator.setStyleSheet("color: white; font-weight: bold;")
                self.glow_effect.setColor(QColor(150, 150, 150, 150))
                # Show reset button for game over
                self.show_reset_button()
        elif self.engine.is_in_checkmate():
            # Checkmate state
            indicator_key = f"{current_turn}_checkmate"
            self.turn_indicator.setText(config.TURN_INDICATOR_TEXT[indicator_key])
            self.turn_indicator.setStyleSheet(f"color: {config.TURN_INDICATOR_COLORS['checkmate']}; font-weight: bold;")
            self.glow_effect.setColor(QColor(config.GLOW_COLOR["checkmate"]))
            self.glow_effect.setBlurRadius(config.GLOW_RADIUS_CHECKMATE)

            # Show the reset button when checkmate occurs
            self.show_reset_button()
        elif self.engine.is_in_check():
            # Check state
            indicator_key = f"{current_turn}_check"
            self.turn_indicator.setText(config.TURN_INDICATOR_TEXT[indicator_key])
            self.turn_indicator.setStyleSheet(f"color: {config.TURN_INDICATOR_COLORS['check']}; font-weight: bold;")
            self.glow_effect.setColor(QColor(config.GLOW_COLOR["check"]))
            self.glow_effect.setBlurRadius(config.GLOW_RADIUS_CHECK)
        else:
            # Normal turn
            self.turn_indicator.setText(config.TURN_INDICATOR_TEXT[current_turn])
            self.turn_indicator.setStyleSheet("color: white;")
            glow_color = QColor(config.GLOW_COLOR[current_turn])
            self.glow_effect.setColor(glow_color)
            self.glow_effect.setBlurRadius(config.GLOW_RADIUS)

            # Hide the reset button if visible
            self.hide_reset_button()

    def update_glow(self):
        """Update the glow effect animation."""
        if self.glow_increasing:
            self.glow_intensity += 5
            if self.glow_intensity >= 100:
                self.glow_intensity = 100
                self.glow_increasing = False
        else:
            self.glow_intensity -= 5
            if self.glow_intensity <= 30:
                self.glow_intensity = 30
                self.glow_increasing = True

        # Update the glow effect
        self.glow_effect.setBlurRadius(config.GLOW_RADIUS * (self.glow_intensity / 100))

        # Only update the turn indicator, not the whole widget
        self.turn_indicator.update()

    def paintEvent(self, event):
        """Paint the chess board and pieces."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw the board
        self.draw_board(painter)

        # Draw the pieces
        self.draw_pieces(painter)

        # Draw the dragged piece
        if self.dragging and self.drag_piece:
            self.draw_dragged_piece(painter)

    def draw_board(self, painter):
        """Draw the chess board.

        Args:
            painter: QPainter object
        """
        # Set the opacity
        painter.setOpacity(config.BOARD_OPACITY)

        # Draw the squares
        for row in range(8):
            for col in range(8):
                square = row * 8 + col
                x = col * self.square_size
                y = (7 - row) * self.square_size  # Flip the board

                # Determine the square color
                is_light = (row + col) % 2 == 0
                color = QColor(config.BOARD_COLORS["light" if is_light else "dark"])

                # Check if the square is highlighted
                if square == self.selected_square:
                    color = QColor(config.BOARD_COLORS["highlight"])
                elif square in self.highlighted_squares:
                    color = QColor(config.BOARD_COLORS["highlight"])

                # Check if the square was part of the last move
                last_move = self.engine.get_last_move()
                if last_move:
                    if square == last_move.from_square or square == last_move.to_square:
                        color = QColor(config.BOARD_COLORS["last_move"])

                # Draw the square
                painter.fillRect(
                    x, y, self.square_size, self.square_size, color
                )

        # Draw the board border
        painter.setPen(QPen(QColor(0, 0, 0, 150), 2))
        painter.drawRect(
            0, 0, self.board_size, self.board_size
        )

    def draw_pieces(self, painter):
        """Draw the chess pieces.

        Args:
            painter: QPainter object
        """
        # Reset opacity for pieces
        painter.setOpacity(1.0)

        # Draw each piece
        for square in chess.SQUARES:
            # Skip the dragged piece
            if self.dragging and square == self.selected_square:
                continue

            piece = self.engine.get_piece_at(square)
            if piece:
                # Get the piece position
                col = chess.square_file(square)
                row = 7 - chess.square_rank(square)  # Flip the board
                x = col * self.square_size
                y = row * self.square_size

                # Draw the piece
                self.draw_piece(painter, piece, x, y)

    def draw_piece(self, painter, piece, x, y):
        """Draw a chess piece.

        Args:
            painter: QPainter object
            piece: chess.Piece object
            x: X coordinate
            y: Y coordinate
        """
        # Get the piece symbol
        symbol = piece.symbol()

        # Map symbols to Unicode chess pieces
        unicode_map = {
            'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
            'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚'
        }

        # Set the font
        font = QFont("Arial", int(self.square_size * 0.7))
        painter.setFont(font)

        # Set the color
        color = QColor(255, 255, 255) if piece.color == chess.WHITE else QColor(0, 0, 0)
        painter.setPen(color)

        # Draw the piece
        painter.drawText(
            QRect(int(x), int(y), int(self.square_size), int(self.square_size)),
            Qt.AlignmentFlag.AlignCenter,
            unicode_map[symbol]
        )

    def draw_dragged_piece(self, painter):
        """Draw the piece being dragged.

        Args:
            painter: QPainter object
        """
        if not self.drag_piece or not self.drag_current_pos:
            return

        # Reset opacity for the dragged piece
        painter.setOpacity(1.0)

        # Calculate the position
        x = self.drag_current_pos.x() - self.square_size // 2
        y = self.drag_current_pos.y() - self.square_size // 2

        # Draw the piece
        self.draw_piece(painter, self.drag_piece, x, y)

    def mousePressEvent(self, event):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Get the square at the mouse position
            pos = event.position()
            square = self.get_square_at_pos(pos)

            if square is not None:
                piece = self.engine.get_piece_at(square)
                current_turn = self.engine.get_current_turn()

                # Check if the piece belongs to the current player
                if piece and ((piece.color == chess.WHITE and current_turn == "white") or
                             (piece.color == chess.BLACK and current_turn == "black")):
                    # Start dragging
                    self.dragging = True
                    self.selected_square = square
                    self.drag_piece = piece
                    self.drag_start_pos = pos
                    self.drag_current_pos = pos

                    # Highlight legal moves
                    self.highlighted_squares = [
                        move.to_square for move in self.engine.get_legal_moves_for_square(square)
                    ]

                    # Update the board
                    self.update()
                elif self.selected_square is not None:
                    # Try to make a move
                    move = chess.Move(self.selected_square, square)

                    # Check for promotion
                    if self.engine.get_piece_type(self.selected_square) == chess.PAWN:
                        # Check if the move is to the last rank
                        to_rank = chess.square_rank(square)
                        if (to_rank == 7 and self.engine.get_piece_color(self.selected_square) == chess.WHITE) or \
                           (to_rank == 0 and self.engine.get_piece_color(self.selected_square) == chess.BLACK):
                            # Promote to queen by default
                            move = chess.Move(self.selected_square, square, chess.QUEEN)

                    if self.engine.make_move(move):
                        # Move was successful
                        self.move_made.emit(move)

                        # Update the move log
                        self.move_log.update_moves(self.engine.get_move_history())

                        # Update the turn indicator
                        self.update_turn_indicator()

                        # Check if the game is over
                        if self.engine.is_game_over():
                            self.game_over.emit(self.engine.get_game_result())

                        # Save the game
                        self.save_game()

                    # Reset selection
                    self.selected_square = None
                    self.highlighted_squares = []

                    # Update the board
                    self.update()

    def mouseMoveEvent(self, event):
        """Handle mouse move events."""
        if self.dragging:
            self.drag_current_pos = event.position()
            self.update()

    def mouseReleaseEvent(self, event):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton and self.dragging:
            # Get the square at the mouse position
            pos = event.position()
            square = self.get_square_at_pos(pos)

            if square is not None and square != self.selected_square:
                # Try to make a move
                move = chess.Move(self.selected_square, square)

                # Check for promotion
                if self.engine.get_piece_type(self.selected_square) == chess.PAWN:
                    # Check if the move is to the last rank
                    to_rank = chess.square_rank(square)
                    if (to_rank == 7 and self.engine.get_piece_color(self.selected_square) == chess.WHITE) or \
                       (to_rank == 0 and self.engine.get_piece_color(self.selected_square) == chess.BLACK):
                        # Promote to queen by default
                        move = chess.Move(self.selected_square, square, chess.QUEEN)

                if self.engine.make_move(move):
                    # Move was successful
                    self.move_made.emit(move)

                    # Update the move log
                    self.move_log.update_moves(self.engine.get_move_history())

                    # Update the turn indicator
                    self.update_turn_indicator()

                    # Check if the game is over
                    if self.engine.is_game_over():
                        self.game_over.emit(self.engine.get_game_result())

                    # Save the game
                    self.save_game()

            # Reset dragging
            self.dragging = False
            self.drag_piece = None
            self.drag_start_pos = None
            self.drag_current_pos = None

            # Reset selection
            self.selected_square = None
            self.highlighted_squares = []

            # Update the board
            self.update()

    def get_square_at_pos(self, pos):
        """Get the chess square at a given position.

        Args:
            pos: QPointF position

        Returns:
            int or None: Chess square (0-63) or None if outside the board
        """
        # Check if the position is within the board
        if (pos.x() < 0 or pos.x() >= self.board_size or
            pos.y() < 0 or pos.y() >= self.board_size):
            return None

        # Calculate the square
        col = int(pos.x() // self.square_size)
        row = 7 - int(pos.y() // self.square_size)  # Flip the board

        return row * 8 + col

    def sizeHint(self):
        """Get the suggested size for the widget."""
        return QSize(self.board_size + 250, self.board_size + 50)

    def minimumSizeHint(self):
        """Get the minimum suggested size for the widget."""
        return QSize(self.board_size + 200, self.board_size)

    def on_connection_requested(self, ip_address):
        """Handle connection request.

        Args:
            ip_address: IP address to connect to
        """
        # This is a placeholder for the actual network connection code
        # In a real implementation, this would establish a socket connection

        print(f"Connection requested to: {ip_address}")

        # For demonstration purposes, we'll simulate a successful connection
        self.connected = True
        self.peer_name = ip_address

        # Update the connection panel
        self.connection_panel.set_connected(True, self.peer_name)

        # Emit the connection status changed signal
        self.connection_status_changed.emit(True, self.peer_name)

    def set_connection_status(self, connected, peer_name=None):
        """Set the connection status.

        Args:
            connected: Whether the connection is established
            peer_name: Name of the connected peer (optional)
        """
        self.connected = connected
        self.peer_name = peer_name if connected else None

        # Update the connection panel
        self.connection_panel.set_connected(connected, peer_name)

        # Emit the connection status changed signal
        self.connection_status_changed.emit(connected, peer_name if connected else "")

    def show_reset_button(self):
        """Show the reset button below the board."""
        self.reset_button.setVisible(True)

    def hide_reset_button(self):
        """Hide the reset button."""
        self.reset_button.setVisible(False)

    def reset_all(self):
        """Reset all states - game, connection, and move history."""
        # Reset the board
        self.engine.reset_board()

        # Reset the connection if connected
        if self.connected:
            self.set_connection_status(False)

        # Update the move log
        self.move_log.update_moves([])

        # Update the turn indicator
        self.update_turn_indicator()

        # Hide the reset button
        self.hide_reset_button()

        # Update the board
        self.update()

    def reset_board(self):
        """Reset the board to the starting position."""
        # Ask for confirmation
        reply = QMessageBox.question(
            self,
            "Reset Board",
            "Are you sure you want to reset the board? This will clear the current game.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            # Reset the board
            self.engine.reset_board()

            # Update the move log
            self.move_log.update_moves([])

            # Update the turn indicator
            self.update_turn_indicator()

            # Hide the reset button if visible
            self.hide_reset_button()

            # Update the board
            self.update()

            return True

        return False
