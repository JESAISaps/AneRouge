# Typing
from Map import Map
from Case import Case
from Element import Element
from CubeJaune import CubeJaune
from math import sqrt
from copy import deepcopy

class Heuristics:
    def __init__(self):
        pass

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
        """
        returns numbers of blocking peices directly underneath red cube
        """
        redCube: Element = carte.cubeRouge
        redX, redY = max(redCube.GetPresence(), key=lambda case: case.GetCoo()).GetCoo()
        if redX == 4:
            return 0
        
        #for x in range(redX + 1, 5):
        #    piece = carte.GetMap()[x][redY]
        #    if piece and piece != redCube:
        #        blockers += 1
        rep = 0
        for y in [redY-1, redY]:
            piece = carte.GetMap()[redX+1][y]
            if piece and piece != redCube:
                rep += 1

        return rep

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
    
    def Heuristic_MustMove(self, carte:Map):
        """
        Heuristique qui verifie si le cube a bougé
        """
        cubeRouge = carte.cubeRouge
        coo = max(cubeRouge.GetPresence(), key=lambda case: sum(case.GetCoo())).GetCoo()

        return 5 - self.distance(coo, (1,2))
    
    def Heuristic_LongMonte(self, carte:Map):
        rectangleLong = carte.rectangleLong
        return deepcopy(rectangleLong.GetPresence()).pop().GetCoo()[0]-1

    def Heuristic_CloseHoles(self, carte:Map):
        voids:set[Case] = set()
        for void in carte.GetVoids():
            voids.update(void.GetPresence())
        return self.distance(voids.pop().GetCoo(), voids.pop().GetCoo()) - 1
    
    def Heuristic_CotesOpposes(self, carte:Map):
        """
        le carré rouge et vert doivent etre sur des cotes opposes
        """
        rouge = carte.cubeRouge
        vert = carte.rectangleLong
        _, yRCoo = max(rouge.GetPresence(), key=lambda case: case.GetCoo()[1]).GetCoo()
        _, yVCoo = max(vert.GetPresence(), key=lambda case: case.GetCoo()[1]).GetCoo()
        return 2 - abs(yRCoo - yVCoo)


    def distance(self, p0, p1):
        return abs((p0[0] - p1[0]) + (p0[1] - p1[1]))
    
    def GetHeuristics(self, carte: Map):
        """
        Combine les heuristiques pour une évaluation plus fiable.
        """
        return (3 * self.Heuristic_DistanceToExit(carte) +
                4 * self.Heuristic_MustMove(carte) +
                1 * self.Heuristic_CloseHoles(carte) +
                0.5 * self.Heuristic_CotesOpposes(carte) +
                1 * self.Heuristic_LongMonte(carte) + 
                0.75 * self.Heuristic_YellowInPairs(carte) + 

                1 * self.Heuristic_BlockingVertical(carte))

