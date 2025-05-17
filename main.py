#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Widget Chess - A translucent chess widget for Linux desktops.
"""

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QSystemTrayIcon,
    QMenu, QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QSlider, QCheckBox, QPushButton,
    QTabWidget, QLineEdit, QWidget
)
from PyQt6.QtGui import QIntValidator
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QAction, QKeySequence

import config
from chess_widget import ChessWidget
from resources.chess_icon import create_chess_icon

class SettingsDialog(QDialog):
    """Dialog for configuring application settings."""

    def __init__(self, parent=None):
        """Initialize the settings dialog.

        Args:
            parent: Parent widget
        """
        super().__init__(parent)

        self.setWindowTitle("Widget Chess Settings")
        self.setMinimumWidth(400)

        # Create the layout
        layout = QVBoxLayout(self)

        # Create tabs
        self.tabs = QTabWidget()

        # General settings tab
        general_tab = QWidget()
        general_layout = QVBoxLayout(general_tab)

        # Opacity setting
        opacity_layout = QHBoxLayout()
        opacity_label = QLabel("Opacity:")
        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(10, 100)
        self.opacity_slider.setValue(int(config.SETTINGS["opacity"] * 100))
        opacity_layout.addWidget(opacity_label)
        opacity_layout.addWidget(self.opacity_slider)

        # Always on top setting
        self.always_on_top = QCheckBox("Always on top")
        self.always_on_top.setChecked(config.SETTINGS["always_on_top"])

        # Start minimized setting
        self.start_minimized = QCheckBox("Start minimized")
        self.start_minimized.setChecked(config.SETTINGS["start_minimized"])

        # Auto-save setting
        self.auto_save = QCheckBox("Auto-save game")
        self.auto_save.setChecked(config.SETTINGS["auto_save"])

        # Sound setting
        self.sound_enabled = QCheckBox("Enable sounds")
        self.sound_enabled.setChecked(config.SETTINGS["sound_enabled"])

        # Add widgets to general tab
        general_layout.addLayout(opacity_layout)
        general_layout.addWidget(self.always_on_top)
        general_layout.addWidget(self.start_minimized)
        general_layout.addWidget(self.auto_save)
        general_layout.addWidget(self.sound_enabled)
        general_layout.addStretch()

        # Network settings tab
        network_tab = QWidget()
        network_layout = QVBoxLayout(network_tab)

        # Player name setting
        player_name_layout = QHBoxLayout()
        player_name_label = QLabel("Your Name:")
        self.player_name_input = QLineEdit()
        self.player_name_input.setText(config.SETTINGS.get("player_name", "Player"))
        player_name_layout.addWidget(player_name_label)
        player_name_layout.addWidget(self.player_name_input)

        # Port setting
        port_layout = QHBoxLayout()
        port_label = QLabel("Network Port:")
        self.port_input = QLineEdit()
        self.port_input.setText(str(config.SETTINGS.get("network_port", config.DEFAULT_PORT)))
        self.port_input.setValidator(QIntValidator(1024, 65535))
        port_layout.addWidget(port_label)
        port_layout.addWidget(self.port_input)

        # Port note
        port_note = QLabel("Note: Changing the port requires restarting the application")
        port_note.setStyleSheet("color: #888888; font-style: italic;")

        # Add widgets to network tab
        network_layout.addLayout(player_name_layout)
        network_layout.addLayout(port_layout)
        network_layout.addWidget(port_note)
        network_layout.addStretch()

        # Add tabs to tab widget
        self.tabs.addTab(general_tab, "General")
        self.tabs.addTab(network_tab, "Network")

        # Buttons
        button_layout = QHBoxLayout()
        save_button = QPushButton("Save")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)

        # Add widgets to main layout
        layout.addWidget(self.tabs)
        layout.addLayout(button_layout)

        # Connect signals
        save_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

    def get_settings(self):
        """Get the current settings from the dialog.

        Returns:
            dict: Settings dictionary
        """
        # Get network port (with validation)
        try:
            network_port = int(self.port_input.text())
            if network_port < 1024 or network_port > 65535:
                network_port = config.DEFAULT_PORT
        except ValueError:
            network_port = config.DEFAULT_PORT

        return {
            # General settings
            "opacity": self.opacity_slider.value() / 100,
            "always_on_top": self.always_on_top.isChecked(),
            "start_minimized": self.start_minimized.isChecked(),
            "auto_save": self.auto_save.isChecked(),
            "sound_enabled": self.sound_enabled.isChecked(),
            "shortcut": config.SETTINGS["shortcut"],  # Keep the existing shortcut

            # Network settings
            "player_name": self.player_name_input.text().strip() or "Player",
            "network_port": network_port
        }

class MainWindow(QMainWindow):
    """Main window for the Widget Chess application."""

    def __init__(self):
        """Initialize the main window."""
        super().__init__()

        # Set up the window
        self.setWindowTitle("Widget Chess")
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Create the chess widget
        self.chess_widget = ChessWidget(self)
        self.setCentralWidget(self.chess_widget)

        # Set up the system tray
        self.setup_tray()

        # Set up the keyboard shortcut
        self.setup_shortcut()

        # Apply settings
        self.apply_settings()

        # Show the window if not starting minimized
        if not config.SETTINGS["start_minimized"]:
            self.show()

    def setup_tray(self):
        """Set up the system tray icon and menu."""
        # Create the tray icon
        self.tray_icon = QSystemTrayIcon(self)

        # Use our custom chess icon
        self.tray_icon.setIcon(create_chess_icon())

        # Create the tray menu
        tray_menu = QMenu()

        # Add actions
        show_action = QAction("Show/Hide", self)
        show_action.triggered.connect(self.toggle_visibility)

        new_game_action = QAction("New Game", self)
        new_game_action.triggered.connect(self.new_game)

        reset_board_action = QAction("Reset Board", self)
        reset_board_action.triggered.connect(self.reset_board)

        connect_action = QAction("Connect to Friend", self)
        connect_action.triggered.connect(self.show_connection_panel)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.show_settings)

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.quit_application)

        # Add actions to menu
        tray_menu.addAction(show_action)
        tray_menu.addAction(new_game_action)
        tray_menu.addAction(reset_board_action)
        tray_menu.addAction(connect_action)
        tray_menu.addAction(settings_action)
        tray_menu.addSeparator()
        tray_menu.addAction(quit_action)

        # Set the tray menu
        self.tray_icon.setContextMenu(tray_menu)

        # Show the tray icon
        self.tray_icon.show()

        # Connect signals
        self.tray_icon.activated.connect(self.tray_activated)

    def setup_shortcut(self):
        """Set up the keyboard shortcut for showing/hiding the widget."""
        self.shortcut = QKeySequence(config.SETTINGS["shortcut"])

        # Create a global shortcut
        # Note: This requires additional setup for global shortcuts
        # For now, we'll use a regular shortcut that works when the app has focus
        shortcut_action = QAction(self)
        shortcut_action.setShortcut(self.shortcut)
        shortcut_action.triggered.connect(self.toggle_visibility)
        self.addAction(shortcut_action)

    def apply_settings(self):
        """Apply the current settings."""
        # Set opacity
        self.setWindowOpacity(config.SETTINGS["opacity"])

        # Set always on top
        if config.SETTINGS["always_on_top"]:
            self.setWindowFlags(
                self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint
            )
        else:
            self.setWindowFlags(
                self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint
            )

        # Apply the window flags
        self.show()

    def toggle_visibility(self):
        """Toggle the visibility of the widget."""
        if self.isVisible():
            self.hide()
        else:
            self.show()
            self.raise_()
            self.activateWindow()

    def new_game(self):
        """Start a new game."""
        self.chess_widget.engine.new_game()
        self.chess_widget.move_log.update_moves([])
        self.chess_widget.update_turn_indicator()
        self.chess_widget.update()

    def reset_board(self):
        """Reset the board to the starting position."""
        # Make sure the widget is visible
        if not self.isVisible():
            self.show()
            self.raise_()
            self.activateWindow()

        # Reset the board
        self.chess_widget.reset_board()

    def show_connection_panel(self):
        """Show the connection panel by making the widget visible."""
        # Make sure the widget is visible
        if not self.isVisible():
            self.show()
            self.raise_()
            self.activateWindow()

    def show_settings(self):
        """Show the settings dialog."""
        dialog = SettingsDialog(self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update settings
            new_settings = dialog.get_settings()
            config.SETTINGS.update(new_settings)
            config.save_settings(config.SETTINGS)

            # Apply settings
            self.apply_settings()

    def tray_activated(self, reason):
        """Handle tray icon activation.

        Args:
            reason: Activation reason
        """
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_visibility()

    def quit_application(self):
        """Quit the application."""
        # Save the game before quitting
        self.chess_widget.save_game()

        # Quit the application
        QApplication.quit()

    def closeEvent(self, event):
        """Handle the close event.

        Args:
            event: Close event
        """
        # Minimize to tray instead of closing
        event.ignore()
        self.hide()

def main():
    """Main entry point for the application."""
    # Create the application
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    # Create the main window
    window = MainWindow()

    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
