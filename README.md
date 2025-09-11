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

https://github.com/user-attachments/assets/9feef8f2-9a2f-498a-a454-7ad89487cfb2

*Frodo, Sam, and Gollum Witness the Eruption of Mount Doom*

https://github.com/user-attachments/assets/7b269479-9afb-410a-8996-367d0ff99190

*Game Play of Gandalf Fighting a Dragon in a Cavern*

## The Level Editor Implementation
<img width="1348" height="748" alt="image" src="https://github.com/user-attachments/assets/0588977d-1b1f-410d-a15a-868553b05342" />

*User Interface of The Level Editor, designing a game level*

The first program we will look at is level_editor.py. The level editor allows users to animate the levels using square tiles with dimensions of 10 by 10 pixels, 16 by 16 pixels, or 32 by 32 pixels. These tiles can be created using the Tile Drawer program, which can be opened up through the Level Editor program by clicking the first button. The Tile Drawer program allows you to set certain attributes, other than pixel color, such as whether the player can walk on them or whether they should have a transparent background.
<img width="1631" height="986" alt="image" src="https://github.com/user-attachments/assets/d22c42b6-d60a-43a6-901c-0c328f7cc479" />

*User Interface of The Tile Drawer, designing a grass tile*

The tile images will be saved in a directory named "_10/" for 10 by 10 pixel tiles, "_16"  for 16 by 16 pixel tiles, and "_32" for 32 by 32 pixel tiles. The tile attributes will be stored in a file called tile_log.txt placed in the current working directory. After designing the tiles and setting their attributes, the user can then draw out the desired map. After a base map has been designed, the user can then add new frames and start the process of animating the map. Using the level editor tool, the user is able to add effects on top of the map, shuffle in between frames, and play the full animation. Finally, the user can add music to the level after they are finished designing. The completed map is then stored in a .txt file, which game_demo.py can decode. The complete controls for the Level Editor Tool are shown below:

<img width="409" height="611" alt="Screen Shot 2025-09-11 at 12 59 36 AM" src="https://github.com/user-attachments/assets/17e18674-02e4-4050-a063-11f1b88070ee" />

*Controls for The Tile Editor*

## The Game Demo Implementation
The second program we will discuss is game_demo.py. This is the program that runs the level and thus allows the player to interact with the program. Thus, game_demo.py acts as the main file accessing the game engine. Before we delve into the game engine, a quick note about the limitations of the game engine should be discussed. Due to the immense complexity involved in building a fully fledged game engine, we had to make a few important tradeoffs that influenced the development of the engine. Below is a list of important tradeoffs that were made in its development. 

### Perspective
As previously mentioned, this is a top-down, 2d tile based game engine. Therefore, all of the art, physics, and logic of the games designed using Tile Master must take into account this aerial perspective. This has wide ranging implications for the system, chief amongst them being that for any moving object within the game (NPCs, playable characters, projectiles, etc.), there are 8 directions of movement: Up, Down, Left, Right, Left-Up, Left-Down, Right-Up, Right-Down, commonly denoted as "u", "d", "l", "r", "lu", "ld", "ru", and "rd" respectively. While the objects are locked into only moving in these directions, particle effects, map animations, and GUI elements have a greater range of motion since they are not treated as objects, as the camera system renders them in a different manner.

### Camera System
The camera system in the game engine is also restricted in ways that game designers must take into account. The camera is initialized with an object it keeps in the center of the screen (usually the player, but the central object can be any object within the level). However, if the object approaches a side of the map (either a corner or a left, right, up, or down boundary), the camera will stop following the object and allow it to move being untethered to the center of the screen. When the object leaves the vicinity of the side, the camera will refocus on the object and recenter it on the screen. This is done in order to keep the camera from going off the map. The camera can also zoom in and out to a certain extent, but it will follow this same locking and unlocking principle. The camera's center object can also change while in-game (for example, allowing it to focus on an enemy for a short time frame after the player has been defeated). It is also worth noting that everything except the UI is displayed using the camera, and that the camera for the Level Editor Program works slightly differently in that it moves using the users commands (the WASD keys) and that it does not have the snapping mechanism, so it is allowed to drift off-screen. This is done intentionally as it is a better fit for drawing the game levels. 
