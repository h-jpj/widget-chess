#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Move log widget for Widget Chess.
Displays the history of moves in the game.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QScrollArea, QLabel,
    QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPalette

import config

class MoveLogWidget(QWidget):
    """Widget for displaying the move history."""

    move_selected = pyqtSignal(int)  # Signal emitted when a move is selected

    def __init__(self, parent=None):
        """Initialize the move log widget.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        # Set up the widget
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setMinimumWidth(200)
        self.setMaximumWidth(300)

        # Create the layout
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(5)

        # Create the scroll area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # Create the content widget
        self.content_widget = QWidget()
        self.content_layout = QVBoxLayout(self.content_widget)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(2)
        self.content_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Set up the scroll area
        self.scroll_area.setWidget(self.content_widget)
        self.layout.addWidget(self.scroll_area)

        # Set up the widget appearance
        self.setup_appearance()

        # Move labels
        self.move_labels = []

    def setup_appearance(self):
        """Set up the appearance of the widget."""
        # Set background color with opacity
        palette = self.palette()
        background_color = QColor(30, 30, 30, 200)  # RGBA
        palette.setColor(QPalette.ColorRole.Window, background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Set the content widget background
        content_palette = self.content_widget.palette()
        content_palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 0))
        self.content_widget.setPalette(content_palette)
        self.content_widget.setAutoFillBackground(True)

        # Set the scroll area background
        scroll_palette = self.scroll_area.palette()
        scroll_palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 0))
        self.scroll_area.setPalette(scroll_palette)
        self.scroll_area.setAutoFillBackground(True)

    def update_moves(self, move_history):
        """Update the move log with the current move history.

        Args:
            move_history: List of move information dictionaries
        """
        # Clear existing move labels
        for label in self.move_labels:
            self.content_layout.removeWidget(label)
            label.deleteLater()
        self.move_labels = []

        # Add header
        header = QLabel("Move History")
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Arial")
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Bold)
        header.setFont(font)
        header.setStyleSheet("color: white;")
        self.content_layout.addWidget(header)
        self.move_labels.append(header)

        # Add separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("background-color: #555555;")
        self.content_layout.addWidget(separator)
        self.move_labels.append(separator)

        # Add moves
        if not move_history:
            no_moves = QLabel("No moves yet")
            no_moves.setAlignment(Qt.AlignmentFlag.AlignCenter)
            no_moves.setStyleSheet("color: #aaaaaa;")
            self.content_layout.addWidget(no_moves)
            self.move_labels.append(no_moves)
        else:
            for i, move_info in enumerate(move_history):
                move_number = i // 2 + 1
                is_white = i % 2 == 0

                # Create move label
                if is_white:
                    move_text = f"{move_number}. {move_info['move']}"
                else:
                    move_text = f"{move_number}... {move_info['move']}"

                move_label = QLabel(move_text)
                move_label.setStyleSheet("color: white;")
                font = QFont("Arial")
                font.setPointSize(10)
                move_label.setFont(font)
                move_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
                move_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
                move_label.setToolTip(f"Move made at {move_info['timestamp']}")

                # Add to layout
                self.content_layout.addWidget(move_label)
                self.move_labels.append(move_label)

        # Scroll to the bottom
        self.scroll_area.verticalScrollBar().setValue(
            self.scroll_area.verticalScrollBar().maximum()
        )

    def sizeHint(self):
        """Get the suggested size for the widget."""
        return QSize(250, 400)

    def minimumSizeHint(self):
        """Get the minimum suggested size for the widget."""
        return QSize(200, 200)
