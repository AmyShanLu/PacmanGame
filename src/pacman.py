import TileMap
import GameStart
import pygame
import events

class PacMan(pygame.sprite.Sprite):
    ''' PacMan class, which stores the various values of PacMan
        and the various functions needed to move.
        Input:
            image - The image of PacMan.
            gameScreen - The game screen object.'''
    def __init__(self, image, gameScreen):
        self.direction = 'right'
        self.prev_direction = 'right'
        self.x_value = 13*16
        self.y_value = 23*16
        self.lives = 3
        self.image = image
        self.score = 0
        self.numdot = 0
        self.getenergizer = False
        gameScreen.blit(self.image,(self.x_value,self.y_value))

    def move(self, direction, x, y, TileMap, gameScreen):
        ''' Moves and draws the PacMan onto the screen. If it can
            move in the direction that is inputed, PacMan will move
            in that direction. Otherwise try to continue in the
            previous direction PacMan was going to go.'''
        # change the coordinates of PacMan to check if move is valid
        if direction == 'up':
            y = y-1
        elif direction == 'down':
            y = y+1
        elif direction == 'left':
            x = x-1
        elif direction == 'right':
            x = x+1
        # check if coordinates are at the tunnel, then move to the other side
        #of the tunnel
        if int(x/16) == 0 and int(y/16) == 14 and direction == 'left':
            x = 27*16
        elif int(x/16) == 27 and int(y/16) == 14 and direction == 'right':
            x = 0*16
        fail = True
        #for each direction, check if the coordinates are in the legal tile
        #if it is True, change the values and redreaw PacMan
        #and do not go to the fail case
        if direction == 'up':
            if (int(y/16),int((x/16))) in TileMap.legaltile.keys() and x%16 == 0:
                pygame.draw.circle(gameScreen, (0,0,0), (self.x_value+8,self.y_value+8), 11)
                self.x_value = x
                self.y_value = y
                gameScreen.blit(pygame.transform.rotate(self.image,270),(x,y))
                fail = False
        if direction == 'down':
            if (int(y/16)+1,int((x/16))) in TileMap.legaltile.keys() and x%16 == 0 or y%16 == 0:
                pygame.draw.circle(gameScreen, (0,0,0), (self.x_value+8,self.y_value+8), 11)
                self.x_value = x
                self.y_value = y
                gameScreen.blit(pygame.transform.rotate(self.image,90),(x,y))
                fail = False
        if direction == 'left':
            if (int(y/16),int((x/16))) in TileMap.legaltile.keys() and y%16 == 0:
                pygame.draw.circle(gameScreen, (0,0,0), (self.x_value+8,self.y_value+8), 11)
                self.x_value = x
                self.y_value = y
                gameScreen.blit(self.image,(x,y))
                fail = False
        if direction == 'right':
            if (int(y/16),int((x/16)+1)) in TileMap.legaltile.keys() and y%16 == 0 or x%16 == 0:
                pygame.draw.circle(gameScreen, (0,0,0), (self.x_value+8,self.y_value+8), 11)
                self.x_value = x
                self.y_value = y
                gameScreen.blit(pygame.transform.rotate(self.image,180),(x,y))
                fail = False
        #if it fails, try the direction it was previously going if it was
        #different, otherwise do nothing
        if fail:
            if self.direction != self.prev_direction:
                self.direction = self.prev_direction
                self.move(self.direction, self.x_value, self.y_value, TileMap, gameScreen)

    def eat_dots(self, TileMap, fruits, gameScreen):
        ''' Checks if PacMan is in a tile that either contains a dot
            or a energizer, then applies the following effects depending
            on the object eaten.
            Dot - Add 10 to the score and increases numdot by 1.
            Energizer - Makes PacMan's getenergizer to true,
                making the ghosts go into Frightened Mode.
            Fruits - Adds points to the score depending on the type
                of fruit.'''
        #store coordinates of PacMan
        (y,x) = (self.y_value, self.x_value)
        #if PacMan is at the fruit's position,then call the eat fruit function.
        if (int(y/16),int(x/16)) == (17,14):
            fruits.eat_fruit(self,gameScreen)
            #draw rectangle to clear fruit
            pygame.draw.rect(gameScreen,(0,0,0),(14*16,17*16,16,16))
        #if PacMan is on a tile with a active dot on, add 10 to the score and
        #update numdot.
        if TileMap.legaltile[(int(y/16),int(x/16))].dot == True:
            self.score += 10
            self.numdot += 1
            TileMap.legaltile[(int(y/16),int(x/16))].dot = False
        #if PacMan is on a tile with a active energizer on, change getenergizer
        #to true
        if TileMap.legaltile[(int(y/16),int(x/16))].energizer == True:
            self.getenergizer = True
            TileMap.legaltile[(int(y/16),int(x/16))].energizer = False

    def move_input(self, TileMap, fruits, gameScreen):
        '''Reads the input from the user to direct PacMan in a direction,
        then calls functions to move PacMan and eat dots if needed.'''
        #if a key is focused, look at which key is used
        if pygame.key.get_focused():
            #store the previous direction
            self.prev_direction = self.direction
            #Depending on which key is pressed, change PacMan's direction
            if pygame.key.get_pressed()[pygame.K_UP] != 0:
                self.direction = 'up'
            elif pygame.key.get_pressed()[pygame.K_DOWN] != 0:
                self.direction = 'down'
            elif pygame.key.get_pressed()[pygame.K_RIGHT] != 0:
                self.direction = 'right'
            elif pygame.key.get_pressed()[pygame.K_LEFT] != 0:
                self.direction = 'left'
            #call function to eat dots and move PacMan
            self.eat_dots(TileMap, fruits, gameScreen)
            self.move(self.direction, self.x_value, self.y_value, TileMap, gameScreen)
