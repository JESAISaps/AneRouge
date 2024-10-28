from typing import Self

class Case:
    def __init__(self, coo:tuple, voisinNord=None, voisinEst=None, voisinSud=None, voisinOuest=None) -> None:
        """
        Noeud du graph.
        """
        self.x, self.y = coo # En x la ligne et y la colonne
        self._vNord = voisinNord
        self._vEst = voisinEst
        self._vSud = voisinSud
        self._vOuest = voisinOuest
        self._content = None
    
    def GetNorthNeighbour(self) -> Self:
        return self._vNord
    def GetEastNeighbour(self) -> Self:
        return self._vEst
    def GetSouthNeighbour(self) -> Self:
        return self._vSud
    def GetWestNeighbour(self) -> Self:
        return self._vOuest
    
    def SetNorthNeighbour(self, neighbour):
        self._vNord = neighbour
    def SetEastNeighbour(self, neighbour):
        self._vEst = neighbour
    def SetSouthNeighbour(self, neighbour):
        self._vSud = neighbour
    def SetWestNeighbour(self, neighbour):
        self._vOuest = neighbour

    def SetContent(self, content):
        self._content = content
    
    def GetContent(self):
        return self._content
    
    def GetCoo(self):
        return self.x, self.y

    def __repr__(self) -> str:
        # Temporaire, peut etre qu'on garde, peut etre pas
        if self.GetContent() != None:
            return f"{str(self.GetContent())}"
        else:
            return " "