from queue import PriorityQueue
from copy import deepcopy
from Map import Map
from itertools import count
from CubeJaune import CubeJaune
from CubeRouge import CubeRouge
from Heuristics import Heuristics
from time import time

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
                print(f"Map total cost: {fCost}\nMap heuristic: {self.heuristicsFunction(currentMap)}")
                print(f"Len of closed set: {len(self.closedSet)}")
                print(f"Len of open set: {self.openQueue.qsize()}")

            # Vérifier l'état de fin
            if currentMap.CheckEnd():
                print("Solution trouvée !")
                print(currentMap)
                return currentMap, currentMap.GetMovesDone()

            self.closedSet.add(hash(str(currentMap)))  # Utilisation d'un hash pour optimiser l'ensemble des états explorés

            holes:set[Case] = set()
            for void in currentMap.GetVoids():
                holes.update(void.GetPresence())
            
            toExplore = [case.GetCoo() for case in holes]

            # Explorer tous les déplacements possibles
            for holeCoo in toExplore:
                hX, hY = holeCoo
                for x , y, direction in [(hX-1, hY, "south"), (hX, hY + 1, "west"), (hX + 1, hY, "north"), (hX, hY - 1, "east")]:
                    
                    newMap:Map = self.CloneMap(currentMap)
                    if 0 <= x <= 4 and 0 <= y <= 3 and newMap.MovePiece((x, y), direction):
                        stateHash = hash(str(newMap))
                        if stateHash not in self.closedSet:
                            newGCost = gCost + 1
                            heuristic = self.heuristicsFunction(newMap)
                            newFCost = newGCost + heuristic
                            self.openQueue.put((newFCost, next(self.unique), (newGCost, newMap)))
                            self.closedSet.add(stateHash)

        # Ne devrai jamais arriver, mais on sait jamais
        print("Aucune solution trouvée.")
        return currentMap, False

    def CloneMap(self, game_map: Map):
        """
        Copie l'état actuel de la carte.
        """
        return deepcopy(game_map)

if __name__ == "__main__":
    gameMap = Map()
    heuristic = Heuristics()
    startTime = time()
    finalMap, solution = AStar(gameMap, heuristic.GetHeuristics).solve()
    stopTime = time()


    if solution:
        print(f"Solution finale, en {len(solution)} coups :")
        showcaseMap = Map()
        print(showcaseMap)
        for action in solution:
            showcaseMap.MovePiece(*action)
            print(showcaseMap)

        print(f"Solution Found in {stopTime - startTime} seconds, in {int(len(solution))} moves.")

