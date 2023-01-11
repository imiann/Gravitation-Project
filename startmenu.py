import pygame
import main

pygame.init()

WIDTH = 960
HEIGHT = 540
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
FPS = 30

title_height = 100
title_width = 100
rect_height = 100
rect_width = 400
small_rect_height = 50
small_rect_width = 115
medium_rect_width = 175
BG = pygame.image.load("assets/BG.png")
BGF = pygame.transform.scale(BG, (WIDTH, HEIGHT))
WHITE = (255,255,255)
PURPLE = (127,0,238)
LIGHT = (177,156,217)
BLACK = (27,30,35)
BLUE = (106, 90, 205)
smallfont = pygame.font.SysFont('Roboto',75)
smallfont1 = pygame.font.SysFont('Times New Roman',50)
smallfont2 = pygame.font.SysFont('Roboto', 32)

text = smallfont.render('PLAY' , True , BLACK) 
instruction = smallfont1.render('Use Space to change the gravity' , True , WHITE) 
niv1 = smallfont2.render('Level 1' , True , BLACK)
niv2 = smallfont2.render('Level 2', True, BLACK)
niv3 = smallfont2.render('Level 3', True, BLACK)
normal = smallfont2.render('Normal Mode', True, BLACK)
hard = smallfont2.render('Hard Mode', True, BLACK)

TITLE = pygame.image.load("assets/title.png")
TITLE_T = pygame.transform.scale(TITLE,(800,800))

clock = pygame.time.Clock()

