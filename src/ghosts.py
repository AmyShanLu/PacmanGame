import GameStart
from minheap import MinHeap
import pygame

# Ghosts' tile location in the ghost house
RedGHLoc = (13,14)
PinkGHLoc = (13, 14)
BlueGHLoc = (11, 14)
OrangeGHLoc = (15, 14)

class Ghost:
    '''
    Ghost object.
    ghostColor = 'R': Red ghost
    ghostColor = 'B': Blue ghost
    ghostColor = 'P': Pink ghost
    ghostColor = 'O': Orange ghost
    '''

    def __init__(self, ghostColor, gameScreen, gamemap):
        self.gameScreen = gameScreen
        self.ghostColor = ghostColor
        self.gamemap = gamemap
        self.gspeed = 1
        # when ghost is in the ghost house, mode = None
        self.mode = None

        # The moving direction of the ghost, (after leaving the ghost house) initially to the left, 'L'
        self.movingdir = 'L'

        # Eaten by pacman
        self.eatenbypacman = False

        #Initialize the ghost
        if ghostColor == 'R':
            # Ghost's current tile
            self.xtile = 13
            self.ytile = 11

            # Initially, red ghost is outside the ghost house, so mode = Scatter
            self.mode = 'Scatter'
            self.dotlimit = -1

            # The path that ghost should follow to leave the ghost house
            self.leavingGHPath = [RedGHLoc, (13,13), (13,12), (13,11)]

        elif ghostColor == 'B':
            self.xtile, self.ytile = BlueGHLoc
            self.dotlimit = 20

            # The path that ghost should follow to leave the ghost house
            self.leavingGHPath = [BlueGHLoc, (12,14), (13,14), (13,13), (13,12), (13,11)]

            #Indicate whether the ghost start following pink ghost's leaving GH path
            self.PinkPath = False

        elif ghostColor == 'P':
            self.xtile, self.ytile = PinkGHLoc
            self.dotlimit = 0

            # The path that ghost should follow to leave the ghost house
            self.leavingGHPath = [PinkGHLoc, (13,13), (13,12), (13,11)]

        elif ghostColor == 'O':
            self.xtile, self.ytile = OrangeGHLoc
            self.dotlimit = 40

            # The path that ghost should follow to leave the ghost house
            self.leavingGHPath = [OrangeGHLoc, (14,14), (13,14), (13,13), (13,12), (13,11)]
            #Indicate whether the ghost start following pink ghost's leaving GH path
            self.PinkPath = False

        # Ghost loc in pixels
        self.xloc = self.xtile*GameStart.TileLen
        self.yloc = self.ytile*GameStart.TileLen

        # Ghost's next tile
        self.nextxtile, self.nextytile = self.NextTile()

        # Initial draw ghost
        self.drawGhost()

    def drawGhost(self):
        '''
        Draw the ghost according to their mode, moving direction, and ghost color.
        '''

        if self.mode == 'Frightened':
            self.gameScreen.blit(GameStart.FrightenedGImg, (self.xloc, self.yloc))
        else:
            if self.ghostColor == 'R':
                if self.movingdir == 'L':
                    self.gameScreen.blit(GameStart.RedGLImg, (self.xloc, self.yloc))
                elif self.movingdir == 'R':
                    self.gameScreen.blit(GameStart.RedGRImg, (self.xloc, self.yloc))
                elif self.movingdir == 'U':
                    self.gameScreen.blit(GameStart.RedGUImg, (self.xloc, self.yloc))
                elif self.movingdir == 'D':
                    self.gameScreen.blit(GameStart.RedGDImg, (self.xloc, self.yloc))

            elif self.ghostColor == 'B':
                if self.movingdir == 'L':
                    self.gameScreen.blit(GameStart.BlueGLImg, (self.xloc, self.yloc))
                elif self.movingdir == 'R':
                    self.gameScreen.blit(GameStart.BlueGRImg, (self.xloc, self.yloc))
                elif self.movingdir == 'U':
                    self.gameScreen.blit(GameStart.BlueGUImg, (self.xloc, self.yloc))
                elif self.movingdir == 'D':
                    self.gameScreen.blit(GameStart.BlueGDImg, (self.xloc, self.yloc))

            elif self.ghostColor == 'P':
                if self.movingdir == 'L':
                    self.gameScreen.blit(GameStart.PinkGLImg, (self.xloc, self.yloc))
                elif self.movingdir == 'R':
                    self.gameScreen.blit(GameStart.PinkGRImg, (self.xloc, self.yloc))
                elif self.movingdir == 'U':
                    self.gameScreen.blit(GameStart.PinkGUImg, (self.xloc, self.yloc))
                elif self.movingdir == 'D':
                    self.gameScreen.blit(GameStart.PinkGDImg, (self.xloc, self.yloc))

            elif self.ghostColor == 'O':
                if self.movingdir == 'L':
                    self.gameScreen.blit(GameStart.OrangeGLImg, (self.xloc, self.yloc))
                elif self.movingdir == 'R':
                    self.gameScreen.blit(GameStart.OrangeGRImg, (self.xloc, self.yloc))
                elif self.movingdir == 'U':
                    self.gameScreen.blit(GameStart.OrangeGUImg, (self.xloc, self.yloc))
                elif self.movingdir == 'D':
                    self.gameScreen.blit(GameStart.OrangeGDImg, (self.xloc, self.yloc))

    def NextTile(self):
        '''
        Calculate the ghost's next tile location according to it's moving direction
        '''
        if self.movingdir == 'L':
            return self.xtile-1, self.ytile
        elif self.movingdir == 'R':
            return self.xtile+1, self.ytile
        elif self.movingdir == 'U':
            return self.xtile, self.ytile-1
        elif self.movingdir == 'D':
            return self.xtile, self.ytile+1

    def NextLoc(self):
        '''
        Update the ghost's next location in pixels according to it's moving direction and moving speed
        '''
        if self.movingdir == 'L':
            self.xloc -= self.gspeed
        elif self.movingdir == 'R':
            self.xloc += self.gspeed
        elif self.movingdir == 'U':
            self.yloc -= self.gspeed
        elif self.movingdir == 'D':
            self.yloc += self.gspeed

    def GhostMoving(self):
        '''
        Moving the ghost according to its moving direction by it's moving speed
        '''
        if (self.ytile, self.xtile) in self.gamemap.legaltileLoc:
            # Draw the ghost's original tile with the blank tile
            self.gamemap.legaltile[(self.ytile, self.xtile)].redrawTile()
        elif (self.ytile, self.xtile) in set(self.gamemap.ghosthousetile.keys()):
            self.gamemap.ghosthousetile[(self.ytile, self.xtile)].redrawTile()

        # Calculate the ghost's current location according to it's moving direction
        self.NextLoc()
        # Draw ghost on this current location
        self.drawGhost()

    def CalMovingDir(self, next_tile):
        '''
        Calculate the next moving direction base on the tile with minimun estimated dist to targetlocation
        and the current ghost tile location.
        '''
        if next_tile[0] - self.xtile == -1:
            self.movingdir = 'L'
        elif next_tile[0] - self.xtile == 1:
            self.movingdir = 'R'
        elif next_tile[1] - self.ytile == -1:
            self.movingdir = 'U'
        elif next_tile[1] - self.ytile == 1:
            self.movingdir = 'D'
        else:
            print("ERROR in CalMovingDir func")

    def LeavingGhostHouse(self):
        '''
        Ghost leaving the ghost house from their ghost house tile to the tile (13, 11)
        '''
        def RorPLeaving(self):
            '''
            Leaving ghost path for red or pink ghost
            '''
            if self.xtile * GameStart.TileLen == self.xloc and self.ytile * GameStart.TileLen == self.yloc and (self.xtile, self.ytile) == PinkGHLoc:
                # ghosts are in their initial location
                self.movingdir = 'U'
                # Ghost's next tile
                self.nextxtile, self.nextytile = self.NextTile()

            if self.nextxtile * GameStart.TileLen == self.xloc and self.nextytile * GameStart.TileLen == self.yloc:
                # The ghost moved to it's next tile
                self.xtile, self.ytile =  self.nextxtile, self.nextytile

                if (self.xtile, self.ytile) == self.leavingGHPath[-1]:
                    # Already leave the ghost house
                    self.movingdir = 'L'
                    # Ghost's next tile
                    self.nextxtile, self.nextytile = self.NextTile()

                    if self.ghostColor == 'B' or self.ghostColor == 'O':
                        #Ghost leaving GH
                        self.PinkPath = False
                    return True

                # Ghost's next tile
                self.nextxtile, self.nextytile = self.NextTile()

            # Move the ghost
            self.GhostMoving()
            return False

        def BorOLeaving(self):
            '''
            Blue and Orange ghosts follow the same path as Red or Pink ghost after they reach RedGHLoc = (13, 14)
            '''
            if self.ghostColor == 'B':
                if (self.nextxtile, self.nextytile) == BlueGHLoc or (self.nextxtile, self.nextytile) == (BlueGHLoc[0], BlueGHLoc[1]-1):
                    # Redraw tiles
                    self.gamemap.ghosthousetile[(self.ytile, self.xtile)].redrawTile()
                    self.gamemap.ghosthousetile[(self.nextytile, self.nextxtile)].redrawTile()

                    # Initialize blue ghost to BlueGHLoc, it moves to right before it reaches RedGHLoc
                    self.xtile, self.ytile = BlueGHLoc
                    self.xloc = self.xtile * GameStart.TileLen
                    self.yloc = self.ytile * GameStart.TileLen
                    self.movingdir = 'R'

                    # Ghost's next tile
                    self.nextxtile, self.nextytile = self.NextTile()

            elif self.ghostColor == 'O':
                if (self.nextxtile, self.nextytile) == OrangeGHLoc or (self.nextxtile, self.nextytile) == (OrangeGHLoc[0], OrangeGHLoc[1]-1):
                    # Redraw tiles
                    self.gamemap.ghosthousetile[(self.ytile, self.xtile)].redrawTile()
                    self.gamemap.ghosthousetile[(self.nextytile, self.nextxtile)].redrawTile()

                    # Initialize blue ghost to BlueGHLoc, it moves to right before it reaches RedGHLoc
                    self.xtile, self.ytile = OrangeGHLoc
                    self.xloc = self.xtile * GameStart.TileLen
                    self.yloc = self.ytile * GameStart.TileLen
                    self.movingdir = 'L'

                    # Ghost's next tile
                    self.nextxtile, self.nextytile = self.NextTile()

            if self.nextxtile * GameStart.TileLen == self.xloc and self.nextytile * GameStart.TileLen == self.yloc:
                # The ghost moved to it's next tile
                self.xtile, self.ytile =  self.nextxtile, self.nextytile

                if (self.xtile, self.ytile) == PinkGHLoc:
                    #The ghost moved to PinkGHLoc
                    self.PinkPath = True

                if self.PinkPath == True:
                    return RorPLeaving(self)

                # Ghost's next tile
                self.nextxtile, self.nextytile = self.NextTile()

            # Move the ghost
            self.GhostMoving()
            return False

        if self.ghostColor == 'R' or self.ghostColor == 'P':
            return RorPLeaving(self)
        else:
            return BorOLeaving(self)

    def StayInGhostHouse(self):
        '''
        Ghost moves in the ghost house back and forth
        Red and Pink ghosts will leave the ghost house immediately once they enter the ghost house
        '''
        if self.movingdir == 'L':
            # When the ghost is at it's initial location in the ghost house, move up by one tile in the ghost house
            self.movingdir = 'U'
            # Ghost's next tile
            self.nextxtile, self.nextytile = self.NextTile()

        if self.nextxtile * GameStart.TileLen == self.xloc and self.nextytile * GameStart.TileLen == self.yloc:
            # The ghost has moved to the next tile, change it's moving direction
            if self.movingdir == 'U':
                self.movingdir = 'D'
            elif self.movingdir == 'D':
                self.movingdir = 'U'

            self.xtile, self.ytile = self.nextxtile, self.nextytile
            # Ghost's next tile
            self.nextxtile, self.nextytile = self.NextTile()

        self.GhostMoving()

