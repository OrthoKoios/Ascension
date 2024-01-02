# ---------------------------------------
# Justin Dai
# Ascension Game
# ICS3U Final Project
# ---------------------------------------






# ---------------------------------------
# Importing necessary files
# ---------------------------------------

import pgzrun
import time
import random






# ---------------------------------------
# Title
# ---------------------------------------

TITLE = "Ascension"






# ---------------------------------------
# Dimensions
# ---------------------------------------

WIDTH = 1000
HEIGHT = 500






# ---------------------------------------
# Events
# ---------------------------------------

event = 'menu'
# Other events are 'game', 'exit', 'instructions', 'character_selection', different character info pages, and 'level'


# ---------------------------------------
# Indicators
# ---------------------------------------

# Dictionary of indicators to track when they should be drawn
indicators = {
  'menu_begin' : False,
  'menu_instructions' : False,
  'back_button' : False,
  'level_continue' : False,
  'char_info_1' : False,
  'char_info_2' : False,
  'char_info_3' : False,
  'char_commence_1' : False,
  'char_commence_2' : False,
  'char_commence_3' : False
}






# ---------------------------------------
# Necessary Values in Code
# Makes easier readability in code
# ---------------------------------------

# Bullet Radius
bullet_rad = 5
# Bullet speed
bullet_spd = 7
# Enemy move speed
enemy_spd = 1
# ATK interval for enemy
enemy_shoot_interval = 2.0
# Background movespeed
background_spd = 10
# Offset so the bullet comes out of the nose of the plane
player_bullet_offset = 7
# Offset so player destruction explosion is centered
player_destruct_explosion_offset = [100, 100]






# ---------------------------------------
# Backgrounds
# Includes:
#   Backgrounds
#   Background animations
# ---------------------------------------

# x-coordinate of background
background_pos = 0

def background_animation():
  '''
  Moves the background to give the illusion of moving forward.

  Parameters:
    None.
  Returns:
    None.
  '''
  global background_pos
  # Draws background, changes based on level
  if player.LEVEL < 6:
    screen.blit('background_2', (background_pos, 0))
  else:
    screen.blit('background_1', (background_pos, 0))
  # Moving background
  background_pos -= background_spd
  # Looping
  if background_pos <= -WIDTH:
    background_pos = 0




    
# ---------------------------------------
# Player Character
# Includes:
#    - player sprite
#    - initializing player stats
#    - variables necessary for player movement
# ---------------------------------------

