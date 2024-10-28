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

    def solve(self):
        """
        Implémente l'algorithme A* pour résoudre le jeu de l'âne rouge.
        """
        startState:tuple[float, int, tuple[int, Map]] = (self.heuristicsFunction(self.carte), next(self.unique), (0, self.carte))
        self.openQueue.put(startState)

        while not self.openQueue.empty():
            currentMap:Map # Purement pour le typing
            gCost:int
            _, _, (gCost, currentMap) = self.openQueue.get()
            print(currentMap, self.heuristicsFunction(currentMap))

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
                            heuristic = self.heuristicsFunction(newMap)
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
    heuristic = Heuristics()
    finalMap, solution = AStar(gameMap, heuristic.GetHeuristics).solve()


    if solution:
        print(f"Solution finale, en {len(solution)} coups :")
        showcaseMap = Map()
        print(showcaseMap)
        for action in solution:
            showcaseMap.MovePiece(*action)
            print(showcaseMap)

