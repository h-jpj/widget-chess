#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuration settings for the Widget Chess application.
"""

import os
import json
from pathlib import Path

# Application settings
APP_NAME = "Widget Chess"
APP_VERSION = "1.0.0"

# File paths
HOME_DIR = str(Path.home())
CONFIG_DIR = os.path.join(HOME_DIR, ".config", "widget_chess")
SAVE_FILE = os.path.join(CONFIG_DIR, "game_state.json")
LOG_FILE = os.path.join(CONFIG_DIR, "game_log.json")
ENCRYPTION_KEYS_FILE = os.path.join(CONFIG_DIR, "encryption_keys.json")
NETWORK_KEYS_FILE = os.path.join(CONFIG_DIR, "network_keys.json")

# Ensure config directory exists
os.makedirs(CONFIG_DIR, exist_ok=True)

# Board settings
SQUARE_SIZE = 60  # Size of each square in pixels
BOARD_SIZE = SQUARE_SIZE * 8  # Total board size
BOARD_OPACITY = 0.8  # Default opacity for the board (0.0 - 1.0)
BOARD_COLORS = {
    "light": "#f0d9b5",  # Light squares
    "dark": "#b58863",   # Dark squares
    "highlight": "#aaa23b",  # Highlighted squares
    "last_move": "#7eb36b"  # Last move highlight
}

# Turn indicator settings
TURN_INDICATOR_TEXT = {
    "white": "YOUR TURN",
    "black": "YOUR TURN",
    "white_check": "CHECK! YOUR TURN",
    "black_check": "CHECK! YOUR TURN",
    "white_checkmate": "CHECKMATE! BLACK WINS",
    "black_checkmate": "CHECKMATE! WHITE WINS"
}
TURN_INDICATOR_COLORS = {
    "white": "#ffffff",
    "black": "#000000",
    "check": "#ff9900",
    "checkmate": "#ff0000"
}
GLOW_COLOR = {
    "white": "#ffffcc",
    "black": "#aaaaff",
    "check": "#ffcc00",
    "checkmate": "#ff6666"
}
GLOW_RADIUS = 30
GLOW_RADIUS_CHECK = 40  # Increased glow radius for check
GLOW_RADIUS_CHECKMATE = 50  # Even larger glow radius for checkmate

# Keyboard shortcut
DEFAULT_SHORTCUT = "Ctrl+Alt+C"  # Default shortcut to show/hide the widget

# Network settings
DEFAULT_PORT = 5555
CONNECTION_TIMEOUT = 30  # seconds

# Default settings
DEFAULT_SETTINGS = {
    "opacity": BOARD_OPACITY,
    "shortcut": DEFAULT_SHORTCUT,
    "always_on_top": True,
    "start_minimized": False,
    "auto_save": True,
    "sound_enabled": True,
    "network_port": DEFAULT_PORT,
    "player_name": "Player"  # Default player name for network play
}

# Load user settings
def load_settings():
    """Load user settings from config file."""
    settings_file = os.path.join(CONFIG_DIR, "settings.json")
    settings = DEFAULT_SETTINGS.copy()

    if os.path.exists(settings_file):
        try:
            with open(settings_file, 'r') as f:
                user_settings = json.load(f)
                settings.update(user_settings)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading settings: {e}")

    return settings

# Save user settings
def save_settings(settings):
    """Save user settings to config file."""
    settings_file = os.path.join(CONFIG_DIR, "settings.json")

    try:
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)
    except IOError as e:
        print(f"Error saving settings: {e}")

# Current settings
SETTINGS = load_settings()