# Sprite
player = Actor('no_sprite', anchor = ('right', 'center'), center = (0, HEIGHT // 2))
# Character
player.character = None

# Upgrades player has unlocked for each character
# First letter of character's name
# Note that Crusader has 'j' because the original name was Julia
player.upgrades = {
  'w' : [False, False, False],
  'r' : [False, False, False],
  'j' : [False, False, False]
}

# Player movement
player.move_right = False
player.move_left = False
player.move_up = False
player.move_down = False

# Player bullets that have been fired
player.curr_bullets = []
player.skill_projectile = []
# Skill effects
player.skill_effects = []

# Player status
player.ALIVE = True

# Player kills per playthrough  
player.KILLS = 0  

# Player stats
player.MAX_HITPOINTS = None
player.HITPOINTS = None
player.ATTACK = None
player.MOVE_SPEED = None
player.ATTACK_SPEED = None
player.SKILL_POINTS = None
player.SKILL_BAR = None
player.SKILL_REFUND = None

# Times when player shot
player.last_shot_time = -float('inf')
player.curr_shot_time = 0

# Player current level and furthest player progressed
# Due to how levels are displayed, first level is "level 0"
# Therefore, greatest ascent starts at -1
player.LEVEL = 0
player.GREATEST_ASCENT = -1

# Time when player starts
player.level_start_time = None







# ---------------------------------------
# Player Actions
# Includes:
#   - player movement
#   - shooting
# ---------------------------------------

# ---------- Update player movement ---------- #
def cmd_player_move(key):
  '''
  Makes player sprite move upon pressing arrow keys

  Parameters:
    key (enum): the arrow key being pressed

  Returns:
    None
  '''
  # If key is pressed, player sprite moves in that direction
  # Using if statements so user can press multiple keys at once
  if key == keys.RIGHT or key == keys.D:
    player.move_right = True
  if key == keys.LEFT or key == keys.A:
    player.move_left = True
  if key == keys.UP or key == keys.W:
    player.move_up = True
  if key == keys.DOWN or key == keys.S:
    player.move_down = True

def cmd_player_stop(key):
  '''
  Makes player sprite stop upon releasing arrow keys

  Parameters:
    key (enum): the arrow key being released

  Returns:
    None
  '''
  # If key is released, player stops moving in that direction
  # Using if statements so user can release several keys at once
  if key == keys.RIGHT or key == keys.D:
    player.move_right = False
  if key == keys.LEFT or key == keys.A:
    player.move_left = False
  if key == keys.UP or key == keys.W:
    player.move_up = False
  if key == keys.DOWN or key == keys.S:
    player.move_down = False

# ---------- Player movement ---------- #
def player_movement():
  '''
  Updates player location

  Parameters:
    None
  
  Returns:
    None
  '''
  # Testing, REMOVE LATER PLEASE
  #print(f'''
  #          {player.move_up}
  #     {player.move_left}     {player.move_right}
  #          {player.move_down}
  #      ''')

  # Player movement
  # Using if statements so user can move multiple directions at same time
  # e.g. up and right for diagonal movement
  if player.move_right:
    player.right += player.MOVE_SPEED
  if player.move_left:
    player.left -= player.MOVE_SPEED
  if player.move_up:
    player.top -= player.MOVE_SPEED
  if player.move_down:
    player.bottom += player.MOVE_SPEED
  
  # Checks if player will move out of boundaries and prevents this
  # Uses if statements, in case player exceeds several boundaries at same time
  if player.right > WIDTH:
    player.right = WIDTH
  if player.left < 0:
    player.left = 0
  if player.top < 0:
    player.top = 0
  if player.bottom > HEIGHT:
    player.bottom = HEIGHT

# ---------- Shooting system ---------- #
def cmd_player_shoot(key):
  '''
  Makes player sprite shoot upon hitting space bar

  Parameters:
    key (enum): the key being pressed

  Returns:
    None
  '''
  # If space key is pressed, player shoots
  if key == keys.SPACE:
    # Checks current time
    player.curr_shot_time = time.time()
    # Sees if the time from the last shot is larger than the attack speed interval
    # If it is, then player can shoot
    if player.curr_shot_time - player.last_shot_time > player.ATTACK_SPEED:
      # Adds bullet location to bullets array
      # offset for the bullet so the animation is nice
      player.curr_bullets.append({'x' : player.x, 'y' : player.y + player_bullet_offset})
      player.last_shot_time = player.curr_shot_time

def player_bullet_movement():
  '''
  Has all the bullets move after being shot

  Parameters:
    None
  Returns:
    None
  '''
  # Iterator to move through array of bullets
  
  bullet_iter = 0
  # All the player bullets continuosly move right over time
  while bullet_iter < len(player.curr_bullets):
    # Bullet speed is ___ pixels per update
    player.curr_bullets[bullet_iter]['x'] += bullet_spd
    # Remove bullet if it is out of bounds
    # Adds bullet_rad as bullet.x is center of bullet
    if player.curr_bullets[bullet_iter]['x'] > WIDTH + bullet_rad:
      player.curr_bullets.remove(player.curr_bullets[bullet_iter])
      # Make sure that removed bullet is no longer used for anything else with continue statement
      # Proceed to next bullet
      continue
    # Proceed to next bullet
    bullet_iter += 1

# ---------- Skill ---------- #
def cmd_activate_player_skill(key):
  '''
  Activtes player's skill

  Parameters:
    key (enum): button to be pressed by player
  Returns:
    None
  '''
  # >= in case SP exceeds skill bar
  if player.SKILL_POINTS >= player.SKILL_BAR:
    if key == keys.F:
      # Resets skill points
      player.SKILL_POINTS = 0
      # Skill based on character selected
      if player.character == 'w':
        player.skill_projectile.append(Actor('weedy_skill', Anchor = ('left', 'center'), midleft = (player.x, player.y)))
      elif player.character == 'r':
        player.skill_projectile.append(Actor('rosmontis_skill', Anchor = ('left', 'center'), midleft = (player.x, player.y)))
      else:
        player.ATTACK = 5000
        player.ATTACK_SPEED = 0
        player.MOVE_SPEED = 6
        # Prevents effect from being drawn several times
        if not player.skill_effects:
          player.skill_effects.append(Actor('julia_skill_indicator'))
        clock.schedule_unique(remove_player_skill_effects, 5.0)

def player_skill_movement():
  '''
  Animates player skill and checks for collision between skill and enemies

  Parameters:
    None
  Returns:
    None
  '''
  # Iterator to move through array of projectiles
  proj_iter = 0
  
  while proj_iter < len(player.skill_projectile):
    player.skill_projectile[proj_iter].x += bullet_spd
    # if projectile is out of bounds, remove it
    if player.skill_projectile[proj_iter].left > WIDTH:
      player.skill_projectile.remove(player.skill_projectile[proj_iter])
      # Continue statement for safety
      # Proceed to next projectile
      continue
    # Different skills do different things
    if player.character == 'w':
      enemy_iter = 0
      while enemy_iter < len(curr_enemies):
        if player.skill_projectile[proj_iter].colliderect(curr_enemies[enemy_iter][0]):
          # Player gets kill, so increment to kill tracker
          player.KILLS += 1
          # Each kill from the skill refunds SP
          player.SKILL_POINTS += player.SKILL_REFUND
          # Explosion animation
          # Centered on enemy
          destruc_explosion(curr_enemies[enemy_iter][0].center[0], curr_enemies[enemy_iter][0].center[1])
          curr_enemies.remove(curr_enemies[enemy_iter])
          # Skill can pass through enemies
          # Continue statement so removed enemy is not used for anything else
          # Continue to next enemy
          continue
        enemy_iter += 1
      proj_iter += 1
    elif player.character == 'r':
      for enemy in curr_enemies:
        if player.skill_projectile[proj_iter].colliderect(enemy[0]):
          # An enemy is hit
          enemy[2] -= player.ATTACK * 5
          # Shockwave is created
          player.skill_effects.append(Actor('rosmontis_skill_shockwave', center = (player.skill_projectile[proj_iter].right, player.skill_projectile[proj_iter].y)))
          # Schedules shockwave to be removed
          clock.schedule(remove_player_skill_effects, 1.5)
          # Checks for enemies that are hit by skill shockwave
          enemy_iter = 0
          while enemy_iter < len(curr_enemies):
            # Hits all enemies in explosion
            if (curr_enemies[enemy_iter][0].center[0] - player.skill_projectile[proj_iter].right)**2 + (curr_enemies[enemy_iter][0].center[1] - player.skill_projectile[proj_iter].y)**2 <= 22500:
              # Shockwave damage
              curr_enemies[enemy_iter][2] -= player.ATTACK * 2
              # Checks for dead enemies
              # Note that this also checks if the originally hit enemy is dead
              if curr_enemies[enemy_iter][2] <= 0:
                # Player gets kill, so increment to kill tracker
                player.KILLS += 1
                # Each kill from the skill refunds SP
                player.SKILL_POINTS += player.SKILL_REFUND
                # Explosion animation
                # Centered on enemy
                destruc_explosion(curr_enemies[enemy_iter][0].center[0], curr_enemies[enemy_iter][0].center[1])
                curr_enemies.remove(curr_enemies[enemy_iter])
                # Continue statement so removed enemy is not used for anything else
                # Continue to next enemy
                continue
            enemy_iter += 1
          # Projectile only hits one enemy
          player.skill_projectile.remove(player.skill_projectile[proj_iter])
          # Break statement so removed projectile is not used for anythine else
          # Continue to next projectile
          break
      proj_iter += 1

def remove_player_skill_effects():
  '''
  Removes effects from skills, such as animations or buffs.

  Parameters:
    None
  Returns:
    None
  '''
  if player.character == 'r':
    # Removes the shockwave
    # Oldest shockwave will be the first element
    # Similar to queue
    # Makes sure the list is not empty, just in case
    if player.skill_effects:
      player.skill_effects.pop(0)
  elif player.character == 'j':
    # Reset stats from Crusader's skill and removes the skill indicator
    player.skill_effects.clear()
    if player.upgrades[player.character][0]:
      player.ATTACK = 200
    else:
      player.ATTACK = 100
    player.ATTACK_SPEED = 1.5
    if player.upgrades[player.character][1]:
      player.MOVE_SPEED = 4
    else:
      player.MOVE_SPEED = 1
          
# ---------- Drawings ---------- #
def draw_player_assets():
  '''
  Draws character sprite and player bullets
  
  Parameters:
    None
  Returns:
    None
  '''
  player.draw()
  # Draws bullets
  for bullet in player.curr_bullets:
    screen.draw.filled_circle((bullet['x'], bullet['y']), bullet_rad, (0, 191, 255))
  # Draws skill projectile
  for projectile in player.skill_projectile:
    projectile.draw()
  for effect in player.skill_effects:
    effect.draw()

# Bars and score are top left corner, starting at 10, 10, each 
# 10 pixels tall, with 10 pixels separating each bar/text
def display_player_hp_bar():
  '''
  Player loses game upon hp bar becomes 0
  Draws player current hp bar

  Parameters:
    None
  Returns:
    None
  '''
  # Player loses upon no hp
  # <= as hp could be reduced to a negative number
  if player.HITPOINTS <= 0:
    player.ALIVE = False
    # Player explodes
    # The image is offset so the explosion is on the ship
    screen.blit('death_explosion', (player.left - player_destruct_explosion_offset[0], player.top - player_destruct_explosion_offset[1]))
    # Death text
    screen.draw.text("You Died!", (200, 150), fontsize = 200, color = (255, 255, 255), owidth = 3, ocolor = 'black')
    # Exits
    clock.schedule(cmd_end_game, 4.0)
  
  # Amount HP left relative to MAX HP bar
  # Min and max functions to ensure percent hp is a valid percentage, i.e. it is not greater than max hitpoints and not less than 0
  percent_hp = min(max(int(player.HITPOINTS / player.MAX_HITPOINTS * 300), 0), 300)
  # Max HP bar
  empty_bar = Rect((10, 10), (300, 10))
  # Curr HP bar
  hp_bar = Rect((10, 10), (percent_hp, 10))
  # Draws HP bars
  screen.draw.filled_rect(empty_bar, (220, 220, 220))
  screen.draw.filled_rect(hp_bar, (80, 200, 120))
  # Displays number of hit points
  # max function prevents a negative number from displaying
  screen.draw.text(f"{max(player.HITPOINTS, 0)}/{player.MAX_HITPOINTS}", (10, 10), fontsize = 18, color = (0, 0, 0))

def display_player_skill_bar():
  '''
  Draws player skill bar, as well as recharging it.

  Parameters:
    None
  Returns:
    None
  '''
  # Amount skill points relative to skill points needed
  # Min and max functions to ensure the percentage is a valid number, i.e. it isn't greater than skill bar or less than 0
  percent_skill_bar = min(max(int(player.SKILL_POINTS / player.SKILL_BAR * 300), 0), 300)
  # Max skill bar
  empty_bar = Rect((10, 30), (300, 10))
  # Curr skill points
  skill_bar = Rect((10, 30), (percent_skill_bar, 10))
  # Draws skill bars
  screen.draw.filled_rect(empty_bar, (220, 220, 220))
  screen.draw.filled_rect(skill_bar, (216, 161, 117))
  # Displays when skill is ready
  if player.SKILL_POINTS >= player.SKILL_BAR:
    screen.draw.text("SKILL READY!!!", (10, 30), fontsize = 18, color = (139 ,0 ,0))
  # Otherwise, skill is not ready
  # Recharge skill
  else:
    # Only recharges if player is alive
    # Otherwise. player sees bar regening while player is dead, which is kinda awkward
    if player.ALIVE:
      player.SKILL_POINTS += 1

def display_level_and_kills():
  '''
  Draws player's current level and kills

  Parameters:
    None
  Returns:
    None
  '''
  screen.draw.text(f"Level: {player.LEVEL // 3 + 1}-{player.LEVEL % 3 + 1}", (10, 50), fontsize = 18, color = (255, 255, 255))
  screen.draw.text(f"Kills: {player.KILLS}", (10, 70), fontsize = 18, color = (255, 255, 255))











  
# ---------------------------------------
# Enemy Actions
# Includes:
#   - spawn rate
#   - snemy shooting
#   - collision
# ---------------------------------------

# Existing enemies
# 2D List
  # element 0 stores the enemy sprite + location
  # element 1 stores the last time enemy fired a bullet
  # element 2 stores enemy hp
  # element 3 stores enemy atk
  # element 4 stores enemy type
curr_enemies = []
# Existing enemy bullets
curr_enemy_bullets = []

# ---------- Spawning Enemies ---------- #
def spawn_enemies(difficulty):
  '''
  Spawns enemies randomly

  Parameters:
    difficulty (int): the spawn rate of enemies
  Returns:
    None
  '''
  # Spawns enemies at a random interval
  if random.randint(1, 1000) <= difficulty:
    # randomly spawns different enemy types
    if random.randint(1, 6) < 6:
      enemy = Actor('enemy_1', anchor = ('right', 'center'))
      enemy.x = WIDTH
      enemy.y = random.randint((enemy.bottom - enemy.top) // 2, HEIGHT - (enemy.bottom - enemy.top) // 2)
      # Enemy stats scale with level
      curr_enemies.append([enemy, -float('inf'), 200 + player.LEVEL * 20, 100 + player.LEVEL * 10, 1])
    else:
      enemy = Actor('enemy_2', anchor = ('right', 'center'))
      enemy.x = WIDTH
      enemy.y = random.randint((enemy.bottom - enemy.top) // 2, HEIGHT - (enemy.bottom - enemy.top) // 2)
      # Enemy stats scale with level
      curr_enemies.append([enemy, -float('inf'), 300 + player.LEVEL * 100, 100 + player.LEVEL * 5, 2])


# ---------- Enemies Actions ---------- #
def enemy_movement():
  '''
  Has enemies make actions such as shooting and moving
  Also checks for collision between enemies and player bullets

  Parameters:
    None
  Returns:
    None
  '''
  enemy_iter = 0
  
  while enemy_iter < len(curr_enemies):
    # Enemy shoots
    enemy_shoot(curr_enemies[enemy_iter])
    # Moves enemy left
    # Rammers move thrice as fast
    if curr_enemies[enemy_iter][4] == 1:
      curr_enemies[enemy_iter][0].x -= enemy_spd
    else:
      curr_enemies[enemy_iter][0].x -= enemy_spd * 3
    # Checks if enemy is out of screen, and removes said enemy if so
    if curr_enemies[enemy_iter][0].x < 0:
      curr_enemies.remove(curr_enemies[enemy_iter])
      # Continue statement for safety
      # Ensures that removed enemy is not used for anything else
      # Continue to next enemy
      continue
    # Checks if player collides with enemy
    # If so, enemy ship explodes, dealing damage to player
    if player.colliderect(curr_enemies[enemy_iter][0]):
      # Player gets kill, so add to kill tracker
      player.KILLS += 1
      # Player takes damage based on enemy type
      if curr_enemies[enemy_iter][4] == 1:
        # Takes 300 dmg if its a shooter enemy
        player.HITPOINTS -= 300
      else:
        # Takes more damage from ramming enemies
        player.HITPOINTS -= 300 + curr_enemies[enemy_iter][3]
      destruc_explosion(curr_enemies[enemy_iter][0].center[0], curr_enemies[enemy_iter][0].center[1])
      curr_enemies.remove(curr_enemies[enemy_iter])
      # Continue statement for safety
      # Continue to next enemy
      continue

    bullet_iter = 0
    # If enemy collides with player bullet, enemy takes damage
    while bullet_iter < len(player.curr_bullets):
      # Detects collision
      # I did not use collidepoint so if the bullet grazes the enemy it also counts as a hit
      if (curr_enemies[enemy_iter][0].top - bullet_rad < player.curr_bullets[bullet_iter]['y'] < curr_enemies[enemy_iter][0].bottom + bullet_rad) and (curr_enemies[enemy_iter][0].left - bullet_rad < player.curr_bullets[bullet_iter]['x'] < curr_enemies[enemy_iter][0].right + bullet_rad):
        # Bullet explosion
        bullet_explosion(player.curr_bullets[bullet_iter]['x'], player.curr_bullets[bullet_iter]['y'])
        curr_enemies[enemy_iter][2] -= player.ATTACK
        # Enemy is removed if enemy has no HP left
        if curr_enemies[enemy_iter][2] <= 0:
          # Player gets kill
          player.KILLS += 1
          # During Crusader's skill, if she kills an enemy using bullets, she gets skill refund and some hp
          # I can identify when the skill is active by checking if the skill indicator is empty or not
          if player.character == 'j' and player.skill_effects:
            player.SKILL_POINTS += player.SKILL_REFUND
            # Prevent HP from going above max
            player.HITPOINTS = min(player.HITPOINTS + 50, player.MAX_HITPOINTS)
          # Explosion animation
          # Centered on enemy
          destruc_explosion(curr_enemies[enemy_iter][0].center[0], curr_enemies[enemy_iter][0].center[1])
          # Enemy is dead
          curr_enemies.remove(curr_enemies[enemy_iter])
          # Bullets can only hit one enemy
          player.curr_bullets.remove(player.curr_bullets[bullet_iter])
          # Break statement so removed enemy and bullet are not used for anything else
          # Continues to next enemy
          break
        # Bullets can only hit one enemy
        # I could put the removal at the start of this block of code only once, but because of organization reasons I put it twice near the break and continue statements
        # Also, I must use a break statement if the enemy is killed, so it is easier to put two different removals for two different cases
        player.curr_bullets.remove(player.curr_bullets[bullet_iter])
        # Continue statement so removed bullet is not used for anything else
        # Continue to next bullet
        continue
      bullet_iter += 1
    enemy_iter += 1

# ---------- Enemies Shooting ---------- #
def enemy_shoot(enemy):
  '''
  Has enemy fire a bullet

  Parameters:
    enemy (object, class: Actor): enemy shooting bullet
  Returns:
    None
  '''
  # Enemy only shoots if it is a shooting enemy
  if enemy[4] == 1:
    # Enemy shooting interval is at least [enemy_shoot_interval] seconds
    if time.time() - enemy[1] > enemy_shoot_interval:
      # 10 percent chance to shoot per update
      # slightly randomizes shooting
      if random.randint(1, 50) == 1:
        enemy[1] = time.time()
        # Bullet location initialized at the front of each enemy
        # Bullet is a dictionary with x and y coordinates and damage depending on enemy attack
        curr_enemy_bullets.append({'x' : enemy[0].left, 'y' : enemy[0].y, 'dmg' : enemy[3]})

# ---------- Enemy Bullet Movement ---------- #
def enemy_bullet_movement():
  '''
  Moves enemy bullets, checks for collision between player and bullet

  Parameters:
    None
  Returns:
    None
  '''
  bullet_iter = 0
  
  while bullet_iter < len(curr_enemy_bullets):
    # Moves bullets
    curr_enemy_bullets[bullet_iter]['x'] -= bullet_spd
    # If bullet out of bounds, remove it
    if curr_enemy_bullets[bullet_iter]['x'] < 0:
      curr_enemy_bullets.remove(curr_enemy_bullets[bullet_iter])
      # Continue statement for safety
      # Move to next bullet
      continue
    # Collision between player and bullet
    # Did not use collide point so if bullet grazes you, it counts as damage
    if (player.top - bullet_rad < curr_enemy_bullets[bullet_iter]['y'] < player.bottom + bullet_rad) and (player.left - bullet_rad < curr_enemy_bullets[bullet_iter]['x'] < player.right + bullet_rad):
      player.HITPOINTS -= curr_enemy_bullets[bullet_iter]['dmg']
      bullet_explosion(curr_enemy_bullets[bullet_iter]['x'], curr_enemy_bullets[bullet_iter]['y'])
      curr_enemy_bullets.remove(curr_enemy_bullets[bullet_iter])
      # Continue statement for safety
      # Proceed to next bullet
      continue
    bullet_iter += 1

# ---------- Drawing Enemies and Bullets ---------- #
def draw_enemy_assets():
  '''
  Draws bullets and enemies

  Parameters:
    None
  Returns:
    None
  '''
  for enemy in curr_enemies:
    enemy[0].draw()
  for bullet in curr_enemy_bullets:
    screen.draw.filled_circle((bullet['x'], bullet['y']), bullet_rad, (255, 0, 0))












    
# ---------------------------------------
# Animations
# Includes:
#   - different explosions
#   - sprite changes
# ---------------------------------------

# ---------- Explosions ---------- #
# Stores all the explosions caused by death
destruction_explosions = []
# Stores all the explosions caused by bullet collision
bullet_explosions = []
# These lists act as queues

def destruc_explosion(x, y):
  '''
  Explosion that occurs upon destruction of player or enemy

  Parameters:
    x (int): x coordinate of explosion
    y (int): y coordinate of explosion
  '''
  destruction_explosions.append(Actor('destruction_explosion', center = (x, y)))
  # Explosion lasts for 1 second
  clock.schedule(destruc_explosion_removal, 1.0)
    
def destruc_explosion_removal():
  '''
  Removes explosion

  Parameters:
    None
  Returns:
    None
  '''
  # All explosions here last the same length, so we can use a queue to remove an explosion when the time has come
  # Checks if list contains items. That way, no error occurs when list is cleared after game ends or level is beat. While I do unschedule these removals, during testing, sometimes this error still occurs. I add this for safety.
  if destruction_explosions:
    destruction_explosions.pop(0)

def bullet_explosion(x, y):
  '''
  Explosion that occurs upon bullet collision
  
  Parameters:
    x (int): x coordinate of explosion
    y (int): y coordinate of explosion
  '''
  bullet_explosions.append(Actor('bullet_explosion', center = (x, y)))
  # Explosion lasts for 0.2 seconds
  clock.schedule(bullet_explosion_removal, 0.2)

def bullet_explosion_removal():
  '''
  Removes explosion

  Parameters:
    None
  Returns:
    None
  '''
  # All explosions here last the same length, so we can use a queue to remove an explosion when the time has come
  # Checks if list contains items. That way, no error occurs when list is cleared after game ends or level is beat. While I do unschedule these removals, during testing, sometimes this error still occurs. I add this for safety.
  if bullet_explosions:
    bullet_explosions.pop(0)

def draw_explosions():
  '''
  Draws all explosions

  Parameters:
    None
  Returns:
    None
  '''
  for explosion in bullet_explosions:
    explosion.draw()
  for explosion in destruction_explosions:
    explosion.draw()

# ---------- Character Sprite Animations ---------- #
def character_animation():
  '''
  Animates the player sprite

  Parameters:
    None
  Returns:
    None
  '''
  # Switches sprite every 2 seconds
  # Depends on character chosen
  if player.character == 'w':
    if (time.time() // 1) % 4 < 2:
      player.image = 'weedy_sprite_1'
    else:
      player.image = 'weedy_sprite_2'
  elif player.character == 'r':
    if (time.time() // 1) % 4 < 2:
      player.image = 'rosmontis_sprite_1'
    else:
      player.image = 'rosmontis_sprite_2'
  else:
    if (time.time() // 1) % 4 < 2:
      player.image = 'julia_sprite_1'
    else:
      player.image = 'julia_sprite_2'





    


# ---------------------------------------
# Menu
# Includes:
#   - Button to start game (go to character selection screen)
#   - Button to go to instructions
#   - End game command that sends user to menu
# ---------------------------------------

# ---------- Draw Menu ---------- #
def display_menu():
  '''
  Draws the menu

  Parameters:
    None
  Returns:
    None
  '''
  # Draws menu screen and buttons
  screen.blit('menu_screen', (0, 0))
  # Greatest ascent tracks the highest level that has been cleared.
  # The level to reach to beat the game is 6-1, i.e. 15
  # Thus, we check if the player has cleared 5-3, i.e. 14
  # >= just in case
  if player.GREATEST_ASCENT >= 14:
    screen.draw.text(f"Greatest Ascent: -", (760, 20), fontsize = 26, color = (0, 0, 0))
  # Checks if player has played the game or has beaten the game
  elif player.GREATEST_ASCENT > -1:
    screen.draw.text(f"Greatest Ascent: {player.GREATEST_ASCENT // 3 + 1}-{player.GREATEST_ASCENT % 3 + 1}", (760, 20), fontsize = 26, color = (0, 0, 0))
  else:
    screen.draw.text(f"Greatest Ascent: the ground", (760, 20), fontsize = 26, color = (0, 0, 0))

  # Indicators
  if indicators['menu_begin']:
    screen.blit('begin_indicator', (367, 388))
  if indicators['menu_instructions']:
    screen.blit('instruct_indicator', (936, 433))
    
# ---------- Character Selection ---------- #
def cmd_goto_character_selection_screen(pos):
  '''
  Go to character selection screen

  Parameters:
    pos (tuple): The location that player clicked
  Returns:
    None
  '''
  # The current event player is experiencing
  global event

  # If start button is pressed, go to character selection screen
  if (460 <= pos[0] <= 570) and (420 <= pos[1] <= 470):
    event = 'character_selection'

# ---------- End Game ---------- #
def cmd_end_game():
  '''
  Once player wins or dies, the game ends, resetting all the values and updating scores
  
  Parameters:
    None
  Returns:
    None
  '''
  # Current event
  global event
  # Location of background
  global background_pos

  # Unlocks upgrades
  # Checks if upgrade has not been unlocked
  if not player.upgrades[player.character][0]:
    # Player gets first upgrade by reaching stage 2 with that character
    if player.LEVEL >= 3:
      player.upgrades[player.character][0] = True
  # Checks if upgrade has not been unlocked
  if not player.upgrades[player.character][1]:
    # Player gets second upgrade by getting 150 kills with that character in 1 playthrough
    if player.KILLS >= 60:
      player.upgrades[player.character][1] = True
  # Checks if upgrade has not been unlocked
  if not player.upgrades[player.character][2]:
    # Player gets third upgrade by reaching stage 4 with that character
    if player.LEVEL >= 9:
      player.upgrades[player.character][2] = True
      
  
  # Reset sprite image
  player.image = 'no_sprite'
  
  # Reset positions
  background_pos = 0
  player.pos = 0, HEIGHT // 2

  # Reset player status
  player.ALIVE = True
  
  # Update greatest ascent
  # Level is subtracted by 1, as player greatest ascent is the furthest level player cleared
  if player.LEVEL - 1 > player.GREATEST_ASCENT:
    player.GREATEST_ASCENT = player.LEVEL - 1

  # Reset level
  player.LEVEL = 0
    
  # Reset kills
  player.KILLS = 0
    
  # Reset player movement
  player.move_right = False
  player.move_left = False
  player.move_up = False
  player.move_down = False

  # Reset projectiles
  player.curr_bullets.clear()
  player.skill_projectile.clear()
  # Reset skill effects
  player.skill_effects.clear()
  
  # Resets all of player's stats to None
  player.MAX_HITPOINTS = None
  player.HITPOINTS = None
  player.ATTACK = None
  player.MOVE_SPEED = None
  player.ATTACK_SPEED = None
  player.SKILL_POINTS = None
  player.SKILL_BAR = None
  player.SKILL_REFUND = None
  
  # Reset times of shooting
  player.last_shot_time = -float('inf')
  player.curr_shot_time = 0

  # Reset enemies
  curr_enemies.clear()
  curr_enemy_bullets.clear()

  # Reset all destructions
  destruction_explosions.clear()
  bullet_explosions.clear()

  # Update event
  event = 'menu'

  # Resets level start time
  player.level_start_time = None
  
  # Unschedules any game events that are still scheduled
  clock.unschedule(remove_player_skill_effects)
  clock.unschedule(destruc_explosion_removal)
  clock.unschedule(bullet_explosion_removal)
  clock.unschedule(cmd_end_game)
  
# ---------- Instructions ---------- #
def cmd_goto_instructions(pos):
  '''
  Sends player to instructions screen upon pressing instructions button

  Parameters:
    pos (tuple): The location that player clicked
  Returns:
    None
  '''
  # The current event player is experiencing
  global event

  # If instructions button is pressed, go to instructions page
  if (920 <= pos[0] <= 970) and (430 <= pos[1] <= 470):
    event = 'instructions'










# ---------------------------------------
# Sub-menu screens
# Includes:
#   - Instructions
#   - Character Selection Screen
#   - Character Info Screen
# ---------------------------------------

# ---------- Draw Instructions Menu ---------- #
def display_instructions():
  '''
  Displays a screen telling player the instructions.

  Parameters:
    None
  Returns:
    None
  '''
  screen.blit('instructions', (0, 0))

  # Indicators
  if indicators['back_button']:
    screen.blit('back_indicator', (880, 0))

# ---------- Returning to main menu ---------- #
def cmd_go_back_menu(pos):
  '''
  Sends player back to menu from instructions page

  Parameters:
    pos (tuple): The location that player clicked
  Returns:
    None
  '''
  # The current event player is experiencing
  global event

  # If back button is pressed, go to menu 
  if (880 <= pos[0] <= 1000) and (0 <= pos[1] <= 50):
    event = 'menu'

# ---------- Draw Character Selection Screen Menu ---------- #
def display_character_selection_screen():
  '''
  Displays a screen that allows player to select a character, as well as displaying upgrades

  Parameters:
    None
  Returns:
    None
  '''
  screen.blit('character_selection_screen', (0, 0))

  # Indicators
  if indicators['back_button']:
    screen.blit('back_indicator', (880, 0))
  if indicators['char_info_1']:
    screen.blit('info_indicator', (278, 107))
  if indicators['char_info_2']:
    screen.blit('info_indicator', (539, 100))
  if indicators['char_info_3']:
    screen.blit('info_indicator', (788, 98))
  if indicators['char_commence_1']:
    screen.blit('commence_indicator', (120, 350))
  if indicators['char_commence_2']:
    screen.blit('commence_indicator', (380, 350))
  if indicators['char_commence_3']:
    screen.blit('commence_indicator', (640, 350))

# ---------- Exit Character Selection Screen ---------- #
def cmd_exit_char_select(pos):
  '''
  Exits character selection screen if user wishes. Goes back to menu

  Parameters:
    pos (tuple): place where player clicks
  Returns:
    None
  '''
  global event

  if (880 <= pos[0] <= 1000) and (0 <= pos[1] <= 50):
    # Update event
    event = 'menu'
  
# ---------- Start Game ---------- #
def cmd_start_game(pos):
  '''
  Starts game after selecting a character

  Parameters:
    pos (tuple): place where player clicks
  Returns:
    None
  '''
  # current event
  global event

  # If character is selected, starts game
  if (120 <= pos[0] <= 350) and (350 <= pos[1] <= 385):
    # Sets player sprite and stats based on character chosen
    player.character = 'w'
    player.image = 'weedy_sprite_1'
    player.MAX_HITPOINTS = 3000
    player.HITPOINTS = player.MAX_HITPOINTS
    player.ATTACK = 500
    if player.upgrades[player.character][0]:
      player.MOVE_SPEED = 5
    else:
      player.MOVE_SPEED = 1
    if player.upgrades[player.character][1]:
      player.ATTACK_SPEED = 1
    else:
      player.ATTACK_SPEED = 4
    player.SKILL_POINTS = 0
    player.SKILL_BAR = 2000
    if player.upgrades[player.character][2]:
      player.SKILL_REFUND = 300
    else:
      player.SKILL_REFUND = 0

    # Update event
    event = 'game'

    # Start level timer
    player.level_start_time = time.time()
  elif (380 <= pos[0] <= 610) and (350 <= pos[1] <= 385):
    # Sets player sprite and stats based on character chosen
    player.character = 'r'
    player.image = 'rosmontis_sprite_1'
    player.MAX_HITPOINTS = 2000
    player.HITPOINTS = player.MAX_HITPOINTS
    if player.upgrades[player.character][0]:
      player.ATTACK = 300
    else:
      player.ATTACK = 50
    if player.upgrades[player.character][1]:
      player.MOVE_SPEED = 3
    else:
      player.MOVE_SPEED = 1
    if player.upgrades[player.character][2]:
      player.ATTACK_SPEED = 0.2
    else:
      player.ATTACK_SPEED = 2
    player.SKILL_POINTS = 0
    player.SKILL_BAR = 500
    player.SKILL_REFUND = 100

    # Update event
    event = 'game'

    # Start level timer
    player.level_start_time = time.time()
  elif (640 <= pos[0] <= 870) and (350 <= pos[1] <= 385):
    # Sets player sprite and stats based on character chosen
    player.character = 'j'
    player.image = 'julia_sprite_1'
    player.MAX_HITPOINTS = 1500
    player.HITPOINTS = player.MAX_HITPOINTS
    if player.upgrades[player.character][0]:
      player.ATTACK = 200
    else:
      player.ATTACK = 100
    if player.upgrades[player.character][1]:
      player.MOVE_SPEED = 4
    else:
      player.MOVE_SPEED = 1
    player.ATTACK_SPEED = 1.5
    player.SKILL_POINTS = 0
    player.SKILL_BAR = 1000
    if player.upgrades[player.character][2]:
      player.SKILL_REFUND = 200
    else:
      player.SKILL_REFUND = 0

    # Update event
    event = 'game'

    # Start level timer
    player.level_start_time = time.time()

# ---------- Go To Character Info Menu ---------- #
def cmd_goto_character_info_screen(pos):
  '''
  Goes to the info screen for the character user wishes to see

  Parameters:
    pos (tuple): position where user clicks
  Returns:
    None
  '''
  # current event
  global event

  # Goes to different character menu depending on character user wishes to view
  if (280 <= pos[0] <= 335) and (110 <= pos[1] <= 135):
    # Update event
    event = 'char_info_1'
  elif (545 <= pos[0] <= 600) and (110 <= pos[1] <= 135):
    # Update event
    event = 'char_info_2'
  elif (800 <= pos[0] <= 855) and (110 <= pos[1] <= 135):
    # Update event
    event = 'char_info_3'
    
# ---------- Draw Character Info Menu ---------- #
def display_character_info_screen():
  '''
  Displays a screen that shows the player character info and upgrades. Uses events to know which character info to display

  Parameters:
    character (int) : the player character
  Returns:
    None
  '''
  # Draws text that tells player upgrades are locked
  # Checks for different characters as some characters upgrades may be unlocked while others are not
  if event == 'char_info_1':
    screen.blit('character_info_screen_1', (0, 0))

    if player.upgrades['w'][0] == False:
      screen.blit('unlock_upgrade_1', (640, 180))
    if player.upgrades['w'][1] == False:
      screen.blit('unlock_upgrade_2', (640, 240))
    if player.upgrades['w'][2] == False:
      screen.blit('unlock_upgrade_3', (640, 300))
    
  elif event == 'char_info_2':
    screen.blit('character_info_screen_2', (0, 0))

    if player.upgrades['r'][0] == False:
      screen.blit('unlock_upgrade_1', (640, 180))
    if player.upgrades['r'][1] == False:
      screen.blit('unlock_upgrade_2', (640, 240))
    if player.upgrades['r'][2] == False:
      screen.blit('unlock_upgrade_3', (640, 300))
      
  elif event == 'char_info_3':
    screen.blit('character_info_screen_3', (0, 0))
    
    if player.upgrades['j'][0] == False:
      screen.blit('unlock_upgrade_1', (640, 180))
    if player.upgrades['j'][1] == False:
      screen.blit('unlock_upgrade_2', (640, 240))
    if player.upgrades['j'][2] == False:
      screen.blit('unlock_upgrade_3', (640, 300))

  # Indicators
  if indicators['back_button']:
    screen.blit('back_indicator', (880, 0))

# ---------- Exit Character Info Menu ---------- #
def cmd_exit_char_info(pos):
  '''
  Exits character info screen if user wishes

  Parameters:
    pos (tuple): place where player clicks
  Returns:
    None
  '''
  global event

  if (880 <= pos[0] <= 1000) and (0 <= pos[1] <= 50):
    # Update event
    event = 'character_selection'




# ---------------------------------------
# Levels
# Includes:
#   - Beating level
#   - Different spawn rates
#   - Boss levels
# ---------------------------------------

# ---------- Draw Level Menu ---------- #
def display_level():
  '''
  Displays a screen telling player that they are about to proceed to next level.

  Parameters:
    None
  Returns:
    None
  '''
  screen.blit('level_screen', (0, 0))
  # If player reaches stage 6, player has won
  # Changes level display to make it slightly more anticipating :D
  # Next level is 15, so we check 14
  # >= for safety
  if player.LEVEL >= 14:
    screen.draw.text(f"???", (810, 310), fontsize = 50, color = (0, 0, 0))
  else:
    # Player level has 1 added to it, as it is next level
    # Levels are displayed as [stage]-[level], where every 3 levels are a stage
    # Stage and levels start at 1, so that is why there is a +1
    screen.draw.text(f"{(player.LEVEL + 1) // 3 + 1}-{(player.LEVEL + 1) % 3 + 1}", (810, 310), fontsize = 50, color = (0, 0, 0))

  # Indicators
  if indicators['level_continue']:
    screen.blit('continue_indicator', (763, 370))

# ---------- Beating Levels ---------- #
def cmd_continue_next_level(pos):
  '''
  Continues player to next level upon clicking continue button. Resets projectiles fired, enemies, movement, and restores some HP.

  Parameters:
    pos (tuple): The location that player clicked
  Returns:
    None
  '''
  # The current event player is experiencing
  global event
  # Background location
  global background_pos

  # Reset position
  background_pos = 0
  player.pos = 0, HEIGHT // 2
    
  # Reset player movement
  player.move_right = False
  player.move_left = False
  player.move_up = False
  player.move_down = False

  # If player uses Crusader's skill and goes through portal before it expires, the stats will not be reset
  # Thus, to prevent this, I reset them here as well
  if player.character == 'j':
    if player.upgrades[player.character][0]:
      player.ATTACK = 200
    else:
      player.ATTACK = 100
    player.ATTACK_SPEED = 1.5
    if player.upgrades[player.character][1]:
      player.MOVE_SPEED = 4
    else:
      player.MOVE_SPEED = 1
  
  # Reset projectiles
  player.curr_bullets.clear()
  player.skill_projectile.clear()
  # Reset skill effects
  player.skill_effects.clear()
  
  # Restore some hitpoints and start of with half skill bar filled
  player.HITPOINTS += (player.MAX_HITPOINTS - player.HITPOINTS) // 2
  player.SKILL_POINTS = player.SKILL_BAR // 2

  # Reset times of shooting
  player.last_shot_time = -float('inf')
  player.curr_shot_time = 0

  # Reset enemies
  curr_enemies.clear()
  curr_enemy_bullets.clear()

  # Reset all destructions
  destruction_explosions.clear()
  bullet_explosions.clear()

  # Unschedules any events scheduled during the game
  clock.unschedule(remove_player_skill_effects)
  clock.unschedule(destruc_explosion_removal)
  clock.unschedule(bullet_explosion_removal)
  
  # If continue button is pressed, proceed to next level or end the game
  if (780 <= pos[0] <= 910) and (380 <= pos[1] <= 420):
    # This means the next level will be stage 6, so we check 14 instead of 15
    # >= just in case
    if player.LEVEL >= 14:
      event = 'end'
      # Incrementing level is necessary for the highscore
      player.LEVEL += 1
    else:
      event = 'game'
      # Next level
      player.LEVEL += 1
      player.level_start_time = time.time()

def beat_level():
  '''
  Player beats level by surviving on time and getting a certain number of kills. Once level is beat, portal spawns, allowing player to continue to next level.
  '''
  # Current event
  global event
  # Conditions to go to next level:
    # time which scales with levels and kills which also scale with levels
  if time.time() - player.level_start_time >= 10.0 + (player.LEVEL - 1) and player.KILLS >= 2 + player.LEVEL * 2:
    # Draws exit portal
    portal = Actor('portal', center = (600, 250))
    portal.draw()

    # Player proceeds if player enters. Player can also continue farming the level for whatever reason
    if portal.colliderect(player):
      event = 'level'














      
# ---------------------------------------
# End Game
# 
# For when game is beaten
# ---------------------------------------
def display_end_game_screen():
  '''
  Displays the end game screen.

  Parameters:
    None.
  Returns:
    None.
  '''
  screen.blit('end_screen', (0,0))
  clock.schedule(cmd_end_game, 5.0)
      




  






# ---------------------------------------
# Eye candy
# 
# Indicators for buttons
# ---------------------------------------
def menu_begin_indicator(pos):
  '''
  Indicates that player can press the begin button on menu

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (460 <= pos[0] <= 570) and (420 <= pos[1] <= 470):
    return True
  else:
    return False

def menu_instruct_indicator(pos):
  '''
  Indicates that player can press the instructions button on menu

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (920 <= pos[0] <= 970) and (430 <= pos[1] <= 470):
    return True
  else:
    return False

def back_button_indicator(pos):
  '''
  Indicates that player can press the back button

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (880 <= pos[0] <= 1000) and (0 <= pos[1] <= 50):
    return True
  else:
    return False

def level_continue_indicator(pos):
  '''
  Indicates that player can press the continue button on the continue level screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (780 <= pos[0] <= 910) and (380 <= pos[1] <= 420):
    return True
  else:
    return False

def char_info_1_indicator(pos):
  '''
  Indicates that player can press the info button for Weedy on the character selection screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (280 <= pos[0] <= 335) and (110 <= pos[1] <= 135):
    return True
  else:
    return False

def char_info_2_indicator(pos):
  '''
  Indicates that player can press the info button for Rosmontis on the character selection screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (545 <= pos[0] <= 600) and (110 <= pos[1] <= 135):
    return True
  else:
    return False

def char_info_3_indicator(pos):
  '''
  Indicates that player can press the info button for Crusader on the character selection screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (800 <= pos[0] <= 855) and (110 <= pos[1] <= 135):
    return True
  else:
    return False

def char_commence_1_indicator(pos):
  '''
  Indicates that player can press the commence button for Weedy on the character selection screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (120 <= pos[0] <= 350) and (350 <= pos[1] <= 385):
    return True
  else:
    return False

def char_commence_2_indicator(pos):
  '''
  Indicates that player can press the commence button for Rosmontis on the character selection screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (380 <= pos[0] <= 610) and (350 <= pos[1] <= 385):
    return True
  else:
    return False

def char_commence_3_indicator(pos):
  '''
  Indicates that player can press the commence button for Crusader on the character selection screen

  Parameters:
    pos (tuple): location of player mouse
  Returns:
    bool: if player mouse is in required position or not
  '''
  if (640 <= pos[0] <= 870) and (350 <= pos[1] <= 385):
    return True
  else:
    return False
    





  
    

# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# -------------------------- RUNNING THE GAME ----------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
# ------------------------------------------------------------------------- #
      
def draw():
  '''
  Draws everything needed, Pygame Zero function
  '''

  # Checks events
  # I could have implemented event checking in the functions themselves, but I believe that it is better to do one event check rather than one for each function.
  # Note that event uses elif checking instead of if because it is safer
  # For example, if I am adding events, then there could be a bug of both events triggering the same thing due to else statements
  # Clear screen
  screen.clear()
  
  # ----------------- Main Menu ----------------- #
  if event == 'menu':
    display_menu()

  # ----------------- Character Selection ----------------- #
  elif event == 'character_selection':
    display_character_selection_screen()

   # ----------------- Character Info ----------------- #
  elif event == 'char_info_1' or event == 'char_info_2' or event == 'char_info_3':
    display_character_info_screen()

  # ----------------- Game ----------------- #
  elif event == 'game':
    background_animation()
    if player.ALIVE:
      beat_level()
      draw_player_assets()
      draw_enemy_assets()
      draw_explosions()
    display_player_hp_bar()
    display_player_skill_bar()
    display_level_and_kills()

  # ----------------- Game End ----------------- #
  elif event == 'end':
    display_end_game_screen()
    
  # ----------------- Continue Level ----------------- #
  elif event == 'level':
    display_level()

  # ----------------- Instructions ----------------- #
  elif event == 'instructions':
    display_instructions()
    
def update():
  '''
  Updates movement, Pygame Zero function
  '''
  
  # ----------------- Game ----------------- #
  if event == 'game':
    if player.ALIVE:
      player_movement()
      character_animation()
      player_bullet_movement()
      player_skill_movement()
      spawn_enemies(player.LEVEL + 2)
      enemy_movement()
      enemy_bullet_movement()

def on_key_down(key):
  '''
  Handles button presses, Pygame Zero function
  '''

  # ----------------- Game ----------------- #
  if event == 'game':
    if player.ALIVE:
      cmd_player_move(key)
      cmd_player_shoot(key)
      cmd_activate_player_skill(key)

def on_key_up(key):
  '''
  Handles button releases, Pygame Zero function
  '''

  # ----------------- Game ----------------- #
  if event == 'game':
    if player.ALIVE:
      cmd_player_stop(key)

def on_mouse_down(pos):
  '''
  Handles mouse clicks, Pygame Zero function
  '''

  # ----------------- Menu ----------------- #
  if event == 'menu':
    cmd_goto_character_selection_screen(pos)
    cmd_goto_instructions(pos)

  # ----------------- Character Selection  ----------------- #
  elif event == 'character_selection':
    cmd_start_game(pos)
    cmd_goto_character_info_screen(pos)
    cmd_exit_char_select(pos)

  # ----------------- Character Info ----------------- #
  elif event == 'char_info_1' or event == 'char_info_2' or event == 'char_info_3':
    cmd_exit_char_info(pos)
  # ----------------- Level ----------------- #
  elif event == 'level':
    cmd_continue_next_level(pos)

  # ----------------- Instructions ----------------- #
  elif event == 'instructions':
    cmd_go_back_menu(pos)

def on_mouse_move(pos):
  '''
  Handles when indicators should be shown and where mouse is hovering, Pygame Zero function
  '''
  # The indicator values being changed is not locked behind different events
  # This is because the mouse position can change during the game, causing the indicator to be stuck on True or False even if the mouse is not in the correct position
  # A fix to this would either to have a function that gets mouse position
  # Which unfortunately pgzero lacks for some reason
  # Or, as done here, the values are always updated
  indicators['menu_begin'] = menu_begin_indicator(pos)
  indicators['menu_instructions'] = menu_instruct_indicator(pos)
  indicators['back_button'] = back_button_indicator(pos)
  indicators['level_continue'] = level_continue_indicator(pos)
  indicators['char_info_1'] = char_info_1_indicator(pos)
  indicators['char_info_2'] = char_info_2_indicator(pos)
  indicators['char_info_3'] = char_info_3_indicator(pos)
  indicators['char_commence_1'] = char_commence_1_indicator(pos)
  indicators['char_commence_2'] = char_commence_2_indicator(pos)
  indicators['char_commence_3'] = char_commence_3_indicator(pos)


pgzrun.go()