class Chase:
    '''
    Chase mode of the ghost, ghosts will chase the pac man
    Different ghosts have different target locations.

    Input argument: tilemap: the tile map object
                    ghostColor: The color of the ghost
                    ghostlocation: the tile loction of the ghost (xtile, ytile)
                    pacmanlocation: the tile loction of the pac man
                    pacmovingdir: the moving direction of the pac man ('U', 'D', 'L', 'R')
                    redghostlocation: the red ghost's location
    '''
    def __init__(self, tilemap, ghost, pacmanlocation, pacmovingdir, redghostlocation):
        self.tilemap = tilemap
        self.ghost = ghost

        if self.ghost.nextxtile * GameStart.TileLen == self.ghost.xloc and self.ghost.nextytile * GameStart.TileLen == self.ghost.yloc:
            # The ghost has already reached it's previous next tile, it needs to find the new next tile to move to
            self.ghostlocation = (self.ghost.nextxtile, self.ghost.nextytile)
            self.targetlocation = self.ghosttargetlocation(pacmanlocation, pacmovingdir, redghostlocation)

            # The shortest path from the ghost to it's target
            self.path = self.pathreturn()

            if len(self.path) > 1:
                # The ghost's current tile is it's previous next tile
                self.ghost.xtile, self.ghost.ytile = self.ghost.nextxtile, self.ghost.nextytile
                # The next tile that the ghost moving to is self.path[1]
                self.ghost.nextxtile, self.ghost.nextytile = self.path[1]
                # Calculate the new moving direction
                self.ghost.CalMovingDir(self.path[1])
            else:
                #Switch ghost's previous tile and current tile
                oldtile = self.ghost.xtile, self.ghost.ytile
                self.ghost.xtile, self.ghost.ytile = self.ghost.nextxtile, self.ghost.nextytile
                self.ghost.nextxtile, self.ghost.nextytile = oldtile[0], oldtile[1]
                # Calculate the new moving direction
                self.ghost.CalMovingDir((self.ghost.nextxtile, self.ghost.nextytile))

        # Moving the ghost by 1 pixel towards it's  moving direction
        self.ghost.GhostMoving()

    def pathreturn(self):
        '''
        return the shortest path list
        '''
        path = shortestpath(self.tilemap, self.ghostlocation, self.targetlocation)
        return path

    def ghosttargetlocation(self, pacmanlocation, pacmovingdir, redghostlocation):
        '''
        Calcultate the ghost's targetlocation
        Red ghost: target location: Pac man's current tile
        Pink ghost: target location: 4 tiles away from pac man in pac man's moving direction
                            (if this tile not walkable, use the cloest walkable tile)
                            Up: 4 tiles left and 4 tiles up
                            Down: 4 tiles below
                            Left: 4 tiles left
                            Right: 4 tiles right
        Blue ghost: target location: 2 tiles away from pac man in pac man's moving direction,
                            double this tile's distance away from the red ghost
        Orange ghost: target location: pac man's current tile if it's 8 tiles away from pac man
                                otherwise, scatter mode tile

        Input Arguments: tilemap: the tile map object
                         ghostColor: The color of the ghost
                         ghostlocation: the tile loction of the ghost (xtile, ytile)
                         pacmanlocation: the tile loction of the pac man
                         pacmovingdir: the moving direction of the pac man ('U', 'D', 'L', 'R')
                         redghostlocation: the red ghost's location
        '''
        def PorBtarLoc(ghost, pacmanlocation, offset):
            if pacmovingdir == 'up':
                targetlocation = (pacmanlocation[0]-offset, pacmanlocation[1]-offset)
            elif pacmovingdir == 'down':
                targetlocation = (pacmanlocation[0], pacmanlocation[1]+offset)
            elif pacmovingdir == 'left':
                targetlocation = (pacmanlocation[0]-offset, pacmanlocation[1])
            elif pacmovingdir == 'right':
                targetlocation = (pacmanlocation[0]+offset, pacmanlocation[1])
            return targetlocation

        def closestWalkableTile(tilemap, targetlocation):
            '''
            Find the cloest walkable tile on the map to the targetlocation
            '''
            mindist = float('inf')
            closesttile = None
            for node in tilemap.legaltileLoc:
                if abs(node[1]-targetlocation[0]) + abs(node[0]-targetlocation[1]) < mindist:
                    mindist = abs(node[1]-targetlocation[0]) + abs(node[0]-targetlocation[1])
                    closesttile = node
            return (closesttile[1], closesttile[0])

        if self.ghost.ghostColor == 'R':
            targetlocation = pacmanlocation
        elif self.ghost.ghostColor == 'P':
            targetlocation = PorBtarLoc(self.ghost, pacmanlocation, 4)
        elif self.ghost.ghostColor == 'B':
            caltarloc = PorBtarLoc(self.ghost, pacmanlocation, 2)
            targetlocation = (2*caltarloc[0]-redghostlocation[0], 2*caltarloc[1]-redghostlocation[1])

        elif self.ghost.ghostColor == 'O':
            if abs(pacmanlocation[0]-self.ghost.xtile) > 8 or abs(pacmanlocation[1]-self.ghost.ytile) > 8:
                targetlocation = pacmanlocation
            else:
                # It's targetlocation is it's Scatter mode's target location
                targetlocation = (7,28)

        # Check if the targetlocation is walkable if not, find the closest walkable tile location
        if (targetlocation[1], targetlocation[0]) not in self.tilemap.legaltileLoc:
            targetlocation = closestWalkableTile(self.tilemap, targetlocation)

        return targetlocation

