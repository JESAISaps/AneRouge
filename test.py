from Map import Map
from Case import Case

if __name__ == "__main__":
    carte = Map()
    print(carte)
    
    carte.MovePiece((3,1), "south")
    print(carte)
    carte.MovePiece((3,2), "south")
    print(carte)
    carte.MovePiece((2,1), "south")
    print(carte)
    carte.MovePiece((0,2), "south")
    print(carte)
    carte.MovePiece((0,0), "east")
    print(carte)