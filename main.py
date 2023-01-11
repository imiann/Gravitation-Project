import pygame, sys
import random
import startmenu, niveau, endScreen

pygame.init()

# Load music
pygame.mixer.init()
pygame.mixer.music.load("assets/music.mp3")

# Global Variables

# Window
WIDTH = 960
HEIGHT = 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitation - Projet Final NSI")

# Character dimensions
CHARACTER_WIDTH = 40
CHARACTER_HEIGHT = 65

# Platform dimensions
PLATFORM_WIDTH = 168
PLATFORM_HEIGHT = 32

# Background and entity images
BACKGROUND_IMAGE = pygame.image.load("assets/BG.png")
BGF = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))
CHARACTER_IMAGE = pygame.image.load("assets/CHARACTER.png")
CHARACTER = pygame.transform.scale(CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
ROCKET_IMAGE = pygame.image.load("assets/rocket.png")
ROCKET = pygame.transform.scale(ROCKET_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
TILE_IMAGE = pygame.transform.scale(pygame.image.load("assets/tile.png"), (PLATFORM_WIDTH , PLATFORM_HEIGHT))
END_FLAG_IMAGE = pygame.image.load("assets/banner-big/banner-big-1.png")
END_FLAG = pygame.transform.scale(END_FLAG_IMAGE, (70, 184))
SHIELD = pygame.image.load("assets/armor_combo.png")

# FPS Variables
SPEED_INCREASE = pygame.USEREVENT+2
PAUSE = 0

BF_x = 0
BF_x2 = BGF.get_width()

# Speed values (also used as tolerance values for collisions)
GRAVITY_FORCE = 7
WALL_RECOIL = 7

# Inherited rectangle class for platforms 
class Platform(pygame.Rect):

  def __init__(self, x, y, width, height):
    self.x = x
    self.y = y
    self.width = width
    self.height = height
    self.rotateCount = 0
    self.vel = 1.4
    self.img = TILE_IMAGE
  
  def draw(self, WIN):
    pygame.draw.rect(WIN, (150, 111, 214), (self.x + 10, self.y + 5, self.width - 20, self.height - 5), 2)

    WIN.blit(pygame.transform.scale(self.img, (self.width, self.height)), (self.x,self.y))

def main(selected_level, mode):
  '''
  This is the main gameplay loop, which handles the core game features, such as collision, keyboard interpretation, background scrolling, and entity movement
  '''
  global platforms, score, grav_inv, slices, shield
  
  CHARACTER = pygame.transform.scale(CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT))
  character = pygame.Rect(WIDTH / 2, HEIGHT-CHARACTER_HEIGHT - 37, CHARACTER_WIDTH, CHARACTER_HEIGHT)
  
  # Main variables
  clock = pygame.time.Clock()
  run = True
  FPS = 30
  BF_x = 0
  BF_x2 = BGF.get_width() 
  grav_inv = False
  shield = True
  platforms = []
  collide = False
  winplatformx = None
  endflag = False
  rocket = pygame.Rect(900, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)
  
  if mode == 1:
    rockety = 500
  pygame.time.set_timer(SPEED_INCREASE, 500)
  pygame.mixer.music.play(-1) #starts and loops the music

  if selected_level == 1:
      slices = loadSlice(niveau.niveau1)
  if selected_level == 2:
      slices = loadSlice(niveau.niveau2)
  if selected_level == 3:
      slices = loadSlice(niveau.niveau3)
  
  for x in range(16):
    if slices[0][x][0] == 1:
      platforms.append(Platform(420, x*(HEIGHT / 16), PLATFORM_WIDTH, PLATFORM_HEIGHT))
  for i in range(7):
      loadLevel(slices[0])
  
  while run:
     
    BF_x = BF_x - 2
    BF_x2 -= 2
      
    if BF_x < BGF.get_width() * -1:  
      BF_x = BGF.get_width()

    if BF_x2 < BGF.get_width() * -1:
      BF_x2 = BGF.get_width()

    for platform in platforms: # Move platforms
      platform.x -= 3

      if winplatformx is not None: # Store the X value of the end of the level (the winning platform)
          winplatformx = platforms[-1].centerx

      if platform.right + 20 < 0: # If any given platform is off screen
        platforms.pop(platforms.index(platform))
        if len(slices) != 0:
            loadLevel(slices[0])
        if len(slices) == 1:
            winplatformx = platforms[-1].centerx
            endflag = True
        
    if character.x + 60 < 0: # Defeat condition 1: Character off screen
        endScreen.endScreen("Where did you go!?", (150, 0, 24))
        
    if character.x == winplatformx: # Win condition: Reach last platform
        endScreen.endScreen("Beep Boop You Win!", (80, 200, 120))
    
    # Collide, Wall and Rocket collision
    collide = checkGroundCollision(character, platforms)
    hitwall = checkWallCollision(character,platforms)
    if mode == 1:
      teamRocketBOOM(character, rocket)
      
    # If character hitting wall, moves back    
    if hitwall:
        character.x -= WALL_RECOIL
    
    # Manages gravity and collision with platforms
    if grav_inv:
      if collide: # If were on top or under a platform, stop moving 
          character.y -= 0
      elif character.y > 0:
          character.y -= GRAVITY_FORCE
      else: # Defeat condition 2: touching the floor 
          endScreen.endScreen("Up up and away!", (0, 191, 254))
          
    if not grav_inv:
      if collide:
          character.y -= 0
      elif character.y < HEIGHT - CHARACTER_HEIGHT:
        character.y += GRAVITY_FORCE
      else:
          endScreen.endScreen("Splat! You hit the ground...", (150, 0, 24))
          
    # Moves rocket
    if mode == 1:
      rocket.x -= 10      
    
      # When rocket is offscreen, give a new random height not within characters height range and re-fire it
      if rocket.x + 60 < 0:
        rocket.x = WIDTH
        rockety = random.randint(100, HEIGHT - 100)
        while rockety > character.y - 50 and rockety < character.bottom + 50:
            rockety = random.randint(100, HEIGHT - 100)
        rocket.y = rockety
        
    # Manages events
    
    for event in pygame.event.get():
        
      if event.type == pygame.QUIT:
          run = False
          pygame.quit()
          sys.quit()

      # Manages keyboard input
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
            
            if collide: # If the character is touching the ground, switching gravity is allowed
                # Changes gravity, and flips the character
                if grav_inv:
                    grav_inv = False
                    CHARACTER = pygame.transform.flip(CHARACTER, False, True) 
                    character.y += 17
                    
                else:
                    grav_inv=True
                    CHARACTER= pygame.transform.flip(CHARACTER, False, True)
                    character.y -= 17
        
      # Increases speed as game goes on
      if event.type == SPEED_INCREASE:
        FPS += 1.5
        
    # Scoring
    score = FPS // 5 - 6
    clock.tick(FPS)
    
    # Drawing function
    draw_window(CHARACTER, character, BF_x, BF_x2, endflag, rocket, mode)

def checkGroundCollision(character, platforms):
    '''
    Function that checks characters collision with top or bottom of platforms
    Returns boolean
    '''
    collide = False
    if len(platforms) != 0:
        for platform in platforms:
          if character.left >= platform.left - 40 and character.right <= platform.right + 40 :

            if abs(character.bottom - platform.top) < GRAVITY_FORCE and not grav_inv:
              collide = True

            if abs(character.top - platform.bottom) < GRAVITY_FORCE and grav_inv:
              collide = True

        return collide

def checkWallCollision(character, platforms):
  '''
  Function that checks character collision with wall
  Returns boolean
  '''
  hitwall = False
  if len(platforms) != 0:
    for platform in platforms:
      
      if character.right > platform.x - WALL_RECOIL and character.right < platform.x + WALL_RECOIL:  # Check if touching left of platform
      
          if character.bottom >= platform.bottom - GRAVITY_FORCE - 3 and character.top <= platform.top + GRAVITY_FORCE + 3 : # Check if character top and bottom in platform hitbox
              if character.right >= platform.left and character.left <= platform.left:
                  
                  hitwall = True
                  return hitwall
          
          if character.bottom >= platform.top + GRAVITY_FORCE + 3 and character.bottom <= platform.bottom - GRAVITY_FORCE - 3: # Check if only character bottom in platform hitbox
              if character.right >= platform.left and character.left <= platform.left:
                  
                  hitwall = True
                  return hitwall
              
          if character.top >= platform.top + GRAVITY_FORCE + 3 and character.top <= platform.bottom - GRAVITY_FORCE - 3: # Check if only character top in platform hitbox
              if character.right >= platform.left and character.left <= platform.left:
                  
                  hitwall = True
                  return hitwall
         
    return hitwall

def teamRocketBOOM(character, rocket):
  ''' 
    Function that checks "character"'s collision with the rocket.
    
    Defeat condition 3: Character touches rocket
  '''
  global shield

  if character.right > rocket.left - WALL_RECOIL and character.right < rocket.left + WALL_RECOIL:  # Check if touching left of rocket
    if character.right >= rocket.left and character.left <= rocket.left: #Check if character's bounds is within the rocket's bounds along the X axis
  
      if character.bottom >= rocket.bottom - GRAVITY_FORCE and character.top <= rocket.top + GRAVITY_FORCE : # Check if platform top and bottom in character
          if not shield:
              return endScreen.endScreen("Boom Boom!", (150, 0, 24))
          shield = False
      
      if character.bottom >= rocket.top and character.bottom <= rocket.bottom - GRAVITY_FORCE: # Check if only character bottom in platform hitbox
          if not shield:
              return endScreen.endScreen("Boom Boom!", (150, 0, 24))
          shield = False
          
      if character.top >= rocket.top and character.top <= rocket.bottom - GRAVITY_FORCE: # Check if only character top in platform hitbox
          if not shield:
              return endScreen.endScreen("Boom Boom!", (150, 0, 24))
          shield = False

def loadSlice(level):
    slices = []
    current_slice = 0
    inverse = niveau.transpose(level)
    
    while len(slices) < len(inverse):
        if current_slice+1 < len(inverse):   
            slices.append(niveau.transpose(inverse[current_slice:current_slice+1]))
        else:
            slices.append(niveau.transpose(inverse[current_slice:]))
            
        current_slice += 1
    
    return slices

def loadLevel(level):
  '''
  Function that loads the level by slice
  '''
  global platforms, slices
  platx = platforms[-1].x + 168
  ind=0
  while ind < 1:
    for x in range(16):
      if level[x][ind] == 1:
        platforms.append(Platform(platx, x*(HEIGHT / 16), PLATFORM_WIDTH, PLATFORM_HEIGHT))
    ind+=1
  if len(level) > 0:
      slices.pop(0)

def updateFile():
    ''' 
    Function that stores top score
    Return score, and integer
    '''
    f = open("score.txt", "r")
    file = f.readlines()
    last = float(file[0])
    
    if last < int(score):
        f.close()
        file = open("score.txt", "w")
        file.write(str(score))
        file.close()
        
        return score
    
    return last

def draw_window(CHARACTER, character, BF_x, BF_x2, endflag, rocket, mode):
  '''
  Draws all entities to pygame window
  '''
  global platforms, score, shield

  font = pygame.font.Font("assets/font.ttf", 30)

  # Background and Character
  WIN.blit(BGF, (BF_x, 0))
  WIN.blit(BGF, (BF_x2, 0))
  WIN.blit(CHARACTER, (character.x, character.y))

  # Platforms
  for platform in platforms:
    if platform.x < WIDTH:
      platform.draw(WIN)

  # Score
  text = font.render("SCORE: " + str(score), 1, (255, 255, 255))
  twidth = text.get_width()
  WIN.blit(text, (WIDTH - twidth - 20 , 10))
  
  if mode == 1:
    # Rocket
    WIN.blit(ROCKET, (rocket.x, rocket.y))
    
    # Shield
    if shield:
      WIN.blit(SHIELD, ((SHIELD.get_width()/2) - 10, 10))
  
  # Endflag
  if endflag:
    WIN.blit(END_FLAG, (platforms[-1].centerx, platforms[-1].y -170))
      

  pygame.display.update()
  

if __name__ == "__main__":
    startmenu.start()