#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Chess icon for Widget Chess.
Provides a simple chess icon for the system tray.
"""

from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QBrush
from PyQt6.QtCore import Qt, QSize, QRect

def create_chess_icon():
    """Create a simple chess icon.
    
    Returns:
        QIcon: Chess icon
    """
    # Create a pixmap
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    # Create a painter
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    # Draw a chess board background
    painter.setPen(Qt.PenStyle.NoPen)
    square_size = 16
    for row in range(4):
        for col in range(4):
            is_light = (row + col) % 2 == 0
            color = QColor(240, 217, 181) if is_light else QColor(181, 136, 99)
            painter.fillRect(
                col * square_size, row * square_size,
                square_size, square_size,
                color
            )
    
    # Draw a knight symbol
    font = QFont("Arial")
    font.setPointSize(40)
    painter.setFont(font)
    painter.setPen(QColor(0, 0, 0))
    painter.drawText(QRect(0, 0, 64, 64), Qt.AlignmentFlag.AlignCenter, "♞")
    
    # End painting
    painter.end()
    
    # Create an icon from the pixmap
    return QIcon(pixmap)
