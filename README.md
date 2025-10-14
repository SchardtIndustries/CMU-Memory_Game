# Memory Matching Game

A simple yet engaging memory game developed with `cmu_graphics`. Players click to find matching pairs of numbered dots, ignoring their colors. The game tracks scores, levels, hints, and high scores, providing an entertaining way to challenge and improve your memory skills.

## Features
- Match pairs of dots with the same number
- Multiple levels with increasing difficulty
- Use hints to reveal a matching pair
- Keep track of high scores
- View guesses and elapsed time

## How to Play
- Click on two dots to select them. If they have the same number, they are removed.
- Press `'h'` to reveal a matching pair as a hint.
- Press number keys (`1`-`5`) to start a new game at that specific level.
- Your score is calculated based on successful matches, with penalties for hints, guesses, and time.

## Requirements
- Python 3.x
- `cmu_graphics` library

## Installation

To install the `cmu_graphics` library, run:

```bash
pip install cmu_graphics
```
## Development and Packaging

### Development
- Created and developed using **Visual Studio Code**.
- The code is written in Python and managed within VS Code for ease of editing and debugging.

### Packaging as an Executable
- The application is packaged into a standalone `.exe` file using **PyInstaller**.
- All dependencies, including `cmu_graphics`, are bundled into the executable to allow easy distribution and execution without requiring a Python environment.

#### Packaging process overview:
1. Developed the code in VS Code.
2. Used **PyInstaller** to bundle the script:
   ```bash
   pyinstaller --onefile --add-data "path/to/cmu_graphics;cmu_graphics" Main.py
   ```
3. Distributed the resulting Main.exe located in the dist folder.

## Running the Game

### From Source
1. Clone or download the project repository.
2. Open a terminal or command prompt.
3. Navigate to the project directory.
4. Run the game with:
   ```bash
   python3 Main.py
   ```
### As a Standalone Executable
1. Download the repository from GitHub: [https://github.com/SchardtIndustries/CMU-Memory_Game](https://github.com/SchardtIndustries/CMU-Memory_Game)
2. Open the `CMU-Memory_Game` folder.
3. Navigate to the `dist` folder.
4. Double-click `Main.exe` or run it from the terminal to start the game.

Enjoy testing your memory with this fun and challenging game!