class Scatter:
    '''
    Scatter mode of the ghost
    In this mode, ghosts go to their own scatter target located at each corner of the map
    '''
    def __init__(self, tilemap, ghost):
        self.tilemap = tilemap
        self.ghost = ghost

        # Assign the targetlocation for the ghost
        self.targetlocation = self.assigntarget()

        if self.ghost.nextxtile * GameStart.TileLen == self.ghost.xloc and self.ghost.nextytile * GameStart.TileLen == self.ghost.yloc:
            # The ghost has already reached it's previous next tile, it needs to find the new next tile to move to
            self.pathfinding()

        # Moving the ghost by 1 pixel towards it's  moving direction
        self.ghost.GhostMoving()

    def assigntarget(self):
        '''
        Assign the target location for the ghost, based on their color
        '''
        if self.ghost.ghostColor == 'R':
            # Red ghost's target location is the top right corner of the map
            return (24,2)
        elif self.ghost.ghostColor == 'P':
            # Pink ghost's target location is the top left corner of the map
            return (3,2)
        elif self.ghost.ghostColor == 'O':
            # Orange ghost's target location is the bottom left corner of the map
            return (7,28)
        elif self.ghost.ghostColor == 'B':
            # Blue ghost's target location is the bottom right corner of the map
            return (20,28)

    def pathfinding(self):
        '''
        Check the neighbours of the next tile, estimate their distance to the targetlocation,
        choose the tile with the smallest estimated distance as the tile moving to next time,
        calculate the next moving direction, save this direction to ghost's movingdir.
        '''
        # Find the neighbours of the ghost's current tile after moving
        neighbourtiles = nodeneighbour(self.tilemap, (self.ghost.nextxtile, self.ghost.nextytile))
        min_dist = float('inf')
        min_tile = None

        if len(neighbourtiles) == 1:
            # Go back to the previous node
            min_tile = (self.ghost.xtile, self.ghost.ytile)
        else:
            for i in neighbourtiles:
                if i != (self.ghost.xtile, self.ghost.ytile):
                    tiledist = heuristiccost(i, self.targetlocation)
                    if tiledist < min_dist:
                        min_dist = tiledist
                        min_tile = i

        # The ghost's current tile is it's previous next tile
        self.ghost.xtile, self.ghost.ytile = self.ghost.nextxtile, self.ghost.nextytile
        # min_tile is ghost's next tile
        self.ghost.nextxtile, self.ghost.nextytile = min_tile
        # Calculate the new moving direction
        self.ghost.CalMovingDir(min_tile)

