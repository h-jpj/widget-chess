# Widget Chess

A translucent chess widget for Linux desktops that enables long-term games between two players, either locally or over a network connection.

![Widget Chess Screenshot](https://github.com/yourusername/widget_chess/raw/main/resources/screenshot.png)

## 🌟 Features

- **Translucent Widget**: Chess board sits as a semi-transparent widget on your desktop
- **Toggle Visibility**: Hide/show with a keyboard shortcut (default: Ctrl+Alt+C)
- **Turn Indicator**: Clear "YOUR TURN" display with a glowing effect
- **Check & Checkmate Alerts**: Visual and popup notifications when a player is in check or checkmate
- **Peer-to-Peer Networking**: Connect directly to a friend using their IP address (IPv4 or IPv6)
- **End-to-End Encryption**: All game data is encrypted using AES-256
- **Drag and Drop Interface**: Intuitive piece movement
- **Move History**: Log of all moves made during the game
- **Local State Saving**: Game state is saved and automatically loaded on startup
- **System Tray Integration**: Control the application from your system tray
- **Reset Board**: Quickly reset the board to the starting position
- **Cross-Distribution Compatibility**: Works on all major Linux distributions

## 📋 Requirements

- Python 3.8+
- PyQt6
- python-chess
- cryptography
- socket (for networking)

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/widget_chess.git
   cd widget_chess
   ```

2. Install the required dependencies:
   ```bash
   pip install python-chess PyQt6 cryptography
   ```

3. Run the application:
   ```bash
   python main.py
   ```

## 📖 Usage

### Starting a Game

When you first run the application, a new game will be created automatically. The board will appear on your screen with white to move.

### Making Moves

1. Click and drag a piece to move it
2. Legal moves will be highlighted
3. Release the mouse button to complete the move
4. The turn indicator will update to show the next player's turn

### Check and Checkmate

1. When a player is in check, the turn indicator will change to "CHECK! YOUR TURN" with an orange glow
2. Only legal moves that get the king out of check will be allowed
3. When a player is in checkmate, the game will end
4. The turn indicator will change to "CHECKMATE!" with a red glow
5. A reset button will appear below the board to reset all states (game, connection, and move history)

### Connecting to a Friend

1. One player needs to ensure their firewall allows incoming connections on port 5555 (default)
2. This player should share their IP address with the other player
3. The other player enters this IP address in the connection field and clicks "Connect"
4. Once connected, moves will be synchronized between both players

### Game Controls

- **Show/Hide**: Press Ctrl+Alt+C to toggle visibility (customizable in settings)
- **System Tray**: Right-click the chess icon in the system tray for options:
  - Show/Hide: Toggle the widget visibility
  - New Game: Start a new game
  - Reset Board: Reset the board to the starting position
  - Connect: Open the connection dialog
  - Settings: Configure application settings
  - Quit: Exit the application

### Settings

Access settings through the system tray menu:

- **Opacity**: Adjust the transparency of the widget
- **Always on top**: Keep the widget above other windows
- **Start minimized**: Start the application hidden in the system tray
- **Auto-save**: Automatically save the game after each move
- **Network port**: Change the default networking port (requires restart)
- **Enable sounds**: Toggle sound effects (coming soon)

## ⚙️ Configuration

Configuration files are stored in `~/.config/widget_chess/`:

- `settings.json`: Application settings
- `game_state.json`: Encrypted game state
- `encryption_keys.json`: Encryption keys
- `network_keys.json`: P2P connection keys

## 🔄 Updates

This project is actively maintained. Check back regularly for updates:

- **v0.2.0** (Coming Soon): Network play implementation
- **v0.3.0** (Planned): Custom piece themes and board styles
- **v0.4.0** (Planned): Game analysis tools

## 🖥️ Cross-Compatibility

Widget Chess is designed to work on all Linux distributions, with particular focus on:
- Debian-based systems (Ubuntu, Linux Mint, etc.)
- Arch-based systems (Arch Linux, Manjaro, etc.)

## 🐛 Known Issues

- System tray icon may not appear on some desktop environments
- Global keyboard shortcuts may require additional setup on some distributions
- Network play requires manual port forwarding on some routers

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📜 License

This project is licensed under the GNU General Public License v3.0 (GPL-3.0) - see the LICENSE file for details.

The GPL-3.0 license ensures that all users have the freedom to run, study, share, and modify the software. If you distribute copies or modified versions of this software, you must pass on these same freedoms to the recipients and make the source code available to them.

## 🙏 Acknowledgments

- [python-chess](https://python-chess.readthedocs.io/) for the chess engine
- [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [cryptography](https://cryptography.io/) for encryption functionality
