# Tile Master
<img width="990" height="536" alt="image" src="https://github.com/user-attachments/assets/e9b05174-c1c2-4c4a-9f09-6e0f57f73472" />

## Overview
Tile Master is a custom 2D game engine built from scratch using the Pygame Library, meant for the simple and rapid development of top-down, 2D games by individuals with minimal software development experience. The engine is composed of a level editor, pixel editor, animation software, a built-in pathfinding AI system, camera system, audio system, particle renderer system, collision detection, sprite manager system, and a customizable user interface. The goal is to allow users to make fun and aesthetic games quickly, without the loss of functionality. 

## Getting Started
Tile Master consists of 2 standalone programs: the level_editor.py, which is a GUI Program that allows the user to create the levels (it handles the sound system, the  tile pixel editor, frame-by-frame animation, and the level design), and game_demo.py, which handles the internal logic of the game (graphics rendering, user input, memory access, pathfinding, user interface, etc.) and initializes the base game object classes which the user can then inherit to build custom classes (such as the playable character class, the non-playable character class (NPC), the projectile class, the object class, the weapon class, etc.).

To get started with the level editor, make a new directory in the levels folder and then run:

<pre>
cd src 
python level_editor.py {name of current level folder}
</pre>
This will open up the Level Editor and direct it to start designing maps and assets in that folder. 

When a level is designed, you can then start to design the logic of the game. This is done by configuring game_demo.py and running it. 
To run game_demo.py:
<pre>
cd src 
python game_demo.py
</pre>
This will start the game up the Level Editor and direct it to start designing maps and assets in that folder. 
