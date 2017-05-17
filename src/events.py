import pacman
import TileMap
import pygame
import GameStart
import ghosts
import random

class events:
    ''' An class which stores the level on text used to display on gameScreen,
        and various functions for the game.'''
    def __init__(self):
        self.level = 1
        self.text = pygame.font.SysFont("comicsansms",16)

    def next_lvl(self,PacMan,gameScreen,TileMap,ghostdict,fruits):
        ''' If PacMan eats all the dots, activate all the tiles that had dots
            and energizers, add to the level variable, then restart the level.'''
        #if PacMan numdot equals 240, which is the number of dots in a level
        if PacMan.numdot == 240:
            PacMan.numdot = 0
            #update level
            self.level += 1
            #give time to process beating level
            pygame.time.wait(3000)
            #update the tiles to have active dots and energizers
            for t in TileMap.legaltile:
                TileMap.legaltile[t].initialDrawTile()
            #restart the level
            self.restart_lvl(PacMan,gameScreen,TileMap,ghostdict,fruits)

    def restart_lvl(self,PacMan,gameScreen,TileMap,ghostdict,fruits):
        ''' Restarts the level with the ghosts and PacMan at their
            original positions. Also redraws the tiles and the active
            dot and energizers on the map. Resets the fruit timer and
            despawns the fruit.'''
        #redraws all the legal tiles
        for t in TileMap.legaltile:
            TileMap.legaltile[t].redrawTile()
        #resets the ghosts to spawn and their numdot is adjusted.
        #the ghosts will be in a state that is similiar to the
        #start of the game.
        for g in ghostdict.keys():
            ghostdict[g].mode = None
            ghostdict[g].movingdir = 'L'
            if ghostdict[g].ghostColor == 'R':
                ghostdict[g].xtile = 13
                ghostdict[g].ytile = 11
                ghostdict[g].mode = 'Scatter'
                ghostdict[g].dotlimit = PacMan.numdot -1
            if ghostdict[g].ghostColor == 'B':
                ghostdict[g].xtile, ghostdict[g].ytile = ghosts.BlueGHLoc
                ghostdict[g].PinkPath = False
                ghostdict[g].dotlimit = PacMan.numdot +20
            if ghostdict[g].ghostColor == 'P':
                ghostdict[g].xtile, ghostdict[g].ytile = ghosts.PinkGHLoc
                ghostdict[g].dotlimit = PacMan.numdot
            if ghostdict[g].ghostColor == 'O':
                ghostdict[g].xtile, ghostdict[g].ytile = ghosts.OrangeGHLoc
                ghostdict[g].PinkPath = False
                ghostdict[g].dotlimit = PacMan.numdot +40
            ghostdict[g].xloc = ghostdict[g].xtile*GameStart.TileLen
            ghostdict[g].yloc = ghostdict[g].ytile*GameStart.TileLen
            ghostdict[g].nextxtile, ghostdict[g].nextytile = ghostdict[g].NextTile()
            ghostdict[g].drawGhost()
        #reset the PacMan's position
        PacMan.x_value = 13*16
        PacMan.y_value = 23*16
        #despawn the fruit
        fruits.active = False
        #reset the fruit type
        fruits.fruit_num = random.randint(0,100)
        pygame.draw.rect(gameScreen,(0,0,0),(8*16 + 10,17*16,7*16,16))
        #redraw PacMan at spawn
        gameScreen.blit(PacMan.image,(PacMan.x_value,PacMan.y_value))
        #inform the player the game is starting
        gameScreen.blit(self.text.render("GET READY",False,(250,250,250),None),(12*16,17*16))
        pygame.display.update()
        pygame.draw.rect(gameScreen,(0,0,0),(12*16,17*16,5*16,16))
        #wait for player to process it
        pygame.time.wait(3000)
        #reset the fruit timer
        fruits.fruitspawn = pygame.time.get_ticks()

    def scoreboard(self,gameScreen,PacMan):
        '''Displays the score of the current PacMan player.'''
        gameScreen.blit(self.text.render("Score",False,(250,250,250),None),(500,50))
        #clears the previous score
        pygame.draw.rect(gameScreen,(0,0,0),(500,100,200,50))
        #draw new score
        gameScreen.blit(self.text.render(str(PacMan.score),False,(250,250,250),None),(500,100))

    def PacManLives(self,PacMan,gameScreen,TileMap,ghostdict,fruits,game_start_time):
        '''Displays the amount of extra lives that PacMan has. If PacMan
            has no more lives, then initiate the Game Over function.'''
        #if no more lives initiate GameOver
        if PacMan.lives == 0:
            self.GameOver(PacMan,gameScreen,TileMap,ghostdict,fruits,game_start_time)
        #else draw the amount of extra lives that PacMan has.
        elif PacMan.lives == 1:
            pygame.draw.rect(gameScreen,(0,0,0),(50,500,100,100))
        elif PacMan.lives == 2:
            pygame.draw.rect(gameScreen,(0,0,0),(50,500,100,100))
            gameScreen.blit(PacMan.image,(50,500))
        elif PacMan.lives == 3:
            pygame.draw.rect(gameScreen,(0,0,0),(50,500,100,100))
            gameScreen.blit(PacMan.image,(50,500))
            gameScreen.blit(PacMan.image,(100,500))

    def high_score(self,PacMan,gameScreen):
        ''' Stores and displays the 10 highest scores gotten in the game.
            It takes the current PacMan's score and sorts the score with
            the previous scores that were stored. If there are no previous
            scores, makes a file that will store the values.
            Input: score - the PacMan's score.
            Returns: High Scores.txt - a text file that contains the 10
                        highest scores in PacMan.'''
        #place to store scores temporary.
        scores = []
        #if there is a file already, grab the scores, otherwise do nothing.
        try:
            file = open('High Scores.txt','r')
            for line in file:
                print(line)
                scores.append(int(line))
        except:
            pass
        #add new score
        scores.append(PacMan.score)
        sort_scores = sorted(scores,reverse = True)
        #grab the first 10 scores
        sort_scores = sort_scores[:10]
        #erase the old scores.
        pygame.draw.rect(gameScreen,(0,0,0),(500,200,100,150))
        #draw the new scores.
        gameScreen.blit(self.text.render("HIGH SCORES",False,(250,250,250),None),(500,200))
        file = open('High Scores.txt','w')
        #store the new scores into the text file.
        for score in range(len(sort_scores)):
            file.write(str(sort_scores[score])+'\n')
            gameScreen.blit(self.text.render(str(score+1)+'. '+str(sort_scores[score]),False,(250,250,250),None),(500,210+10*score))

    def GameOver(self,PacMan,gameScreen,TileMap,ghostdict,fruits, game_start_time):
        ''' Displays the high score after the player loses the game, then asks
            the player to press enter to play again. If the player presses
            enter, restarts the whole game and start a new game.'''
        #inform the player
        gameScreen.blit(self.text.render("GAME OVER",False,(250,250,250),None),(12*16,17*16))
        pygame.display.update()
        pygame.time.wait(3000)
        #display the high scores.
        self.high_score(PacMan,gameScreen)
        pygame.draw.rect(gameScreen,(0,0,0),(12*16,17*16,5*16,16))
        #tell the player to play again
        gameScreen.blit(self.text.render("PRESS ENTER TO PLAY AGAIN",False,(250,250,250),None),(8*16 + 10,17*16))
        pygame.display.update()
        Exit = False
        #If they press the 'x' button, exit. If they press enter, reset the
        #game, otherwise, do nothing.
        while not Exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #Hits 'x'
                    pygame.quit()
                    quit()
            if pygame.key.get_pressed()[pygame.K_RETURN] != 0:
                #reset score, lives, numdot, and level.
                PacMan.score = 0
                PacMan.lives = 3
                PacMan.numdot = 0
                #draw the PacMan lives
                self.PacManLives(PacMan,gameScreen,TileMap,ghostdict,fruits,game_start_time)
                #reinitialize the tiles
                for t in TileMap.legaltile:
                    TileMap.legaltile[t].initialDrawTile()
                self.level = 1
                #reset game_start_time
                game_start_time = pygame.time.get_ticks()
                Exit = True

