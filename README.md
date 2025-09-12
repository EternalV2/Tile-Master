# Tile Master
<img width="170" height="170" alt="image" src="https://github.com/user-attachments/assets/0fa2f360-46b6-48c6-9c0b-20b20b7c55bb" />


## Overview
Tile Master is a custom 2D game engine built from scratch using the Pygame Library, meant for the simple and rapid development of top-down, 2D games by individuals with minimal software development experience. Unlike a typical game project, Tile Master was designed as a full development platform — complete with its own level editor, pixel editor, animation toolset, and game runtime engine. The engine is composed of a level editor, pixel editor, animation software, a built-in pathfinding AI system, camera system, audio system, particle renderer system, collision detection, sprite manager system, and a customizable user interface. The goal is to allow users to make fun and aesthetic games quickly, without the loss of functionality. 

## Highlights
- Input & Collision Detection System: Custom collision detection and input handling for player & NPC interactions.
- Particle System: Configurable particle emitters with randomized trajectories.
- Audio System: Integrated sound and music playback.
- Sprite/Animation Manager: Hierarchical asset management for characters (by action and direction).
- Game AI System: NPC movement, pathfinding, and autonomous behaviour are managed by the engine using custom, open source algorithms. 
- Rendering System: Camera with zoom, boundary snapping, and layered sprite rendering.
- Level Editor: GUI Program for designing tile-based maps, animations, and integrating audio.
- Tile & Pixel Editor: Built-in sprite drawing tool with metadata and memory access.
- Animation Support: Frame-by-frame sprite animation system for characters and environments.

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
<img width="540" height="300" alt="image" src="https://github.com/user-attachments/assets/0588977d-1b1f-410d-a15a-868553b05342" />

*User Interface of The Level Editor, designing a game level*

The first program we will look at is level_editor.py. The level editor allows users to animate the levels using square tiles with dimensions of 10 by 10 pixels, 16 by 16 pixels, or 32 by 32 pixels. These tiles can be created using the Tile Drawer program, which can be opened up through the Level Editor program by clicking the first button. The Tile Drawer program allows you to set certain attributes, other than pixel color, such as whether the player can walk on them or whether they should have a transparent background.
<img width="827" height="500" alt="image" src="https://github.com/user-attachments/assets/d22c42b6-d60a-43a6-901c-0c328f7cc479" />

*User Interface of The Tile Drawer, designing a grass tile*

The tile images will be saved in a directory named "_10/" for 10 by 10 pixel tiles, "_16"  for 16 by 16 pixel tiles, and "_32" for 32 by 32 pixel tiles. The tile attributes will be stored in a file called tile_log.txt placed in the current working directory. After designing the tiles and setting their attributes, the user can then draw out the desired map. After a base map has been designed, the user can then add new frames and start the process of animating the map. Using the level editor tool, the user is able to add effects on top of the map, shuffle in between frames, and play the full animation. Finally, the user can add music to the level after they are finished designing. The completed map is then stored in a .txt file, which game_demo.py can decode. The complete controls for the Level Editor Tool are shown below:

<img width="496" height="300" alt="Screen Shot 2025-09-11 at 12 59 36 AM" src="https://github.com/user-attachments/assets/17e18674-02e4-4050-a063-11f1b88070ee" />

*Controls for The Tile Editor*

## The Game Demo Implementation
The second program we will discuss is game_demo.py. This is the program that runs the level and thus allows the player to interact with the program. Thus, game_demo.py acts as the main file accessing the game engine. Before we delve into the game engine, a quick note about the limitations of the game engine should be discussed. Due to the immense complexity involved in building a fully fledged game engine, we had to make a few important tradeoffs that influenced the development of the engine. Below is a list of important tradeoffs that were made in its development. 

### Perspective
As previously mentioned, this is a top-down, 2d tile based game engine. Therefore, all of the art, physics, and logic of the games designed using Tile Master must take into account this aerial perspective. This has wide ranging implications for the system, chief amongst them being that for any moving object within the game (NPCs, playable characters, projectiles, etc.), there are 8 directions of movement: Up, Down, Left, Right, Left-Up, Left-Down, Right-Up, Right-Down, commonly denoted as "u", "d", "l", "r", "lu", "ld", "ru", and "rd" respectively. While the objects are locked into only moving in these directions, particle effects, map animations, and GUI elements have a greater range of motion since they are not treated as objects, as the camera system renders them in a different manner.

### Camera System
The camera system in the game engine is also restricted in ways that game designers must take into account. The camera is initialized with an object it keeps in the center of the screen (usually the player, but the central object can be any object within the level). However, if the object approaches a side of the map (either a corner or a left, right, up, or down boundary), the camera will stop following the object and allow it to move being untethered to the center of the screen. When the object leaves the vicinity of the side, the camera will refocus on the object and recenter it on the screen. This is done in order to keep the camera from going off the map. The camera can also zoom in and out to a certain extent, but it will follow this same locking and unlocking principle. The camera's center object can also change while in-game (for example, allowing it to focus on an enemy for a short time frame after the player has been defeated). It is also worth noting that everything except the UI is displayed using the camera, and that the camera for the Level Editor Program works slightly differently in that it moves using the users commands (the WASD keys) and that it does not have the snapping mechanism, so it is allowed to drift off-screen. This is done intentionally as it is a better fit for drawing the game levels. 