class Frightened:
    '''
    Frightened mode of the ghost
    Ghosts wander around the map and it picks a way to turn at the intersection randomly
    '''
    def __init__(self, tilemap, ghost):
        self.tilemap = tilemap
        self.ghost = ghost

        if self.ghost.nextxtile * GameStart.TileLen == self.ghost.xloc and self.ghost.nextytile * GameStart.TileLen == self.ghost.yloc:
            # The ghost has already reached it's previous next tile, it needs to find the new next tile to move to
            self.wander()

        # Moving the ghost by 1 pixel towards it's  moving direction
        self.ghost.GhostMoving()

    def wander(self):
        # Find the neighbours of the ghost's current tile after moving
        neighbourtiles = nodeneighbour(self.tilemap, (self.ghost.nextxtile, self.ghost.nextytile))

        if len(neighbourtiles) == 1:
            # Go back to the previous node
            next_tile = (self.ghost.xtile, self.ghost.ytile)
        else:
            # Remove the previous tile that the ghost was on
            neighbourtiles.remove((self.ghost.xtile, self.ghost.ytile))
            # Pick one neighbour tile to turn next time randomly
            import random
            next_tile = neighbourtiles[random.randrange(len(neighbourtiles))]

        # The ghost's current tile is it's previous next tile
        self.ghost.xtile, self.ghost.ytile = self.ghost.nextxtile, self.ghost.nextytile
        # next_tile is ghost's next tile
        self.ghost.nextxtile, self.ghost.nextytile = next_tile
        # Calculate the new moving direction
        self.ghost.CalMovingDir(next_tile)

