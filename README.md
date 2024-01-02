# Ascension

Program that runs the game, Ascension

# Features

Player can select different characters to play as. Player uses character to shoot enemies and destroy them. The goal for the player is to progress as far as possible. The player beats the game upon reaching the sixth stage.

To shoot, press the spacebar. To use your skill, press f. To move, use WASD or arrow leys.

# Installation

* Pygame Zero
  ```
  import pgzero
  ```
  To install pygame zero, run the following command
  ```
  pip install pgzero
  ```
* Time
  ```
  import time
  ```
* Random
  ```
  import random
  ```

# Known Bugs

* When there are many entities on the screen, the game may lag a bit. Further optimization may be required
* Hit boxes are not completely accurate - they are approximated with convenient shapes to use, such as circles or rectangles. Work on collision is needed.
  * These hit boxes include hit boxes for player, enemy, skills, portal, and buttons to navigate through the game.
* Explosion animations stay in place rather than following the enemy/player
  * For deaths, it is not a problem. But for targets that still live after being hit, the explosion will appear to move on the target's sprite, perhaps even moving off it, as the target can continue to move while the explosion does not.
* Enemy spawn is completely random, meaning that player can go quite a while without seeing an enemy.

# Sources

### Sites used for Learning
| Site | Purpose |
|-|-|
| D. Pope, “Introduction to pygame zero¶,” Introduction to Pygame Zero - Pygame Zero 1.2.1 documentation, 03-Jan-2022. [Online]. Available: https://pygame-zero.readthedocs.io/en/stable/introduction.html. [Accessed: 23-Jun-2022]. | To understand how to use Pygame Zero. |
| “Expanding tuples into arguments,” Stack Overflow, Jan-2010. [Online]. Available: https://stackoverflow.com/questions/1993727/expanding-tuples-into-arguments. [Accessed: 23-Jun-2022]. | Was used because of a bug in functions. In the end, I did not need to use this. However, I still learned some stuff. |

### Images
| Source | Description |
|-|-|
| Fire Emblem Heroes. Mobile. Japan: Nintendo, 2017. | Sprite for Crusader. |
| Arknights. Mobile. Japan: Yostar Limited, 2019. | Sprite for Weedy and Rosmontis. |
| 9664c4, Explosion. Pixel Art Maker, 2017. | Explosion for enemy destruction. |
| 9664c4, Explosion. Pixel Art Maker, 2019. | Explosion upon bullet contact. |
| 9664c4, Portal. Pixel Art Maker, 2019. | Portal to go to the next level. |
| Fujiro, Wave. KindPng. | Image for Rosmontis’ skill. |
| Heyimhevel, Seraph. Giphy, 2021. | Sprite for enemy. |
| P. Charitos, Black Hole. Cerncourier, 2019. | Image for end game screen. |
| scrixels, Ophanim. Twitter, 2020. | Sprite for enemy. |
| Water Dragon. Newgrounds. | Image for Weedy’s skill.|
