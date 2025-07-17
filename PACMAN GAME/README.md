# Pac-Man Game 🎮

A fully functional, modular Pac-Man game built with Python and Pygame using object-oriented design principles!

## Features ✨

- **Modular Architecture**: Clean separation of concerns with organized code structure
- **Multiple Game States**: Menu, gameplay, and game over screens
- **Smart Ghost AI**: Advanced AI with chase, scatter, and frightened behaviors
- **Classic Pac-Man Gameplay**: Navigate through the maze, eat dots, and avoid ghosts
- **Power Pellets**: Eat the big dots to turn ghosts blue and eat them for extra points
- **Advanced Score System**: Earn points for eating dots (10 pts), power pellets (50 pts), and ghosts (200 pts with multipliers)
- **Lives System**: Start with 3 lives, lose one when caught by a ghost
- **Level Progression**: Complete levels by eating all dots
- **Tunnel System**: Move through the sides of the screen to teleport
- **Animated Sprites**: Pac-Man mouth animation and ghost movement
- **Game States Management**: Proper pause, game over, and restart functionality

## Project Structure 📁

```
PACMAN GAME/
├── main.py                    # Main entry point
├── game/                      # Game package
│   ├── entities/              # Game entities
│   │   ├── pacman.py         # Pac-Man player entity
│   │   ├── ghost.py          # Ghost entities with AI
│   │   └── dot.py            # Pellet and power pellet entities
│   ├── components/           # Reusable components
│   │   └── position.py       # Position component for entities
│   ├── states/               # Game state management
│   │   ├── menu.py           # Main menu state
│   │   ├── play.py           # Gameplay state
│   │   └── gameover.py       # Game over state
│   ├── ai/                   # Ghost AI behaviors
│   │   ├── chase.py          # Chase behavior implementation
│   │   ├── scatter.py        # Scatter behavior implementation
│   │   └── frightened.py     # Frightened behavior implementation
│   └── manager/              # Game management systems
│       ├── gamemanager.py    # Main game logic coordinator
│       ├── scoremanager.py   # Score and statistics management
│       └── levelmanager.py   # Level and collision management
├── assets/                   # Game assets
│   ├── images/               # Sprite images (expandable)
│   ├── sounds/               # Sound effects (expandable)
│   └── fonts/                # Custom fonts (expandable)
├── create_sprites.py         # Utility to generate basic sprites
└── README.md                 # This file
```

## Controls 🎮

### Menu Navigation
- **Arrow Keys**: Navigate menu options
- **Enter/Space**: Select menu option

### Gameplay
- **Movement**: Arrow Keys or WASD
  - ⬆️ Up Arrow or W
  - ⬇️ Down Arrow or S
  - ⬅️ Left Arrow or A
  - ➡️ Right Arrow or D
- **Pause**: P key
- **Restart** (when game over): R key
- **Menu** (when game over): M key
- **Quit** (when game over): Q key

## How to Run 🚀

1. Make sure Python 3.7+ is installed on your system
2. Install Pygame:
   ```
   pip install pygame
   ```
3. Navigate to the game directory:
   ```
   cd "PACMAN GAME"
   ```
4. Run the game:
   ```
   python main.py
   ```

## Game Architecture 🏗️

This Pac-Man implementation follows modern software engineering principles:

### Design Patterns Used
- **State Pattern**: For managing different game states (menu, play, game over)
- **Component System**: Position component shared across entities
- **Strategy Pattern**: Different AI behaviors for ghosts
- **Manager Pattern**: Separate managers for different game aspects

### Object-Oriented Features
- **Encapsulation**: Each class handles its own responsibilities
- **Inheritance**: Shared functionality through base classes
- **Polymorphism**: Different entities implement common interfaces
- **Abstraction**: Complex game logic hidden behind simple interfaces

### Modular Benefits
- **Maintainability**: Easy to modify individual components
- **Extensibility**: Simple to add new features or entities
- **Testability**: Individual modules can be tested separately
- **Reusability**: Components can be reused across different parts

## Gameplay Features 🎯

### Pac-Man
- Animated mouth that opens in the direction of movement
- Smooth movement with collision detection
- Tunnel teleportation through screen edges

### Ghost AI Behaviors
- **Blinky (Red)**: Aggressive direct chaser
- **Pinky (Pink)**: Ambush strategy (targets ahead of Pac-Man)
- **Inky (Cyan)**: Complex indirect targeting
- **Clyde (Orange)**: Switches between chase and scatter based on distance

### AI States
- **Chase Mode**: Actively pursue Pac-Man
- **Scatter Mode**: Move to designated corners
- **Frightened Mode**: Flee from Pac-Man when power pellet is eaten

### Scoring System
- Small Dot: 10 points
- Power Pellet: 50 points
- Ghost (1st): 200 points
- Ghost (2nd): 400 points
- Ghost (3rd): 800 points
- Ghost (4th): 1600 points

## Customization Guide 🔧

### Adding New Ghost Behaviors
1. Create a new file in `game/ai/`
2. Implement the behavior logic
3. Add the behavior to the ghost's AI system

### Creating New Game States
1. Add a new file in `game/states/`
2. Implement `handle_input()`, `update()`, and `draw()` methods
3. Register the state in the main game loop

### Adding Sound Effects
1. Place audio files in `assets/sounds/`
2. Load them in the appropriate manager
3. Play them at the right game events

### Custom Sprites
1. Run `create_sprites.py` to generate basic sprites
2. Replace with custom artwork in `assets/images/`
3. Modify the drawing methods to use image files instead of shapes

## Technical Details 🔧

- **Language**: Python 3.7+
- **Framework**: Pygame 2.0+
- **Architecture**: Object-Oriented with modular design
- **FPS**: 60 frames per second
- **Grid System**: 20x20 pixel tiles
- **AI**: State-based ghost behaviors
- **Collision**: AABB (Axis-Aligned Bounding Box) detection

## Future Enhancements 💡

### Planned Features
- [ ] Sound effects and background music
- [ ] High score persistence
- [ ] Multiple maze layouts
- [ ] Fruit bonus items
- [ ] Improved sprite graphics
- [ ] Particle effects
- [ ] Settings menu
- [ ] Difficulty levels

### Advanced Extensions
- [ ] Multiplayer support
- [ ] Custom level editor
- [ ] Achievement system
- [ ] Leaderboards
- [ ] Mobile controls support

## Development Notes 📝

This project demonstrates:
- **Clean Code Principles**: Readable, maintainable code structure
- **SOLID Principles**: Single responsibility, open/closed, dependency inversion
- **Game Development Patterns**: Entity-Component-System inspired design
- **Python Best Practices**: Proper module structure and documentation

## Troubleshooting 🔧

**Import Errors?**
- Make sure you're running from the correct directory
- Check that all `__init__.py` files are present

**Game runs too fast/slow?**
- Modify the `FPS` constant in `main.py`

**Want to modify AI behavior?**
- Edit the appropriate AI files in `game/ai/`
- Adjust timing and probability values in ghost update methods

## Credits 👨‍💻

- **Project**: CCOBJPGL COM246 Assignment
- **Framework**: Pygame Community
- **Design**: Classic Pac-Man by Namco
- **Implementation**: Modern Python with OOP principles

Enjoy playing! 🎮✨
