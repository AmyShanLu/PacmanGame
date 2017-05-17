# Pacman_Game
README
PacMan Project

Name: Shan Lu, William Wong

Section: B2	—— CMPUT 275

Table of Contents:

          1. Introduction
          2. How to Play
          3. PacMan
          4. Events
          5. Map
          6. Ghosts
          7. Sources Used


1. Introduction
	This is a project created by Shan Lu and William Wong called PacMan. PacMan
	is a classic arcade game where PacMan tries to eat all of the pellets in the
	game, while trying to avoid the ghosts that are tring to eat them. This game
	also features a high score table where it stores the highest scores gotten in
	the game. This README will give you instructions on how to play the game, as
	well as in-depth descriptions on the different parts of the scripts.

  2. How to Play
	In order to start the game, go to the ubuntu command terminal and change the
	directory so that you are in the folder where the scripts are stored. Then,
	in the terminal type the following command: python3 GameStart.py. This should
	start the game.
	The game will start and a menu will pop up. It gives you two options: Start or
	Exit. If you press start, the PacMan game will start. If you press Exit, the
	game will close.
	In order for PacMan to change directions, the player
	will use the arrow keys. To move PacMan up, press the up arrow key. To move
	PacMan down, press the down arrow key. To move PacMan to the left, press the
	left arrow key. To move PacMan to the right, press the right arrow key.
	The goal of the game is to collect as many points as possible before you lose
	all your lives. To collect points, there are two ways to collect them: eat the
	pellets or eat the fruits. The pellets are the small dots you see on the map.
	In order for PacMan to collect these pellets, he must walk towards them.
	They give 10 points each, and there are 240 pellets in the level. Once you
	collect all the pellets, the level will restart and a new level will begin.
	The fruits are various objects that spawn every 7 seconds whenever there is no
	other fruit present. If PacMan eats the fruit by touching it, it will reward
	the player points depending on what fruit or object it is.
			Cherry: 100 points
			Strawberry: 300 points.
			Orange: 500 points.
			Apple: 700 points.
			Melon: 1000 points.
			Galaxian: 2000 points.
			Bell: 3000 points.
			Key: 5000 points.
	There will be ghosts that will chase you. There are 4 ghosts: Red, Pink, Blue,
	and Orange. Red will try to chase the player's position. Pink will try to
	chase toward's the players future location: that is, it will try to go to the
	tile 4 tiles away from where PacMan is going to. Blue will try to go 2 tiles
	away from where PacMan is going, as long as it is double the distance from the
	Red ghost. Orange ghost will mostly be randomly going to places.
	If PacMan gets hit by any of these ghosts, then PacMan will lose a life. When
	you lose all your lives, then the game is over. It will show you the 10 highest
	scores earned in the game. It will then prompt you to press the enter key to
	play again. If the player does press enter, it will restart and a new game
	will begin.
	In order to beat the ghosts, there is an energizer pellet. This pellet is
	larger than the other pellets, and if eaten by PacMan, the ghosts will stop
	chasing PacMan and be frightened, running around. Then PacMan can touch them
	without losing a life. If PacMan touches them, they will respawn from their
	house and start chasing after PacMan again. This effect does wear off and
	after that they will start chasing PacMan again.
	Warning: This game will create a file named 'High Scores.txt' in order for it
	to store the high scores. Removing it from the directory will remove the data
	stored.

3. PacMan
	The class PacMan is used to store various variables and functions used to
	move PacMan and eat dots and fruits.
	The variables stored in this class are:
		direction - The direction PacMan is going.
		prev_direction - The direction PacMan was going.
		x_value - The x-coordinates of PacMan.
		y_value - The y-coordinates of PacMan.
		lives - The number of lives PacMan has.
		image - The image of PacMan.
		score - The score PacMan has gotten.
		numdot - The number of pellets PacMan has eaten.
		getenergizer - If PacMan's energizer pellet is still in effect.
	The functions stored in this class are:
		move - draws PacMan going towards the direction he is facing. If the
		direction given by the player is invalid, PacMan will continue going in the
		direction he was previously going. If the previous direction is also invalid,
		then he will stay in place.
		eat_dots - checks if PacMan is in a tile with an active pellet, energizer,
		or fruit. If so, the following effects will happen:
				Pellet - Add 10 points to PacMan's score.
				Energizer - Give PacMan a powerup for a short time, which gives him the
				ability to eat ghosts. Ghosts will be frightened at this point in time
				until the powerup runs out.
		move_input - Reads the user's input and calls eat_dots and move.

