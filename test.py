from queue import PriorityQueue, Queue
from copy import deepcopy
from Map import Map
from itertools import count
# Typing
from Case import Case

class AStar:
    def __init__(self, carte: Map):
        self.carte = carte
        self.openQueue = PriorityQueue() # Queue qui ne fonctionne pas avec l'ordre d'arrivé, mais de priorité
        self.unique = count() # Pour diferencier les elements de la prioriryqueue, sinon elle va essayer de comparer des Map
        self.closedSet = set()
    
    def Heuristic_High(self, carte:Map):
        """
        Returns distance from finish depending on how low is the red cube.
        """
        def xCoo(case:Case):
            return case.GetCoo()[0]
        maxCase:Case = max(carte.cubeRouge.GetPresence(), key=xCoo)
        return 4 - maxCase.GetCoo()[0]

    def Heuristic_Side(self, carte:Map):
        """
        Returns distance from finish depending on how far away from center is the red cube.
        Based on the right side, so we will instincivelly get on the right side of the map to reduce this heurisitic
        """
        def yCoo(case:Case):
            return case.GetCoo()[1]
        maxCase:Case = max(carte.cubeRouge.GetPresence(), key=yCoo)
        return abs(2-maxCase.GetCoo()[1])

    def GetHeuristics(self, carte:Map):
        """
        Mixes different heuristic functions to get a solid one.
        """
        return self.Heuristic_High(carte)
    
    def solve(self):
        """
        Implémente l'algorithme A* pour résoudre le jeu.
        """
        # Ajouter l'état initial dans l'open set
        startState:tuple[int, int, tuple[int, Map]] = (self.GetHeuristics(self.carte), next(self.unique), (0,  self.carte))
        self.openQueue.put(startState)

        # Boucle A*
        while self.openQueue.qsize() != 0:
            currentMap:Map # Purement pour le typing
            gCost:int
            _, _, (gCost, currentMap) = self.openQueue.get()
            print(currentMap)
            
            # Vérifier si l'état est final
            if currentMap.CheckEnd():
                print("Solution trouvée!")
                print(currentMap)
                return currentMap

            # Marquer cet état comme exploré
            self.closedSet.add(str(currentMap))  # Utilise la chaine associée pour eviter les doublons doublons
            
            # Explorer tous les déplacements possibles
            for x in range(5):
                for y in range(4):
                    for direction in ["north", "south", "east", "west"]:
                        newMap:Map = self.clone_map(currentMap)
                        if newMap.MovePiece((x, y), direction):  # Si le mouvement est valide
                            # Calcule le cout du chemin g et le cout estimé f = g + heuristic
                            newGCost = gCost + 1
                            newFCost = newGCost + self.GetHeuristics(newMap)
                            
                            # Vérifier si cet état a déjà été exploré
                            stateStr = str(newMap)
                            if stateStr not in self.closedSet:
                                self.openQueue.put((newFCost, next(self.unique), (newGCost, newMap)))
                                self.closedSet.add(stateStr)

        # Ne devrai jamais arriver, mais on sait jamais
        print("Aucune solution trouvée.")
        return

    def clone_map(self, game_map):
        """
        Crée une copie de l'état actuel de la carte pour éviter des modifications non voulues.
        """
        return deepcopy(game_map)

if __name__ == "__main__":
    # Initialiser la carte de départ
    gameMap = Map()
    
    # Instancie le solveur A* et résoud
    solution = AStar(gameMap).solve()

    if solution:
        print("Voici la solution finale :")
        print(solution)
