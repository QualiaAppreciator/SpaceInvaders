GROUP 62 Computer Science E214 project

- Name: Space Inavders
- Purpose: To learn about object orientated programming in a fun and low-stress enviroment.
- Students: 26085410 - Blackenberg, NJ
            26890011 - Glyn-Cuthbert, J
            27293203 - Von Eschwege, MK



FRAMEWORK

- This project was coded using, exclusively, the libriaries in the virtual enviroment given to us on the fIRGA computers.

- Files the project is Composed of: 'project_main.py' (run from the command line and where the main function is contained)
                                    'functions.py' (houses all functions called by the main function in 'project_main.py')
                                    'gameObjects.py' (all objects used in this project are defined here)

- The modularity of the project is present in: The project being split up into three python files.
					       Functions called from 'project_main.py' in order to limited the amount of lines of code in the main.
                                               Methods in the objects such that they move and draw themselves.



ADVANCED FEATURES

- Music:
  > Added by MK. Von Eschwege

- Sounds:
  > Added by MK. Von Eschwege

- Player graphic choice function, playerChoice():
  > Added by J. Glyn-Cuthbert
  > A function that returns the graphic chosen by the player as a picture object.
  > The graphic is then initiated with the player object when a game is played.

- High score:
  > Added by MK. Von Eschwege and NJ. Blackenberg

- Progressively Harder Levels
  > Added by MK. Von Eschwege

- Additional shooter:
  > Added by J. Glyn-Cuthbert
  > If the player chooses to play multiplayer, the boolean variable, multiplayer, is made True.
  > If multiplayer is True, a second ' Player ' object is initialized.
  > The if statement in the ' gameplay ' while lopp for the multiplayer functionality is evaluated and entered.
  > As long as one player survives each level, the game will be won.

- Extra lives:
  > Added by J. Glyn-Cuthbert
  > If a player, in multiplayer mode, is terminated but the other player survives, the player that was terminated will be given an extra life at the beginning of the next level.

- Improved graphics:
  > Added by MK. Von Eschwege and J. Glyn-Cuthbert 
  > A background PNG file that has been editted for btter looking fonts.
  > The Enemies, Player, Missiles and Bunker objects graphics are PNG files with transparent backgrounds and are instance variables of each object.

- Enemies Counterattack:
  > Added by MK. Von Eschwege

- Hitpoints:
  > Added by MK. Von Eschwege and J. Glyn-Cuthbert
  > ' Enemies ' and ' Player ' objects have hitpoints.
  > When the third level is reached the enemies are initialized with two hitpoints instead of one.

- Bunkers:
  > Added by MK. Von Eschwege

- Different missile types:
  > Added by MK. Von Eschwege
  > Enemies have differing missiles to the players 



GRAPHICS AND SOUNDS CREDITS

- All enemy, player and missile graphics can be found at " istockphoto.com/search/2/image-film?phrase=space+invaders+game " (these graphics are non-copyright).
- The background graphic can be found at " freepik.com/free-photos-vectors/space " (this picture is non-copyright) and was edited by MK. Von Eschwege in the online editor Canva.
- The backtrack is from "https://pixabay.com/music/search/arcade/", track name: 8-bit Arcade mode
- The pew sound is from "https://pixabay.com/sound-effects/search/star%20wars/", track name: BLASTER 2, and was shortened by MK Von Eschwege
                                               
                                               