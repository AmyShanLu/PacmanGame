import pygame
import GameStart
import os
from os.path import dirname

# Load all required images for the game
MenuBacImg = pygame.image.load(os.path.join(dirname("images"), "images", 'pacman_menu_background.png'))
UnselStartBuImg = pygame.image.load(os.path.join(dirname("images"), "images", 'UnselectedStartButton.png'))
SelStartBuImg = pygame.image.load(os.path.join(dirname("images"), "images", 'SelectedStartButton.png'))
UnselExitBuImg = pygame.image.load(os.path.join(dirname("images"), "images", 'UnselectedExitButton.png'))
SelExitBuImg = pygame.image.load(os.path.join(dirname("images"), "images", 'SelectedExitButton.png'))
dotImg = pygame.image.load(os.path.join(dirname("images"), "images", 'dot.png'))
energizerImg = pygame.image.load(os.path.join(dirname("images"), "images", 'energizer.png'))
horLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'horL.png'))
verLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'verL.png'))
BoRiCImg = pygame.image.load(os.path.join(dirname("images"), "images", 'BoRiC.png'))
BoLeCImg = pygame.image.load(os.path.join(dirname("images"), "images", 'BoLeC.png'))
ToRiCImg = pygame.image.load(os.path.join(dirname("images"), "images", 'ToRiC.png'))
ToLeCImg = pygame.image.load(os.path.join(dirname("images"), "images", 'ToLeC.png'))
PinkLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'PinkL.png'))
PacManImg = pygame.image.load(os.path.join(dirname("images"), "images", 'PacMan.png'))
RedGLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'RedGhostLeft.png'))
BlueGLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'BlueGhostLeft.png'))
PinkGLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'PinkGhostLeft.png'))
OrangeGLImg = pygame.image.load(os.path.join(dirname("images"), "images", 'OrangeGhostLeft.png'))
RedGRImg = pygame.image.load(os.path.join(dirname("images"), "images", 'RedGhostRight.png'))
BlueGRImg = pygame.image.load(os.path.join(dirname("images"), "images", 'BlueGhostRight.png'))
PinkGRImg = pygame.image.load(os.path.join(dirname("images"), "images", 'PinkGhostRight.png'))
OrangeGRImg = pygame.image.load(os.path.join(dirname("images"), "images", 'OrangeGhostRight.png'))
RedGUImg = pygame.image.load(os.path.join(dirname("images"), "images", 'RedGhostUp.png'))
BlueGUImg = pygame.image.load(os.path.join(dirname("images"), "images", 'BlueGhostUp.png'))
PinkGUImg = pygame.image.load(os.path.join(dirname("images"), "images", 'PinkGhostUp.png'))
OrangeGUImg = pygame.image.load(os.path.join(dirname("images"), "images", 'OrangeGhostUp.png'))
RedGDImg = pygame.image.load(os.path.join(dirname("images"), "images", 'RedGhostDown.png'))
BlueGDImg = pygame.image.load(os.path.join(dirname("images"), "images", 'BlueGhostDown.png'))
PinkGDImg = pygame.image.load(os.path.join(dirname("images"), "images", 'PinkGhostDown.png'))
OrangeGDImg = pygame.image.load(os.path.join(dirname("images"), "images", 'OrangeGhostDown.png'))
FrightenedGImg = pygame.image.load(os.path.join(dirname("images"), "images", 'FrightenedGhost.png'))

# The length of one tile
TileLen = 16

black = (0,0,0)

class GameMenu:
    '''
    Display the game menu.
    '''

    def __init__(self):
        pygame.init()
        self.clock0 = pygame.time.Clock()
        screen_width = 800
        screen_height = 640

        Exit = False

        while not Exit:
            # Check if mouse is clicked
            click = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Hits 'x'
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    click = True

            self.gameScreen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption('Pac-Man Game')

            # Display the menu background image, and button images
            self.gameScreen.blit(MenuBacImg, (0,0))

            self.button(self.gameScreen, click)

            # Update the whole window
            pygame.display.update()
            # Frame per second
            self.clock0.tick(15)

    def button(self, gameScreen, click):
        '''
        Display buttons on the game screen.
        Call gameloop() when user clicks the start button.
        '''

        # Button width and height
        button_width = 80
        button_height = 64

        # Drawing locations for start or try again button
        StartorTryAg_Xloc = 200
        StartorTryAg_Yloc = 450
        # Drawing locations for exit button
        Exit_Xloc = 520
        Exit_Yloc = 450

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        if mouse_pos[0] > StartorTryAg_Xloc and mouse_pos[0] < StartorTryAg_Xloc+button_width \
                and mouse_pos[1] > StartorTryAg_Yloc and mouse_pos[1] < StartorTryAg_Yloc + button_height:
            # The mouse in the start button area
            # Display the selected start button
            gameScreen.blit(SelStartBuImg, (StartorTryAg_Xloc,StartorTryAg_Yloc))

            # Display the unselected exit button
            gameScreen.blit(UnselExitBuImg, (Exit_Xloc,Exit_Yloc))

            # When user clicks the start button button
            if click:
                # Game Starts
                game = GameStart.GameStart(gameScreen)
                game.gameloop()

        elif mouse_pos[0] > Exit_Xloc and mouse_pos[0] < Exit_Xloc+button_width \
                and mouse_pos[1] > Exit_Yloc and mouse_pos[1] < Exit_Yloc + button_height:
            # The mouse in the exit button area, display the selected exit button
            gameScreen.blit(SelExitBuImg, (Exit_Xloc,Exit_Yloc))

            # Display the unselected start button
            gameScreen.blit(UnselStartBuImg, (StartorTryAg_Xloc,StartorTryAg_Yloc))

            # When user clicks the exit button
            if click:
                # Game Ends
                pygame.quit()
                quit()
        else:
            # Display the unselected start button
            gameScreen.blit(UnselStartBuImg, (StartorTryAg_Xloc,StartorTryAg_Yloc))

            gameScreen.blit(UnselExitBuImg, (Exit_Xloc,Exit_Yloc))
