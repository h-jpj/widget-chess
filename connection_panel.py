#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Connection panel widget for Widget Chess.
Provides a UI for connecting to another player over the network.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QLineEdit, QPushButton, QFrame, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QFont, QColor, QPalette

import config

class ConnectionPanel(QWidget):
    """Widget for connecting to another player."""
    
    # Signals
    connection_requested = pyqtSignal(str)  # IP address
    
    def __init__(self, parent=None):
        """Initialize the connection panel.
        
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
        
        # Create the header
        self.header = QLabel("Connect to a Friend")
        font = QFont("Arial")
        font.setPointSize(12)
        font.setWeight(QFont.Weight.Bold)
        self.header.setFont(font)
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.header.setStyleSheet("color: white;")
        
        # Create the separator
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.separator.setStyleSheet("background-color: #555555;")
        
        # Create the IP input
        self.ip_layout = QHBoxLayout()
        self.ip_label = QLabel("IP Address:")
        self.ip_label.setStyleSheet("color: white;")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IPv4 or IPv6 address")
        self.ip_layout.addWidget(self.ip_label)
        self.ip_layout.addWidget(self.ip_input)
        
        # Create the port input
        self.port_layout = QHBoxLayout()
        self.port_label = QLabel("Port:")
        self.port_label.setStyleSheet("color: white;")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("5555")
        self.port_input.setText("5555")
        self.port_layout.addWidget(self.port_label)
        self.port_layout.addWidget(self.port_input)
        
        # Create the connect button
        self.connect_button = QPushButton("Connect")
        self.connect_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
        """)
        
        # Create the status label
        self.status_label = QLabel("Not connected")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #aaaaaa;")
        
        # Add widgets to layout
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.separator)
        self.layout.addLayout(self.ip_layout)
        self.layout.addLayout(self.port_layout)
        self.layout.addWidget(self.connect_button)
        self.layout.addWidget(self.status_label)
        
        # Set up the widget appearance
        self.setup_appearance()
        
        # Connect signals
        self.connect_button.clicked.connect(self.on_connect_clicked)
    
    def setup_appearance(self):
        """Set up the appearance of the widget."""
        # Set background color with opacity
        palette = self.palette()
        background_color = QColor(30, 30, 30, 200)  # RGBA
        palette.setColor(QPalette.ColorRole.Window, background_color)
        self.setPalette(palette)
        self.setAutoFillBackground(True)
    
    def on_connect_clicked(self):
        """Handle connect button click."""
        ip_address = self.ip_input.text().strip()
        if not ip_address:
            self.status_label.setText("Please enter an IP address")
            self.status_label.setStyleSheet("color: #ff6666;")
            return
        
        # Emit the connection requested signal
        self.connection_requested.emit(ip_address)
        
        # Update the status
        self.status_label.setText("Connecting...")
        self.status_label.setStyleSheet("color: #ffcc66;")
    
    def set_connected(self, connected, peer_name=None):
        """Set the connection status.
        
        Args:
            connected: Whether the connection is established
            peer_name: Name of the connected peer (optional)
        """
        if connected:
            status_text = f"Connected to {peer_name}" if peer_name else "Connected"
            self.status_label.setText(status_text)
            self.status_label.setStyleSheet("color: #66ff66;")
            self.connect_button.setText("Disconnect")
            self.connect_button.setStyleSheet("""
                QPushButton {
                    background-color: #f44336;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #d32f2f;
                }
                QPushButton:pressed {
                    background-color: #b71c1c;
                }
            """)
        else:
            self.status_label.setText("Not connected")
            self.status_label.setStyleSheet("color: #aaaaaa;")
            self.connect_button.setText("Connect")
            self.connect_button.setStyleSheet("""
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border-radius: 5px;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3e8e41;
                }
            """)
    
    def sizeHint(self):
        """Get the suggested size for the widget."""
        return QSize(250, 200)
    
    def minimumSizeHint(self):
        """Get the minimum suggested size for the widget."""
        return QSize(200, 150)