def start():
  clock.tick(FPS)
  run = True
  selected_level = 1
  mode = 0
  while run:
    MOUSE = pygame.mouse.get_pos()
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
          run = False
          pygame.quit()  
    
      if event.type == pygame.MOUSEBUTTONDOWN:
        
        # Checking if mouse within any buttons
        if WIDTH / 3 - small_rect_width / 3 <= MOUSE[0] <= WIDTH / 3 + 2* small_rect_width / 3 and 2 * HEIGHT / 3 - small_rect_height / 3 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3:
            selected_level = 1
            
        if WIDTH / 2 - small_rect_width / 2 <= MOUSE[0] <= WIDTH / 2 + small_rect_width / 2 and 2 * HEIGHT / 3 - small_rect_height / 3 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3:
            selected_level = 2
            
        if 2* WIDTH / 3 - 2* small_rect_width / 3 <= MOUSE[0] <= 2* WIDTH / 3 + 2 * small_rect_width / 3 and 2 * HEIGHT / 3 - small_rect_height / 3 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3:
            selected_level = 3
            
        if WIDTH / 2 - medium_rect_width - 25 <= MOUSE[0] <= WIDTH / 2 - 25 and 2 * HEIGHT / 3 - small_rect_height / 3 + 67 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3 + 67:
            mode = 0
            
        if WIDTH / 2 + 25 <= MOUSE[0] <= WIDTH / 2 + small_rect_width + 25 and 2 * HEIGHT / 3 - small_rect_height / 3 + 67 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3 + 67:
            mode = 1
            
        if WIDTH/2 - rect_width/2 <= MOUSE[0] <= WIDTH/2 + rect_width/2 and HEIGHT/2  - rect_height/2 <= MOUSE[1] <= HEIGHT/2 + rect_height/2:
            main.main(selected_level, mode)
          

        
    WIN.blit(BGF, (0,0))
        
    # Play button
    if WIDTH/2 - rect_width/2 <= MOUSE[0] <= WIDTH/2 + rect_width/2 and HEIGHT/2  - rect_height/2 <= MOUSE[1] <= HEIGHT/2 + rect_height/2:       
      pygame.draw.rect(WIN,PURPLE, pygame.Rect(WIDTH/2 - rect_width/2, HEIGHT/2 - rect_height/2, rect_width, rect_height))
    else:    
      pygame.draw.rect(WIN, LIGHT, pygame.Rect(WIDTH/2 - rect_width/2, HEIGHT/2 - rect_height/2, rect_width, rect_height))
      
    # Level 1 button 
    if WIDTH / 3 - small_rect_width / 3 <= MOUSE[0] <= WIDTH / 3 + 2* small_rect_width / 3 and 2 * HEIGHT / 3 - small_rect_height / 3 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3:
        pygame.draw.rect(WIN, PURPLE, pygame.Rect(WIDTH/3 - small_rect_width/3, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))  
    else:
        pygame.draw.rect(WIN, LIGHT, pygame.Rect(WIDTH/3 - small_rect_width/3, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))
     
    # Level 2 button
    if WIDTH / 2 - small_rect_width / 2 <= MOUSE[0] <= WIDTH / 2 + small_rect_width / 2 and 2 * HEIGHT / 3 - small_rect_height / 3 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3:
         pygame.draw.rect(WIN, PURPLE, pygame.Rect(WIDTH/2 - small_rect_width/2, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))  
    else:
         pygame.draw.rect(WIN, LIGHT, pygame.Rect(WIDTH/2 - small_rect_width/2, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))
        
    # Level 3 button    
    if 2* WIDTH / 3 - 2* small_rect_width / 3 <= MOUSE[0] <= 2* WIDTH / 3 + 2 * small_rect_width / 3 and 2 * HEIGHT / 3 - small_rect_height / 3 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3:
        pygame.draw.rect(WIN, PURPLE, pygame.Rect(2 * WIDTH/3 - 2* small_rect_width/3, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))  
    else:
        pygame.draw.rect(WIN, LIGHT, pygame.Rect(2 * WIDTH/3 - 2* small_rect_width/3, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))
    
    # Normal mode button
    if WIDTH / 2 - medium_rect_width - 25 <= MOUSE[0] <= WIDTH / 2 - 25 and 2 * HEIGHT / 3 - small_rect_height / 3 + 67 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3 + 67:
        pygame.draw.rect(WIN, PURPLE, pygame.Rect(WIDTH/2 - medium_rect_width - 25, 2 * HEIGHT / 3 - small_rect_height / 3 + 67, medium_rect_width, small_rect_height))  
    else:
        pygame.draw.rect(WIN, LIGHT, pygame.Rect(WIDTH/2 - medium_rect_width - 25, 2 * HEIGHT / 3 - small_rect_height / 3 + 67, medium_rect_width, small_rect_height))
        
    # Hard mode button
    if WIDTH / 2 + 25 <= MOUSE[0] <= WIDTH / 2 + small_rect_width + 25 and 2 * HEIGHT / 3 - small_rect_height / 3 + 67 <= MOUSE[1] <= 2 * HEIGHT / 3 + 2* small_rect_height / 3 + 67:
        pygame.draw.rect(WIN, PURPLE, pygame.Rect(WIDTH/2 + 25, 2 * HEIGHT / 3 - small_rect_height / 3 + 67, medium_rect_width, small_rect_height))  
    else:
        pygame.draw.rect(WIN, LIGHT, pygame.Rect(WIDTH/2 + 25, 2 * HEIGHT / 3 - small_rect_height / 3 + 67, medium_rect_width, small_rect_height))
        
    if selected_level == 1:
        pygame.draw.rect(WIN, BLUE, pygame.Rect(WIDTH/3 - small_rect_width/3, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))
    elif selected_level == 2:
        pygame.draw.rect(WIN, BLUE, pygame.Rect(WIDTH/2 - small_rect_width/2, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))
    elif selected_level == 3:
        pygame.draw.rect(WIN, BLUE, pygame.Rect(2 * WIDTH/3 - 2* small_rect_width/3, 2 * HEIGHT / 3 - small_rect_height / 3, small_rect_width, small_rect_height))
        
    if mode == 0:
        pygame.draw.rect(WIN, BLUE, pygame.Rect(WIDTH/2 - medium_rect_width - 25, 2 * HEIGHT / 3 - small_rect_height / 3 + 67, medium_rect_width, small_rect_height))
    elif mode == 1:
        pygame.draw.rect(WIN, BLUE, pygame.Rect(WIDTH/2 + 25, 2 * HEIGHT / 3 - small_rect_height / 3 + 67, medium_rect_width, small_rect_height))
    
    
    WIN.blit(text , (WIDTH / 2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    WIN.blit(niv1, (WIDTH / 3 - small_rect_width / 3 + small_rect_width /2 - niv1.get_width()/2, 2 * HEIGHT / 3 - small_rect_height / 3 + small_rect_height / 2 - niv1.get_height() / 2))
    WIN.blit(niv2, (WIDTH / 2 - niv2.get_width()/2, 2 * HEIGHT / 3 - small_rect_height / 3 + small_rect_height / 2 - niv2.get_height() / 2))
    WIN.blit(niv3, (2* WIDTH / 3 - 2*  small_rect_width / 3 + small_rect_width /2 - niv1.get_width()/2, 2 * HEIGHT / 3 - small_rect_height / 3 + small_rect_height / 2 - niv1.get_height() / 2))
    WIN.blit(normal, (WIDTH / 2 - 25 - medium_rect_width / 2 - normal.get_width() / 2, 2 * HEIGHT / 3 - small_rect_height / 3 + 67 + small_rect_height / 2 - normal.get_height() / 2))
    WIN.blit(hard, (WIDTH / 2 + 25 + medium_rect_width / 2 - hard.get_width() / 2, 2 * HEIGHT / 3 - small_rect_height / 3 + 67 + small_rect_height / 2 - hard.get_height() / 2))
    WIN.blit(TITLE_T,(WIDTH/2 - 400, -200))
    WIN.blit(instruction,(WIDTH / 2 - instruction.get_width() / 2,HEIGHT/2+200))
   
   
    pygame.display.update()

if __name__ == "__main__":
  start()