def heuristiccost(currentnode, goalnode):
    '''
    Calculte the estimated distance between the current node and the goal node
    '''
    return abs(currentnode[0]-goalnode[0]) + abs(currentnode[1]-goalnode[1])

def nodeneighbour(tilemap, currentnode):
    '''
    Find the walkable neighbours of the currentnode on the map

    Input Arguments: tilemap: the tile map object
                     currentnode: (xindex, yindex)
            Note: walkable tiles set: tilemap.legaltileLoc: (i, j), i: y index, j: x index

    Return: neighbournodes: A list containing the walkable neighbours of the currentnode
    '''

    neighbournodes = []
    if (currentnode[1], currentnode[0]-1) in tilemap.legaltileLoc:
        neighbournodes.append((currentnode[0]-1, currentnode[1]))

    if (currentnode[1], currentnode[0]+1) in tilemap.legaltileLoc:
        neighbournodes.append((currentnode[0]+1, currentnode[1]))

    if (currentnode[1]-1, currentnode[0]) in tilemap.legaltileLoc:
        neighbournodes.append((currentnode[0], currentnode[1]-1))

    if (currentnode[1]+1, currentnode[0]) in tilemap.legaltileLoc:
        neighbournodes.append((currentnode[0], currentnode[1]+1))

    return neighbournodes