4. Events
	This script has two classes. The events class stores the level number and
	various functions to continue the game. The fruit class stores various
	variables and functions to determine which fruit or object to spawn in and at
	what time.
	The event class:
		This class stores these variables:
			level - the level number.
			text - the text that will be used to write into the game. If the text is
			unavailable then it will use a default text.
		This class stores these functions:
			next_lvl - This function is called when PacMan eats all the normal pellets
			in the game. It will reset the map, activating all the pellets and
			energizers. It will also add 1 to the level number, change PacMan's numdot
			to zero, and calls restart_lvl to restart the level.
			restart_lvl - Redraws PacMan and the ghosts to their original position.
			It then redraws the map in the last state that is was in when the function
			was called. It will print "Get Ready" to start the game again.
			scoreboard - prints the score of PacMan onto the side.
			PacManLives - draws the amount of extra lives that PacMan has. If he has
			no more lives, then it will call the GameOver function.
			high_score - Displays the 10 highest scores in the game. It uses a text
			file to store the previous scores. It will then either make a new file if
			there is no file, or changes the file with the new set of high scores.
			GameOver - This function is called when PacMan runs out of lives. This
			function will call high_score and prompt the user to press enter to play
			again. If the user presses enter a new game will start.
	The fruit class:
		This class stores these variables:
			fruit_num - this is a random number from 0-100 that will determine which
			fruit to spawn.
			points - the amount of points a specific fruit is worth.
			active - whether the fruit is on the map or not.
			fruitspawn - the time used to measure when a fruit should be spawned.
			It also stores the various images needed to draw the fruits.
		This class stores these functions:
			create_fruit - draws the coresponding fruit depending on fruit_num.
			eat_fruit - checks if PacMan is on a fruit. If PacMan eats the fruit,
			this function will give PacMan points depending on which fruit is on the
			map. This function is called only if the fruit is active.


5. Map
	We used Tilemap class to represent the map of the game. The Tilemap class has a 28*36 bytes
array called tilemap which describes the pattern of the game map. Each Tilemap object has the
"legaltile" dictionary whose key is the tile location and value is the Tile object, this
attribute is used for detecting if the tile location that pacman or ghosts are about to go is
walkable. The time complexity for checking if pacman or ghosts go to a walkable tile is O(1).

	We used Tile class to represent each tile object in the tilemap. Each tile object has a
"tilelocation" attribute used to indicate the location of the tile in the tilemap. Also,
the tile object has two boolean attributes, "dot" and "energizer", indicating if the tile
has a dot or an energizer in it. Tile class has two methods. "initialDrawTile" method is only
used when the tilemap is constructed for the first time. "redrawTile" method is used to redraw
a tile after pacman or ghosts leave this tile.

6. Ghost
	ghosts.py contains four classes (Ghost, Chase, Scatter, Frightened) and three functions
(heuristiccost, nodeneighbour, shortestpath).

	Ghost class is used to represent the ghost object. For our pac-man game, like the classic
pacman, we have four ghosts with different colors (red ghost: ghostColor = 'R', pink ghost:
ghostColor = 'P', blue ghost: ghostColor = 'B', orange ghost: ghostColor = 'O'). Attributes
"xtile" and "ytile" are used to represent the tile location of the ghost, and attributes
"xloc" and "yloc" are used to represent the ghost location in pixels, in order to move smoothly
in the map, the ghost moves by 1 pixel each time. Attribute "mode" is used to represent the
current mode that the ghost is in. Ghosts has three modes: Chase, Scatter and Frightened. For
different modes, ghosts have different moving strategies.

	In 'Chase' mode, ghosts will chase the pacman following the shortest path between the ghost's
current tile location and it's target location (A* algorithm is used for getting the shortest path).
In order to make ghosts have different personalities, each ghost has their own target location for
'Chase' mode. For red ghost, the target location is pacman's current tile location. For pink ghost,
the target location is based on pacman's current tile location and it's moving direction (4 tiles
away from pacman's location). For blue ghost, the target location is based on pacman's current tile
location and red ghost's current tile location. For orange ghost, the target location is pacman's
current tile location if it's 8 tiles away from the pacman, otherwise, it's target location is it's
'Scatter' mode's target location which is (7,28) (at the corner of the game map).

	When ghosts are in 'Chase' mode, it will call shortestpath(tilemap, startnode, goalnode) function
each time the ghost moves to a new tile. Function shortestpath is implemented in A* algorithm, the
time complexity is O(b^d), where b is the average number of successors per state and d is the depth
of path. Manhattan distance is used for calculating the heuristic distance between the node and it's
goal node. When the heuristic distance is 0 for every node in the map, A* algorithm becomes Dijkstra's
algorithm, then the time complexity is O(n^2logn) for a n x n tile map.

	In 'Scatter' mode, each ghost uses one of corner tiles as the target tile, and in order to reducing
the running of calculating the ghost's moving path, the path finding function for the 'Scatter' mode
is checking the neighbors of the next tile and calculating their distance to the target tile using
Manhattan distance, and choose the tile with the smallest estimated distance as the tile moving to at the
next time. The time complexity of path finding in 'Scatter' mode is O(n), where n is the number of walkable
neighbor tiles.

	In 'Frightened' mode, ghosts wander in the map, and they choose their new moving direction at intersections
of the map randomly.

7. Sources used
	This game uses various sources to run the game. Here is the list of sources
	used by William and Shan.

	Pygame - An open source software generally used to run games on Python. The
	link to the source is: www.pygame.org.

	pacman_menu_background.png - Menu background image. The link to the source is:
	http://www.pacman.com/en/wp-content/themes/PACMAN/images/uploads/pac-man-maze-1280.jpg

	minheap.py - MinHeap class from eclass. The link to the source is:
	https://eclass.srv.ualberta.ca/mod/page/view.php?id=2317517

	shortestpath - A* algorithm, used Pseudocode from wikipedia. The link to the source is:
	https://en.wikipedia.org/wiki/A*_search_algorithm#Pseudocode

	The behaviors of ghosts are mainly based on the article: The Pac-Man Dossier by Jamey Pittman.
	The link to the source is: http://www.gamasutra.com/view/feature/3938/the_pacman_dossier.php?print=1
