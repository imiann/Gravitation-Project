import pygame, sys
import main, startmenu

def endScreen(state, color):
  '''
  Function that pauses game and shows score after loss
  Click after losing to return to the main menu  
  '''
  score = main.score
  run = True
  while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        run = False
        pygame.quit()
        sys.quit()
        
      if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.K_SPACE:
        run = False
        startmenu.start()
       


    main.WIN.blit(main.BGF, (0,0))
    
    # Font Variables
    font = pygame.font.SysFont('Roboto', 80) # Font
    font2 = pygame.font.SysFont('Roboto', 40)
    endText = font.render(str(state), 1, color) # Rendering text
    lastScore = font2.render("Best Score: " + str(main.updateFile()), 1, (255,255,255))
    currentScore = font2.render("Score: " + str(score), 1, (255, 255, 255))
    restart = font.render("Click to restart", 1, (255,255,255))
    
    # Blitting onto screen
    main.WIN.blit(endText, (main.WIDTH / 2 - endText.get_width()/2, 80))
    main.WIN.blit(lastScore, (main.WIDTH / 2 - lastScore.get_width()/2, 200))
    main.WIN.blit(currentScore, (main.WIDTH / 2 - currentScore.get_width() / 2, 240))
    main.WIN.blit(restart, (main.WIDTH / 2 - restart.get_width() / 2, 330))
    
    pygame.display.update()
    
  score = 0