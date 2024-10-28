from queue import PriorityQueue
from copy import deepcopy
from Map import Map
from itertools import count
from CubeJaune import CubeJaune
from CubeRouge import CubeRouge

#For Typing
from Element import Element
from Case import Case

class AStar:
    def __init__(self, carte: Map):
        self.carte = carte
        self.openQueue = PriorityQueue()
        self.unique = count()  # Pour gérer l'ordre dans la file de priorité
        self.closedSet = set()

    def Heuristic_DistanceToExit(self, carte:Map):
        """
        Calcule la distance directe entre le cube rouge et la ligne de sortie.
        """
        redCube:Element = carte.cubeRouge
        redX, _ = max(redCube.GetPresence(), key=lambda case: case.GetCoo()[0]).GetCoo()
        return 4 - redX  # Nombre de lignes restant avant d'atteindre la ligne de sortie

    def Heuristic_Blockers(self, carte: Map):
        """
        Compte les pièces bloquant le chemin entre le cube rouge et la ligne de sortie.
        """
        blockers = 0
        redCube:Element = carte.cubeRouge
        _, redY = max(redCube.GetPresence(), key=lambda case: case.GetCoo()[1]).GetCoo()
        
        # Vérifie chaque case dans le chemin vertical du cube rouge vers la sortie
        for x in range(4, 5):  # Ligne de sortie
            if carte.GetMap()[x][redY] is not None and carte.GetMap()[x][redY] != redCube:
                blockers += 1
        return blockers
    
    def Heuristic_BlockingPieces(self, carte: Map):
        """
        Calcule les mouvements minimaux pour dégager les pièces bloquant le chemin du cube rouge.
        """
        red_cube = carte.cubeRouge
        _, red_y = max(red_cube.GetPresence(), key=lambda case: case.GetCoo()[1]).GetCoo()
        blocking_cost = 0

        for x in [3, 4]:
            piece = carte.GetMap()[x][red_y].GetContent()
            if piece and piece != red_cube:
                piece_positions = [case.GetCoo() for case in piece.GetPresence()]
                min_y = min(y for _, y in piece_positions)
                max_y = max(y for _, y in piece_positions)
                
                # Calcul de la distance de mouvement minimal pour dégager la voie
                distance_to_clear = min(abs(min_y - 0), abs(max_y - 3))
                blocking_cost += distance_to_clear  # Pénalisation des déplacements de blocage

        return blocking_cost
    
    def Heuristic_BlockingVertical(self, carte: Map):
        redCube: Element = carte.cubeRouge
        redX, redY = max(redCube.GetPresence(), key=lambda case: case.GetCoo()).GetCoo()
        blockers = 0
        
        for x in range(redX + 1, 5):
            piece = carte.GetMap()[x][redY]
            if piece and piece != redCube:
                blockers += 1
        return blockers

    def Heuristic_HorizontalProximity(self, carte: Map):
        """
        Encourage le déplacement des pièces qui se trouvent trop proches de la colonne de sortie du cube rouge.
        """
        red_cube = carte.cubeRouge
        _, red_y = max(red_cube.GetPresence(), key=lambda case: case.GetCoo()).GetCoo()
        horizontal_cost = 0

        for x in range(5):
            for y in [0, 3]:  # Vérifie seulement les colonnes externes par rapport à la cible
                piece = carte.GetMap()[x][y]
                if piece and piece != red_cube:
                    horizontal_cost += 1

        return horizontal_cost
    
    def Heuristic_YellowInPairs(self, carte:Map):
        yellowCubes:tuple[Element] = carte.GetYellowCubes()
        rep = 0

        # Ca peut paraitre beacoup de boucles mais on a 4 cubes, une case a chaque cube, et 8 voisins, donc 32 bouclages en tout, ca va.
        for cube in yellowCubes:
            for case in cube.GetPresence():
                hasNeighbour = False
                for voisin in {case.GetNorthNeighbour(), case.GetEastNeighbour(), 
                               case.GetSouthNeighbour(), case.GetWestNeighbour(),}:
                    if voisin and isinstance(voisin.GetContent(), CubeJaune):
                        hasNeighbour = True
                if not hasNeighbour:
                    rep += 1
        
        return rep
    
    def Heuristic_Side(self, carte: Map):
        """
        Heuristique qui mesure la distance du cube rouge au centre horizontal.
        """
        def yCoo(case: Case):
            return case.GetCoo()[1]
        maxCase: Case = max(carte.cubeRouge.GetPresence(), key=yCoo)
        return abs(2 - maxCase.GetCoo()[1])

    def GetHeuristics(self, carte: Map):
        """
        Combine les heuristiques pour une évaluation plus fiable.
        """
        return (100 * self.Heuristic_DistanceToExit(carte) # Critere principal, ne doit jamais augmenter
                + 1 * self.Heuristic_BlockingPieces(carte)
                + 1 * self.Heuristic_Blockers(carte)
                + 0.25 * self.Heuristic_Side(carte)
                + 0.5 * self.Heuristic_HorizontalProximity(carte)
                + 1 * self.Heuristic_BlockingVertical(carte)
                + 1 * self.Heuristic_YellowInPairs(carte)
                )

    def solve(self):
        """
        Implémente l'algorithme A* pour résoudre le jeu de l'âne rouge.
        """
        startState:tuple[float, int, tuple[int, Map]] = (self.GetHeuristics(self.carte), next(self.unique), (0, self.carte))
        self.openQueue.put(startState)

        while not self.openQueue.empty():
            currentMap:Map # Purement pour le typing
            gCost:int
            _, _, (gCost, currentMap) = self.openQueue.get()
            print(currentMap)

            # Vérifier l'état de fin
            if currentMap.CheckEnd():
                print("Solution trouvée !")
                print(currentMap)
                return currentMap, currentMap.GetMovesDone()

            self.closedSet.add(hash(str(currentMap)))  # Utilisation de hash pour optimiser l'ensemble des états explorés

            # Explorer tous les déplacements possibles
            for x in range(5):
                for y in range(4):
                    for direction in ["north", "south", "east", "west"]:
                        newMap:Map = self.clone_map(currentMap)
                        if newMap.MovePiece((x, y), direction):
                            newGCost = gCost + 1 if isinstance(newMap.GetContentInVertex((x,y)), CubeJaune) or isinstance(newMap.GetContentInVertex((x,y)), CubeRouge) else gCost + 2
                            heuristic = self.GetHeuristics(newMap)
                            print(heuristic)
                            newFCost = newGCost + heuristic

                            stateHash = hash(str(newMap))
                            if stateHash not in self.closedSet:
                                self.openQueue.put((newFCost, next(self.unique), (newGCost, newMap)))
                                self.closedSet.add(stateHash)

        # Ne devrai jamais arriver, mais on sait jamais
        print("Aucune solution trouvée.")
        return

    def clone_map(self, game_map: Map):
        """
        Copie l'état actuel de la carte.
        """
        return deepcopy(game_map)

if __name__ == "__main__":
    gameMap = Map()
    finalMap, solution = AStar(gameMap).solve()


    if solution:
        print(f"Solution finale, en {len(solution)} coups :")
        showcaseMap = Map()
        print(showcaseMap)
        for action in solution:
            showcaseMap.MovePiece(*action)
            print(showcaseMap)

