from queue import PriorityQueue
from copy import deepcopy
from Map import Map
from itertools import count
from CubeJaune import CubeJaune
from CubeRouge import CubeRouge
from Heuristics import Heuristics

#For Typing
from Element import Element
from Case import Case

class AStar:
    def __init__(self, carte: Map, heuristicsFunction):
        self.carte = carte
        self.openQueue = PriorityQueue()
        self.unique = count()  # Pour gérer l'ordre dans la file de priorité
        self.closedSet = set()
        self.heuristicsFunction = heuristicsFunction

        #pour les affichages periodiques
        self.compteur = count()

    def solve(self):
        """
        Implémente l'algorithme A* pour résoudre le jeu de l'âne rouge.
        """
        startState:tuple[float, int, tuple[int, Map]] = (self.heuristicsFunction(self.carte), next(self.unique), (0, self.carte))
        self.openQueue.put(startState)

        while not self.openQueue.empty():
            currentMap:Map # Purement pour le typing
            gCost:int
            fCost, _, (gCost, currentMap) = self.openQueue.get()
            if next(self.compteur) % 100 == 0:
                print(f"\n\nCurrent State: \n{currentMap}")
                #print(f"Map total cost: {fCost}\nMap heuristic: {self.heuristicsFunction(currentMap)}")
                print(f"Len of closed set: {len(self.closedSet)}")
                print(f"Len of open set: {self.openQueue.qsize()}")

            # Vérifier l'état de fin
            if currentMap.CheckEnd():
                print("Solution trouvée !")
                print(currentMap)
                return currentMap, currentMap.GetMovesDone()

            self.closedSet.add(hash(str(currentMap)))  # Utilisation d'un hash pour optimiser l'ensemble des états explorés

            holes = set()
            for ligne in currentMap.GetMap():
                for case in ligne:
                    if case.GetContent() == None:
                        holes.add(case)
            
            toExplore = [case.GetCoo() for case in holes]

            # Explorer tous les déplacements possibles
            for holeCoo in toExplore:
                for x in range(holeCoo[0]-1, holeCoo[0] +2):
                    for y in range(holeCoo[1]-1, holeCoo[1] +2):
                            for direction in ["north", "south", "east", "west"]:
                            
                            
                                newMap:Map = self.CloneMap(currentMap)
                                if x <= 4 and y<= 3 and newMap.MovePiece((x, y), direction):
                                    stateHash = hash(str(newMap))
                                    if stateHash not in self.closedSet:
                                        newGCost = gCost + 1
                                        heuristic = self.heuristicsFunction(newMap)
                                        newFCost = newGCost + heuristic

                                        self.openQueue.put((newFCost, next(self.unique), (newGCost, newMap)))
                                        self.closedSet.add(stateHash)

        # Ne devrai jamais arriver, mais on sait jamais
        print("Aucune solution trouvée.")
        return

    def CloneMap(self, game_map: Map):
        """
        Copie l'état actuel de la carte.
        """
        return deepcopy(game_map)

if __name__ == "__main__":
    gameMap = Map()
    heuristic = Heuristics()
    finalMap, solution = AStar(gameMap, heuristic.GetHeuristics).solve()


    if solution:
        print(f"Solution finale, en {len(solution)} coups :")
        showcaseMap = Map()
        print(showcaseMap)
        for action in solution:
            showcaseMap.MovePiece(*action)
            print(showcaseMap)

