from colorama import Fore

class Element:
    def __init__(self, color=None) -> None:
        self.presence:set = set()
        self.color:str = color

    def GetPresence(self) -> set:
        return self.presence
    
    def AddPresence(self, case):
        self.presence.add(case)
    
    def RemovePresence(self, case):
        if case in self.GetPresence():
            self.presence.remove(case)
        else:
            raise UserWarning(f"Tried to remove case {case} from {self}, bot {case} was not in {self.GetPresence()}")

    def __repr__(self) -> str:
        if self.color != None:
            return self.color + "▮" + Fore.WHITE
        else:
            return "▮"