class fruits:
    ''' Class for fruit. Carries the types of fruits, the amount of points,
        the time that it spawns, and if it it active.'''
    def __init__(self):
        #store a random interger from 0 to 100, used for later.
        self.fruit_num = random.randint(0,100)
        self.points = 0
        self.active = False
        self.fruitspawn = pygame.time.get_ticks()
        #store the images of the fruits.
        import os
        from os.path import dirname
        self.cherry = pygame.image.load(os.path.join(dirname("images"), "images", 'Cherry.png'))
        self.strawberry = pygame.image.load(os.path.join(dirname("images"), "images", 'Strawberry.png'))
        self.orange = pygame.image.load(os.path.join(dirname("images"), "images", 'Orange.png'))
        self.apple = pygame.image.load(os.path.join(dirname("images"), "images", 'Apple.png'))
        self.melon = pygame.image.load(os.path.join(dirname("images"), "images", 'Melon.png'))
        self.bell = pygame.image.load(os.path.join(dirname("images"), "images", 'Bell.png'))
        self.galaxian = pygame.image.load(os.path.join(dirname("images"), "images", 'Galaxian.png'))
        self.key = pygame.image.load(os.path.join(dirname("images"), "images", 'Key.png'))

    def create_fruit(self,gameScreen):
        ''' Creates the fruit onto the map and assigns the points accordingly.
            Uses the random number generated to choose a fruit.
            0-44: Brings a cherry, worth 100 points.
            45-64: Brings a strawberry, worth 300 points.
            65-79: Brings a orange, worth 500 points.
            80-89: Brings a apple, worth 700 points.
            90-94: Brings a melon, worth 1000 points.
            95-97: Brings a galaxian, worth 2000 points.
            98-99: Brings a bell, worth 3000 points.
            100: Brings a key, worth 5000 points.'''
        #active the fruit
        self.active = True
        #draw the fruit and assign the points.
        if self.fruit_num <45:
            self.points = 100
            gameScreen.blit(self.cherry,(14*16,17*16))
        elif self.fruit_num <65:
            self.points = 300
            gameScreen.blit(self.strawberry,(14*16,17*16))
        elif self.fruit_num <80:
            self.points = 500
            gameScreen.blit(self.orange,(14*16,17*16))
        elif self.fruit_num <90:
            self.points = 700
            gameScreen.blit(self.apple,(14*16,17*16))
        elif self.fruit_num <95:
            self.points = 1000
            gameScreen.blit(self.melon,(14*16,17*16))
        elif self.fruit_num <98:
            self.points = 2000
            gameScreen.blit(self.galaxian,(14*16,17*16))
        elif self.fruit_num <100:
            self.points = 3000
            gameScreen.blit(self.bell,(14*16,17*16))
        else:
            self.points = 5000
            gameScreen.blit(self.key,(14*16,17*16))

    def eat_fruit(self, PacMan, gameScreen):
        ''' Gives PacMan the fruit points if he is in the tile where
            the fruit is. Assigns a new random number, and resets the
            fruit timer.'''
        #if the fruit is active, deactivate the fruit, assign a new number,
        #and reset the timer.
        if self.active == True:
            PacMan.score += self.points
            self.active = False
            self.fruit_num = random.randint(0,100)
            pygame.draw.rect(gameScreen,(0,0,0),(14*16,17*16,16,16))
            self.fruitspawn = pygame.time.get_ticks()