def shortestpath(tilemap, startnode, goalnode):
    '''
        Find the shortestpath between the startnode and the goalnode

        Input Arguments: tilemap: the tile map object
                         startnode: the location of start tile on the map (xtile, ytile)
                         goalnode: the location of the goal tile on the map (xtile, ytile)
                Note: startnode and goalnode must be walkable (in the tilemap.legaltileLoc set)

        Return: path: A shortest path list containing the tile locations from start tile to goal tile
    '''
    # reached dict, key: v_to, value: (actualcost, v_from)
    reached = dict()

    # explorenode minheap, key: totalcost, value: (actualcost, v_from, v_to)
    # totalcost = actualcost + heuristiccost
    explorenode = MinHeap()
    explorenode.add(0, (0, startnode, startnode))

    # The node to be explored, key: v_to, value: (actualcost, v_from)
    explorenodedict = dict()
    explorenodedict[startnode] = (0, startnode)

    while len(explorenode) > 0:
        # Get the node with minimun total cost
        totalcost, checknode = explorenode.pop_min()

        actualcost, v_from, v_to = checknode

        if v_to in reached:
            # node has already been reached
            continue

        # Add v_to to reached dict
        reached[v_to] = (actualcost, v_from)
        # Remove v_to from explorenodedict
        del explorenodedict[v_to]

        if v_to == goalnode:
            # reached goal
            break

        # Explore the neighbour nodes of v_to
        for neighbournode in nodeneighbour(tilemap, v_to):
            if neighbournode in reached:
                # Don't do anything if the neighbournode has already been reached
                continue

            # Check if the neighbournode is in the explorenode dict
            if neighbournode in explorenodedict:
                # Check if the new actualcost (v_to's actualcost + 1) is less than the old actualcost
                if explorenodedict[neighbournode][0] > (reached[v_to][0] + 1):
                    # Update the actualcost and v_from for neighbournode
                    explorenodedict[neighbournode] = (reached[v_to][0] + 1, v_to)
                    newtotalcost = reached[v_to][0] + 1 + heuristiccost(neighbournode, goalnode)

                    # Add the neighbournode with newtotalcost to minheap
                    explorenode.add(newtotalcost, (reached[v_to][0] + 1, v_to, neighbournode))
            else:
                # Add neighbournode to explorenodedict
                explorenodedict[neighbournode] = (reached[v_to][0] + 1, v_to)

                # Add neighbournode to explorenode minheap
                totalcost = reached[v_to][0] + 1 + heuristiccost(neighbournode, goalnode)
                explorenode.add(totalcost, (reached[v_to][0] + 1, v_to, neighbournode))

    # The path from start to dest
    path = []
    if goalnode in reached:
        path.append(goalnode)

        while reached[goalnode][1] != startnode:
            path.append(reached[goalnode][1])
            goalnode = reached[goalnode][1]

        if goalnode != startnode:
            path.append(startnode)

        path.reverse()
    return path
