from Element import Element
from Case import Case
from CubeJaune import CubeJaune
from RectangleVert import RectangleLong
from RectangleBleu import RectangleHaut
from CubeRouge import CubeRouge
from colorama import Fore

class Map:
    def __init__(self, taille:tuple[int]=(5,4)) -> None:
        self.graph:list[list[Case]] = self.CreateMap(taille) # Utilisé pour stocker les données, peut eventuellement servir a l'UI
        self.InitialiseStartingMap()
        self.movesDone = []

    def CreateMap(self, taille):
        """
        returns a map populated with Case that are initialized with neighbours
        """

        rep:list[list[Case]] = [[Case((i, j)) for j in range(taille[1])] for i in range(taille[0])]

        for i in range(taille[0]):
            for j in range(taille[1]):
                # On va tester tous les cas limites où on fait un truc different, puis faire par defaut
                match ((i == 0, j == 0), (i == taille[0]-1, j==taille[1]-1)): # repere ou on est sur le cadre exterieur ((ligne 0, colonne 0), (ligne n, collonne n))
                    case ((True, True), (False, False)): # En haut a gauche
                        rep[i][j].SetEastNeighbour(rep[i][j+1])
                        rep[i][j].SetSouthNeighbour(rep[i+1][j])
                    case ((False, False), (True, True)): # En bas a droite
                        rep[i][j].SetWestNeighbour(rep[i][j-1])
                        rep[i][j].SetNorthNeighbour(rep[i-1][j])
                    case ((True, False), (False, True)): # En haut a droite
                        rep[i][j].SetWestNeighbour(rep[i][j-1])
                        rep[i][j].SetSouthNeighbour(rep[i+1][j])
                    case ((False, True), (True, False)): # En bas a gauche
                        rep[i][j].SetEastNeighbour(rep[i][j+1])
                        rep[i][j].SetNorthNeighbour(rep[i-1][j])
                    case ((True, False), (False, False)): # Ligne haute
                        rep[i][j].SetEastNeighbour(rep[i][j+1])
                        rep[i][j].SetSouthNeighbour(rep[i+1][j])
                        rep[i][j].SetWestNeighbour(rep[i][j-1])
                    case ((False, False), (True, False)): # Ligne basse
                        rep[i][j].SetNorthNeighbour(rep[i-1][j])
                        rep[i][j].SetWestNeighbour(rep[i][j-1])
                        rep[i][j].SetEastNeighbour(rep[i][j+1])
                    case ((False, True), (False, False)): # Colonne Gauche
                        rep[i][j].SetEastNeighbour(rep[i][j+1])
                        rep[i][j].SetSouthNeighbour(rep[i+1][j])
                        rep[i][j].SetNorthNeighbour(rep[i-1][j])
                    case ((False, False), (False, True)): # Colonne Droite
                        rep[i][j].SetWestNeighbour(rep[i][j-1])
                        rep[i][j].SetNorthNeighbour(rep[i-1][j])
                        rep[i][j].SetSouthNeighbour(rep[i+1][j])                    
                    case _: # Si on n'est pas un cas limite
                        rep[i][j].SetWestNeighbour(rep[i][j-1])
                        rep[i][j].SetNorthNeighbour(rep[i-1][j])
                        rep[i][j].SetSouthNeighbour(rep[i+1][j])                        
                        rep[i][j].SetEastNeighbour(rep[i][j+1])
        return rep
    
    def doLink(self, case:Case, element:Element):
            case.SetContent(element)
            element.AddPresence(case)
    
    def InitialiseStartingMap(self):
        """
        Size is 5x4 by default, this will init map for size = 5x4
        """
        
        # Initialises every piece.
        self.cubeJaunes = [CubeJaune(Fore.YELLOW) for _ in range(4)]
        self.rectangleLong = RectangleLong(Fore.GREEN)
        self.rectangleHauts = [RectangleHaut(Fore.BLUE) for _ in range(4)]
        self.cubeRouge = CubeRouge(Fore.RED)

        # Pose du carré rouge
        for i in [0,1]:
            for j in [1,2]:
                self.doLink(self.graph[i][j], self.cubeRouge)
        
        # Pose le rectangle long sous le carré rouge
        for i in [1,2]:
            self.doLink(self.graph[2][i], self.rectangleLong)
        
        # Pose les carrés jaunes        
        self.doLink(self.graph[4][0], self.cubeJaunes[0])
        self.doLink(self.graph[3][1], self.cubeJaunes[1])
        self.doLink(self.graph[3][2], self.cubeJaunes[2])
        self.doLink(self.graph[4][3], self.cubeJaunes[3])

        #Pose les rectangles Bleus hauts
        for i in range(2):
            self.doLink(self.graph[i][0], self.rectangleHauts[0])
        for i in range(2):
            self.doLink(self.graph[i+2][0], self.rectangleHauts[1])
        for i in range(2):
            self.doLink(self.graph[i][3], self.rectangleHauts[2])
        for i in range(2):
            self.doLink(self.graph[i+2][3], self.rectangleHauts[3])
        
    def GetContentInVertex(self, coo) -> Element:
        x, y = coo[0], coo[1]
        return self.graph[x][y].GetContent()

    def CheckMovePiece(self, origin:tuple[int, int], direction:str) -> tuple[bool, set[Case], Element]:
        """
        Pour Gerer le mouvement:
        On va prendre dans le graphe la case qui a ete selectionnée, ainsi que l'objet qui y est, et la dierction souhaitée.
        Ensuite on check pour tous les coté de l'objet les plus dans la direction (est, sud ...)  ( des rectangles donc plutot simple)
        si c'est tout vide, si c'est bon on deplace l'objet (on l'enleve des case a l'opposé de direction, et on on l'ajoute vers direction.)
        """
        if direction not in ["north", "east", "south", "west"]:
            raise ValueError(f"Direction is not valid, must be in {["north", "east", "south", "west"]}")

        # Initialisation des variables
        startX, startY = origin
        piece:Element = self.GetContentInVertex((startX, startY))
        if piece == None:
            return False

        # On cherche les cases de la piece dans la direction souhaitée
        toCheck:set[Case] = piece.GetPresence()
        #print(f"presence: {toCheck}")
        goodCases:set[Case] = set()
        def XCoo(element:Case):
            return element.GetCoo()[0]
        def YCoo(element:Case):
            return element.GetCoo()[1]        
        def DoTheMatchX(toCheck:set[Case], refCoo:int):
            return set([case_ for case_ in toCheck if case_.GetCoo()[0] == refCoo])
        def DoTheMatchY(toCheck:set[Case], refCoo:int):
            return set([case_ for case_ in toCheck if case_.GetCoo()[1] == refCoo])
        match direction:
            case "north":
                northCase = min(toCheck, key = XCoo)
                goodCases.update(DoTheMatchX(toCheck, northCase.GetCoo()[0]))
                elementToTest = goodCases.pop()
                if elementToTest.GetNorthNeighbour() == None:
                    return False, piece
            case "south":
                southCase:Case = max(toCheck, key=XCoo)
                goodCases.update(DoTheMatchX(toCheck, southCase.GetCoo()[0]))
                elementToTest = goodCases.pop()
                if elementToTest.GetSouthNeighbour() == None:
                    return False, piece
            case "east":
                eastCase = max(toCheck, key=YCoo)
                goodCases.update(DoTheMatchY(toCheck, eastCase.GetCoo()[1]))
                elementToTest = goodCases.pop()
                if elementToTest.GetEastNeighbour() == None:
                    return False, piece
            case "west":
                westCase = min(toCheck, key=YCoo)
                goodCases.update(DoTheMatchY(toCheck, westCase.GetCoo()[1]))
                elementToTest = goodCases.pop()
                if elementToTest.GetWestNeighbour() == None:
                    return False, piece
        
        goodCases.add(elementToTest)
        #print(f"goodCases : {goodCases}, {[element.GetCoo() for element in goodCases]}")
        match direction:            
            case "north":
                return not any([ not case.GetNorthNeighbour().GetContent() == None for case in goodCases ]), goodCases, piece
            case "south":
                return not any([ not case.GetSouthNeighbour().GetContent() == None for case in goodCases ]), goodCases, piece
            case "east":
                return not any([ not case.GetEastNeighbour().GetContent() == None for case in goodCases ]), goodCases, piece
            case "west":                
                return not any([ not case.GetWestNeighbour().GetContent() == None for case in goodCases ]), goodCases, piece

    def MovePiece(self, origin, direction):
        isMoving = self.CheckMovePiece(origin, direction) # Pas tres bonne pratique, is moving peut avoir des types
                                                        #   differents, mais il sera filtré donc technique de l'autruche.
        match isinstance(isMoving, bool):
            case True:
                if not isMoving: return False
            case False:
                if not isMoving[0]: return False
            case _:
                pass
        # a partir d'ici isMoving est un tuple[True, set, element]

        fromWhereToMove:set[Case] = isMoving[1] # On enleve le premier element, il sert plus a rien
        pieceToMove:Element = isMoving[2]
        whereHasMoved = set()
        toRemove = set.difference(pieceToMove.GetPresence(), fromWhereToMove)
        oldPresence = pieceToMove.GetPresence()

        # Pour le test pour savoir si on a affaire a un carré ou rectangle, savoir ce qu'on enleve des cases
        isSmall = False
        if len(pieceToMove.GetPresence()) == 1:
            isSmall = True

        match direction:
            case "north":
                for case in fromWhereToMove: # on rajoute le meme element a la case du dessus
                    case.GetNorthNeighbour().SetContent(pieceToMove)
                    self.doLink(case.GetNorthNeighbour(), pieceToMove)
                    whereHasMoved.add(case.GetNorthNeighbour())
            case "south":
                for case in fromWhereToMove: # on rajoute le meme element a la case du dessous
                    case.GetSouthNeighbour().SetContent(pieceToMove)
                    self.doLink(case.GetSouthNeighbour(), pieceToMove)
                    whereHasMoved.add(case.GetSouthNeighbour())
            case "east":
                for case in fromWhereToMove: # on rajoute le meme element a la case de droite
                    case.GetEastNeighbour().SetContent(pieceToMove)
                    self.doLink(case.GetEastNeighbour(), pieceToMove)
                    whereHasMoved.add(case.GetEastNeighbour())
            case "west":
                for case in fromWhereToMove: # on rajoute le meme element a la case de gauche
                    case.GetWestNeighbour().SetContent(pieceToMove)
                    self.doLink(case.GetWestNeighbour(), pieceToMove)
                    whereHasMoved.add(case.GetWestNeighbour())

        if isSmall: # Si on a un petit carré
            #print("small")
            oldCase = fromWhereToMove.pop()
            oldCase.SetContent(None)
            pieceToMove.RemovePresence(oldCase)
        else:
            #print("not small")
            for case in set.union(set.difference(pieceToMove.GetPresence(), set.union(fromWhereToMove, whereHasMoved)),
                                    toRemove,): # ATTENTION CA NE MARCHE QUE POUR DES BLOCS QUI NE DEPASSENT PAS UNE TAILLE DE 2
                case.SetContent(None)
                pieceToMove.RemovePresence(case)
        # Edge cases if we have a rectangle moving sideway
        if (isinstance(pieceToMove, RectangleHaut) and direction in {"east", "west"}) \
            or (isinstance(pieceToMove, RectangleLong) and direction in {"north", "south"}):
            #print("edge")
            for case in set.difference(oldPresence, whereHasMoved):
                case.SetContent(None)
                pieceToMove.RemovePresence(case)

        self.movesDone.append((origin, direction))
        return True # Si on est arrivé jusque la, c'est qu'on a reussi a bouget la piece

    def GetMovesDone(self):
        return self.movesDone

    def GetMap(self) -> list[Case]:
        return self.graph
    
    def GetYellowCubes(self):
        return self.cubeJaunes

    def CheckEnd(self):
        endingCases = set([self.graph[i][j] for j in [1,2] for i in [3,4]])
        return self.cubeRouge.GetPresence() == endingCases
    
    def __repr__(self) -> str:
        rep = ""
        for ligne in self.graph:
            for case in ligne:
                rep += str(case)
            rep += "\n"
        return rep
        
