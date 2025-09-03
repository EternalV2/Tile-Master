# Tile Master
<img width="170" height="170" alt="image" src="https://github.com/user-attachments/assets/0fa2f360-46b6-48c6-9c0b-20b20b7c55bb" />


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
This will start the game preview and allow you to play through the current level. 

## Demo
We have developed a demo in order to showcase the capabilities and limitations of the Tile Master Game Engine and to provide examples, allowing new users to learn how the engine operates and how it can be used. The demo is based on the plot of The Lord Of The Rings, providing a humorous and interesting example of how Tile Master can bring J.R.R. Tolkien's classic world to life. The current game_demo.py file is configured to play the volcano level, but it is trivial to start a new project entirely from scratch (follow the instructions outlined in the Getting Started section). We shall also be using the Lord of the Rings demo to create a tutorial. 

## The Level Editor Implementation
<img width="1348" height="748" alt="image" src="https://github.com/user-attachments/assets/0588977d-1b1f-410d-a15a-868553b05342" />

*User Interface of The Level Editor, designing a game level*

The first program we will look at is level_editor.py. The level editor allows users to animate the levels using square tiles with dimensions of 10 by 10 pixels, 16 by 16 pixels, or 32 by 32 pixels. These tiles can be created using the Tile Drawer program, which can be opened up through the Level Editor program by clicking the first button. The Tile Drawer program allows you to set certain attributes, other than pixel color, such as whether the player can walk on them or whether they should have a transparent background.
<img width="1631" height="986" alt="image" src="https://github.com/user-attachments/assets/d22c42b6-d60a-43a6-901c-0c328f7cc479" />

*User Interface of The Tile Drawer, designing a grass tile*

The tile images will be saved in a directory named "_10/" for 10 by 10 pixel tiles, "_16"  for 16 by 16 pixel tiles, and "_32" for 32 by 32 pixel tiles. The tile attributes will be stored in a file called tile_log.txt placed in the current working directory. After designing the tiles and setting its attributes, the user can then draw out the desired map. After a base map has been designed, the user can then add new frames and start the process of animating the map. Using the level editor tool, the user is able to add effects on top of the map, shuffle in between frames, and play the full animation. Finally, the user can add music to the level after they are finished designing. The completed map is then stored in a .txt file which game_demo.py can decode. The complete controls for the Level Editor Tool are shown below:

<img width="411" height="612" alt="image" src="https://github.com/user-attachments/assets/e5d3440f-f6ab-4fe8-98ab-e249989ea972" />

*Controls for The Tile Editor*
