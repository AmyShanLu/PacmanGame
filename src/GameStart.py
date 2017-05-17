import pygame
import TileMap
import pacman
import ghosts
import events
from GameMenu import *

class GameStart:
    '''
    Game starts. Initialize the game map, ghosts, and pacman.

    Input Argument: gameScreen: the game screen object.
    '''

    def __init__(self, gameScreen):

        self.gameScreen = gameScreen
        # background color
        self.gameScreen.fill(black)

        self.clock = pygame.time.Clock()

        # Build the tile map, pass the game screen to the map
        self.gamemap = TileMap.Tilemap(self.gameScreen)

        # The dictionary containing the ghosts in the map, key: ghost's color, value: ghost object
        self.ghostdict = dict()
        # Red, Blue, Pink and Orange ghosts
        self.ghostdict['R'] = ghosts.Ghost('R', self.gameScreen, self.gamemap)
        self.ghostdict['B'] = ghosts.Ghost('B', self.gameScreen, self.gamemap)
        self.ghostdict['P'] = ghosts.Ghost('P', self.gameScreen, self.gamemap)
        self.ghostdict['O'] = ghosts.Ghost('O', self.gameScreen, self.gamemap)

        self.PacMan = pacman.PacMan(PacManImg, gameScreen)

        self.events = events.events()
        self.fruits = events.fruits()
        self.frightenedtime = None

        # Game start time
        self.game_start_time = pygame.time.get_ticks()

    def gameloop(self):
        '''
        Game loop.

        Return: Boolean: - True: when pacman is eaten by the ghost, game ends.
        '''

        Exit = False
        self.events.PacManLives(self.PacMan,self.gameScreen,self.gamemap,self.ghostdict,self.fruits,self.game_start_time)
        while not Exit:
            # Every event that happens
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Hits 'x'
                    pygame.quit()
                    quit()

            # Assign and Check ghosts' mode
            for ghostC in self.ghostdict.keys():
                self.GhostModeAssign(self.ghostdict[ghostC], self.PacMan)
                self.CheckGhostMode(self.ghostdict[ghostC], self.PacMan)
                self.GhostPacmanHit(self.ghostdict[ghostC], self.PacMan)

            self.PacMan.move_input(self.gamemap,self.fruits,self.gameScreen)
            self.events.next_lvl(self.PacMan,self.gameScreen,self.gamemap,self.ghostdict,self.fruits)
            if pygame.time.get_ticks() - self.fruits.fruitspawn >= 7000 and self.fruits.active == False:
                self.fruits.create_fruit(self.gameScreen)
            self.events.scoreboard(self.gameScreen,self.PacMan)

            # Update the whole window
            pygame.display.update()
            # Frame per second
            self.clock.tick(60)

    def GhostModeAssign(self, ghost, pacman):
        '''
        Assigning ghosts' mode, ghosts are in 'Scatter' mode in the first 7 second, otherwise ghosts are in
        'Chase' mode. When pacman gets the energizer, ghosts are in 'Frightened' mode when it's not eaten by pacman.

        Ghosts only leave the ghost house, when the number of dots pacman got exceeds it's dotlimt.
        '''

        if ghost.mode == None:
            # ghost in the ghost house, check if the num of dots exceeds the dotlimit
            if pacman.numdot >= ghost.dotlimit:
                # Move the ghost out of ghost house, set it's mode
                leaved = ghost.LeavingGhostHouse()
                if leaved == True:
                    #ghosts are in Scatter mode in the first 7 second for each level
                    if pygame.time.get_ticks() - self.game_start_time <= 7000:
                        ghost.mode = 'Scatter'
                    else:
                        ghost.mode = 'Chase'
            else:
                # Ghost moves in the ghost house back and forth
                ghost.StayInGhostHouse()
        else:
            #ghosts are in Scatter mode in the first 7 second for each level
            if pygame.time.get_ticks() - self.game_start_time <= 7000:
                ghost.mode = 'Scatter'
            else:
                ghost.mode = 'Chase'

        # Check if pacman get the energizer
        if pacman.getenergizer == True and ghost.mode != None and not ghost.eatenbypacman:
            # Ghosts in Frightened mode
            ghost.mode = 'Frightened'
            if self.frightenedtime == None:
                # The beginning time of the Frightened mode
                self.frightenedtime = pygame.time.get_ticks()
            else:
                # The Frightened mode will last 6 seconds
                if pygame.time.get_ticks() - self.frightenedtime >= 6000:
                    # Go back to Chase Mode
                    ghost.mode = 'Chase'
                    self.frightenedtime = None
                    pacman.getenergizer = False

        if pacman.getenergizer == False:
            # reinitialize ghost's eatenbypacman boolean
            ghost.eatenbypacman = False

    def CheckGhostMode(self, ghost, pacman):
        '''
        Ghosts act according to their current mode.
        '''
        pacmanloc = (pacman.x_value//16, pacman.y_value//16)

        if ghost.mode == 'Chase':
            ghosts.Chase(self.gamemap, ghost, pacmanloc, pacman.direction, (self.ghostdict['R'].xtile,self.ghostdict['R'].ytile))
        elif ghost.mode == 'Scatter':
            ghosts.Scatter(self.gamemap, ghost)
        elif ghost.mode == 'Frightened':
            ghosts.Frightened(self.gamemap, ghost)

    def GhostPacmanHit(self, ghost, pacman):
        '''
        Check if ghost and pacman are in the same tile.
        '''
        if pacman.x_value > (ghost.xloc-TileLen) and pacman.x_value < (ghost.xloc+TileLen) \
            and pacman.y_value > (ghost.yloc-TileLen) and pacman.y_value < (ghost.yloc+TileLen):
            # Check if the ghost is in Frightened mode
            if ghost.mode == 'Frightened':
                # Draw the ghost's tile with blank tile
                self.gamemap.legaltile[(ghost.ytile, ghost.xtile)].redrawTile()

                # Send this ghost back to the ghost house
                if ghost.ghostColor == 'R' or ghost.ghostColor == 'P':
                    ghost.xtile, ghost.ytile = ghosts.PinkGHLoc
                    ghost.nextxtile, ghost.nextytile = ghosts.PinkGHLoc
                elif ghost.ghostColor == 'B':
                    ghost.nextxtile, ghost.nextytile = ghosts.BlueGHLoc
                    ghost.xtile, ghost.ytile = ghosts.BlueGHLoc
                elif ghost.ghostColor == 'O':
                    ghost.nextxtile, ghost.nextytile = ghosts.OrangeGHLoc
                    ghost.xtile, ghost.ytile = ghosts.OrangeGHLoc

                # Update ghost's location in pixels
                ghost.xloc = ghost.xtile * TileLen
                ghost.yloc = ghost.ytile * TileLen

                ghost.drawGhost()
                ghost.mode = None
                ghost.eatenbypacman = True

            else:
                # The pacman was eaten by the ghost
                # the pacman's life - 1, if 0, game over
                print('Eaten')
                self.PacMan.lives -= 1
                pygame.time.wait(3000)
                self.events.PacManLives(self.PacMan,self.gameScreen,self.gamemap,self.ghostdict,self.fruits,self.game_start_time)
                self.events.restart_lvl(self.PacMan,self.gameScreen,self.gamemap,self.ghostdict,self.fruits)

if __name__ == "__main__":
    GameMenu()