<pre>
camera = Camera(player, TILE_SIZE)
</pre>

*Camera Initialization with the first argument being the center object and the second argument being the standard zoom*

<img width="202" height="202" alt="New Piskel-1 png(1)" src="https://github.com/user-attachments/assets/81c2fdce-608d-4f18-bab4-c8daf6421ce0" />

*Visual diagram of how the camera renders the screen (gray rectangle) and follows a central object (gold) depending on the object's proximity to the sides of the map (black outline). The green area in the center of the map is the region where the camera will lock onto the object and keep it in the center of the screen. If the object moves into the dark blue region, the camera will follow the object as it moves vertically, but will not move horizontally to avoid rendering a portion of the screen off the map. Likewise, if the object moves into the light blue region, the camera will follow the object horizontally but will not move vertically. If the object moves into either of the 4 corners, the camera will snap to the center of the corners and stay there until the object has left the corners. The red lines represent the boundaries of the regions where the camera will change its current movement*

### Characters 
The game engine handles characters in a structured way. Characters are initialized with a variety of attributes, including name, size, and speed. The character sprites are stored following a particular hierarchy illustrated below:
<pre>
{character_name}
|_______________{action 1}
|  |_______________u
|  |  |________________0.png
|  |  |________________1.png
|  |_______________d
|  |  |________________0.png
|  |  |________________1.png
|  |_______________ld
|  |  |________________0.png
|  |  |________________1.png
|  |_______________rd
|  |  |________________0.png
|  |  |________________1.png
|_______________{action 2}
|  |_______________etc...
</pre>
*All the sprites for a particular character are stored in a folder named after the character. Then inside that folder, you have the folders that hold the sprite for particular actions the characters can take (for example, attack, walk, dance, etc.). Inside each action's folder, you have 4 folders named "u", "d", "ld", and "rd" symbolizing the directions "up", "down", "left-down", and "right-down" respectively. This extreme level of precision and structure in the directory allows game designers to offload the work of managing the various paths of the sprites to the game engine, allowing them to simply type the name of the character and have the game engine load the images flawlessly and without hassle*

### NPC and Player Systems
The NPC system animates the character sprites in a few ways, most notably, the NPC system implements a pathfinding algorithm. More specifically, the NPC computes a vector based on where the player is relative to the NPC's position, normalizes that into a direction, and then adjusts its position by snapping to adjacent grid tiles, checking that it takes a valid path and that it does not collide with any other objects in the process. If the normalized vector is mostly horizontal, the NPC will move horizontally, and if it is mostly vertical, the NPC will move vertically. If the vector is approximately equal to vertical and horizontal, the NPC will move diagonally. To ensure that the NPCs do not all follow the same path towards the player and avoid clustering, the pathfinding algorithm also computes a separation vector, which is a normalized sum of vectors between the current NPC and nearby NPCs that pushes the current NPC away from nearby NPCs with a set amount of force. If the NPC is an enemy of the player, and it is within a certain distance, it will begin to attack. Apart from the pathfinding AI, the rest of the NPC system is geared to manage the sprites, timing, animation, and game logic of the NPC. THe player system is similar to the NPC system and only differs in the fact that it lacks the pathfinding algorithm inherent in the NPC system because it relies on the human player to control its movement. 

<pre>
Npc({x position}, {y position}, TILE_SIZE, {team}, {name}, {attack_moves}, {.2}, {idle animation}, {character FPS})
</pre>
*NPC Initialization*

<pre>
Player({x position}, {y position}, {size}, {character name}, {attack_moves}, {speed}, {idle animation}, {animation time}, {player FPS})
</pre>
*Player Initialization*

### Particle Emitter
Every object can have a particle emitter attached to it for graphical effects. These particles serve a purely aesthetic purpose, but can be useful visual markers (such as marking when the player gets hit by a projectile or what action a character has just done). Particles, alongside the UI elements, are the only elements in the game engine that are not locked into following one of the eight directions (cardinals and diagonals) for movement. 

<pre>
ParticleEmitter({x position}, {y position}, {number of particles})
</pre>
*Particle Emitter Initialization*

<pre>
for _ in range(self.num_particles):
    particle = Particle(self.x, self.y, "r")
    self.particles.append(particle)
</pre>
*Individual Particle Initialization*

<pre>
for _ in range(self.num_particles):
    angle = random.uniform(0, 2 * math.pi)
    radius = random.uniform(0, max_radius)
    x = center_x + radius * math.cos(angle)
    y = center_y + radius * math.sin(angle)
    particle = Particle(x, y, "g")
    self.particles.append(particle)
</pre>
*Example of Particles set to be Emitted in a Circular Trajectory*

## Wrap Up 
The above serves as a limited overview and tutorial, allowing both game designers to start designing games using Tile Master and developers to start extending and building on top of Tile Master in any way they see fit. This does not serve to act as an exhaustive analysis of the program focused on revealing all of its functionality. It is quite the opposite; there is still much more to discover and learn in Tile Master. We can't wait to see what you create using Tile Master. Happy Creating!
