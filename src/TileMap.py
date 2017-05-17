from Tile import Tile

class Tilemap:
    '''
    Defining the pattern of the tile map (A list of char string) 28 X 36 tiles
    '0': The tile is a blank dead space
    'H': The tile is a dead space and has a horizontal blue line (image of map)
    'V': The tile is a dead space and has a vertical blue line (image of map)
    '2': The tile is a dead space and has a blue bottom right corner (image of map)
    '3': The tile is a dead space and has a blue bottom left corner (image of map)
    '4': The tile is a dead space and has a blue top right corner (image of map)
    '5': The tile is a dead space and has a blue top left corner (image of map)
    'P': The tile is a dead space and has a pink line (door of the ghosts house)
    'G': The tile is a dead space in the ghost house, ghost can only exit the house
    'D': The tile is a legal space, containing a dot
    'E': The tile is a legal space, containing a energizer
    '1': The tile is a blank legal space

    Input Argument: gameScreen: the gameScreen window from GameStart
    '''

    def __init__(self, gameScreen):
        # The tile map
        tilemap = ["2HHHHHHHHHHHH32HHHHHHHHHHHH3",
                    "VDDDDDDDDDDDDVVDDDDDDDDDDDDV",
                    "VD2HH3D2HHH3DVVD2HHH3D2HH3DV",
                    "VEV00VDV000VDVVDV000VDV00VEV",
                    "VD4HH5D4HHH5D45D4HHH5D4HH5DV",
                    "VDDDDDDDDDDDDDDDDDDDDDDDDDDV",
                    "VD2HH3D23D2HHHHHH3D23D2HH3DV",
                    "VD4HH5DVVD4HH32HH5DVVD4HH5DV",
                    "VDDDDDDVVDDDDVVDDDDVVDDDDDDV",
                    "4HHHH3DV4HH31VV12HH5VD2HHHH5",
                    "00000VDV2HH514514HH3VDV00000",
                    "00000VDVV1111111111VVDV00000",
                    "00000VDVV12HHPPHH31VVDV00000",
                    "HHHHH5D451VGGGGGGV145D4HHHHH",
                    "111111D111VGGGGGGV111D111111",
                    "HHHHH3D231VGGGGGGV123D2HHHHH",
                    "00000VDVV14HHHHHH51VVDV00000",
                    "00000VDVV1111111111VVDV00000",
                    "00000VDVV12HHHHHH31VVDV00000",
                    "2HHHH5D4514HH32HH5145D4HHHH3",
                    "VDDDDDDDDDDDDVVDDDDDDDDDDDDV",
                    "VD2HH3D2HHH3DVVD2HHH3D2HH3DV",
                    "VD4H3VD4HHH5D45D4HHH5DV2H5DV",
                    "VEDDVVDDDDDDD11DDDDDDDVVDDEV",
                    "4H3DVVD23D2HHHHHH3D23DVVD2H5",
                    "2H5D45DVVD4HH32HH5DVVD45D4H3",
                    "VDDDDDDVVDDDDVVDDDDVVDDDDDDV",
                    "VD2HHHH54HH3DVVD2HH54HHHH3DV",
                    "VD4HHHHHHHH5D45D4HHHHHHHH5DV",
                    "VDDDDDDDDDDDDDDDDDDDDDDDDDDV",
                    "4HHHHHHHHHHHHHHHHHHHHHHHHHH5"]

        # the legal space tile dict: key: tile location, value: Tile object
        self.legaltile = dict()
        # the dead space tile dict: key: tile location, value: Tile object
        self.deadtile = dict()
        # The space tile in the ghost house dict: key: tile location, value: Tile object
        self.ghosthousetile = dict()

        # Initialize the whole tile map
        for i in range(len(tilemap)):
            for j in range(len(tilemap[i])):
                # When the char in map is '1', 'D', 'E', the tile is a legal space tile
                if tilemap[i][j] == '1' or tilemap[i][j] == 'D' or tilemap[i][j] == 'E':
                    self.legaltile[(i,j)] = Tile(tilemap[i][j], (i,j), gameScreen)
                elif tilemap[i][j] == 'G' or tilemap[i][j] == 'P':
                    # The tile is in the ghost house, the ghost can only exit the tile
                    self.ghosthousetile[(i,j)] = Tile(tilemap[i][j], (i,j), gameScreen)
                else:
                    # The tile is a dead space tile
                    self.deadtile[(i,j)] = Tile(tilemap[i][j], (i,j), gameScreen)

        # The set containing legaltile location
        self.legaltileLoc = set(self.legaltile.keys())
