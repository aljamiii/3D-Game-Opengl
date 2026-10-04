# The Lost Labyrinth - Action Game

A 3D first-person maze game built with OpenGL and Python where you navigate through challenging labyrinths, defeat enemies, collect powerups, and find your way to the exit.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Game Mechanics](#game-mechanics)
- [Controls](#controls)
- [Maps](#maps)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)
- [Contributors](#contributors)

## 🎮 Overview

**The Lost Labyrinth** is a 3D action-adventure game where players explore maze-like levels filled with enemies, collectibles, and powerups. Using a first-person perspective, players must strategically navigate through corridors, shoot enemies with limited ammunition, and reach the exit point while managing their health.

## ✨ Features

### Core Gameplay

- **First-Person 3D Graphics**: Immersive OpenGL-rendered environment with perspective projection
- **Multiple Levels**: 5 unique maze layouts with increasing difficulty
- **Enemy AI**: Intelligent enemies that chase the player when detected or shot at
- **Combat System**: Gun-based shooting mechanics with ammunition management and reload system
- **Health System**: Collect fruits to restore health and survive enemy encounters

### Advanced Mechanics

- **Ammo System**: 6-bullet magazine with 1-second reload time
- **Powerup System**: Four distinct powerups with timed effects:
  - **Speed Boost** (Cyan): Increased movement speed
  - **Invincibility** (Yellow): Immunity to enemy damage
  - **Damage Boost** (Magenta): Enhanced shooting power and range
  - **Rapid Fire** (Orange): Unlimited ammo (no reload required)
- **Particle Effects**: Dynamic explosion effects when enemies are eliminated
- **Camera Shake**: Visual feedback during shooting and impacts
- **Teleportation**: Emergency teleport ability to escape danger
- **Frame Rate Control**: Locked at 60 FPS for smooth gameplay

### Visual Elements

- Color-coded game elements for easy recognition
- 3D enemy models with cylindrical bodies and spherical heads
- Distinct wall, ground, and sky rendering
- Collectible fruits and powerups clearly visible in the environment

## 🔧 Installation

### Prerequisites

- Python 3.7 or higher
- PyOpenGL library

### Setup Steps

1. **Clone the Repository**

   ```bash
   https://github.com/Tawseef-Tonoy/CSE423
   cd cse423_project
   ```

2. **Install Dependencies**

   ```bash
   pip install PyOpenGL PyOpenGL_accelerate
   ```

3. **Run the Game**
   ```bash
   python main.py
   ```

## 🎯 How to Play

1. **Launch the game** by running `main.py`
2. **Select a map** from the menu (Press 1-5)
3. **Navigate** through the maze using WASD keys
4. **Shoot enemies** using Space or Left Mouse Button
5. **Collect fruits** (green) to restore health
6. **Collect powerups** (colored) for temporary abilities
7. **Reach the exit point** (position 9,9) to complete the level
8. **Press R** to restart if you die or want to try again
9. **Press ESC** to return to the main menu

## 🎮 Controls

### Menu Controls

- **1-5**: Select map
- **ESC**: Return to main menu

### In-Game Controls

- **W**: Move forward
- **S**: Move backward
- **A**: Rotate left
- **D**: Rotate right
- **SPACE** or **Left Mouse Button**: Shoot
- **R**: Restart current level
- **ESC**: Return to main menu

## 🎲 Game Mechanics

### Health System

- Start with 2 HP
- Lose 1 HP when touching an enemy
- Gain 1 HP by collecting fruits (green spheres)
- Game over when HP reaches 0

### Ammo System

- Magazine capacity: 6 bullets
- Reload time: 1 second
- Bullets reload automatically when magazine is empty
- Rapid Fire powerup bypasses reload requirement

### Enemy Behavior

- **Idle State**: Enemies patrol their spawn area
- **Chase State**: Activated when player is within 5 units OR when shot at (within 15 units)
- Enemies navigate around walls while chasing
- Move at 25% of player speed
- Eliminated by shooting within a narrow cone of vision

### Powerups (3-second duration)

- **Speed Boost**: Doubles movement speed
- **Invincibility**: Cannot take damage from enemies
- **Damage Boost**: Wider shooting angle and longer range
- **Rapid Fire**: Infinite ammo without reload

## 🗺️ Maps

The game features 5 progressively challenging levels:

1. **The Snake**: Winding corridor with 3 enemies
2. **The Hallway**: Long passages with 4 enemies
3. **The Room**: Open spaces with 4 enemies
4. **The Maze**: Complex pathways (enemy count varies)
5. **Final Challenge**: Ultimate test of skill

Each map is a 10×10 grid with:

- Starting position at (1,1)
- Exit point at varying locations
- Strategic powerup and fruit placement
- Enemy spawn points

## 📁 Project Structure

```
cse423_project/
├── main.py              # Entry point, OpenGL initialization, event handlers
├── config.py            # Game constants, colors, maps, settings
├── game_state.py        # Game state management, update loop, collision detection
├── player.py            # Player class, movement, shooting, powerup effects
├── enemy.py             # Enemy AI, movement, hit detection
├── maze.py              # Maze rendering, wall collision, entity management
├── particles.py         # Particle system for explosion effects
├── utils.py             # Utility functions (distance calculation, etc.)
└── OpenGL/              # PyOpenGL library files
```

### Key Files

- **main.py**: Sets up the GLUT window, handles input events, and manages the game loop
- **config.py**: Centralized configuration for colors, map layouts, powerup types, and game constants
- **game_state.py**: Manages level transitions, win/lose conditions, and entity updates
- **player.py**: Implements player movement, camera system, shooting mechanics, and powerup effects
- **enemy.py**: Contains enemy AI logic and collision detection
- **maze.py**: Renders 3D maze walls and manages collectible items
- **particles.py**: Handles explosion particle effects

## 🛠️ Technologies Used

- **Python 3.x**: Core programming language
- **PyOpenGL**: OpenGL bindings for 3D graphics
  - `OpenGL.GL`: Core OpenGL functions
  - `OpenGL.GLU`: OpenGL Utility Library for camera and quadrics
  - `OpenGL.GLUT`: OpenGL Utility Toolkit for window management
- **Math Module**: Trigonometric calculations for movement and angles
- **Random Module**: Procedural generation and effects

### Graphics Techniques

- Perspective projection with gluPerspective
- 3D transformations (translation, rotation)
- GLU quadrics for 3D primitives (spheres, cylinders)
- Depth testing for proper 3D rendering
- Double buffering for smooth animation

## 📝 License

This project is part of CSE423 coursework. See [LICENSE](LICENSE) for details.

## 🎓 Academic Context

This project was developed as part of the CSE423 (Computer Graphics) course, demonstrating:

- 3D graphics programming with OpenGL
- Game state management
- Real-time rendering techniques
- User interaction and input handling
- Object-oriented design patterns
- Collision detection algorithms

---

**Enjoy navigating The Lost Labyrinth!** 🎮✨
