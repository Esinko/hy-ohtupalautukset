from abc import abstractmethod
from typing import Any, Dict, List
from kps_peli import Game_Move_Type, Game_Moves

class MoveBuffer:
    def __init__(self, size: int):
        self.size = size
        self.buffer = [None] * size
        self.index = 0
        self.count = 0

    def insert(self, value: Game_Move_Type):
        self.buffer[self.index] = value
        self.index = (self.index + 1) % self.size
        self.count = min(self.count + 1, self.size)

    def get_move_counts(self) -> Dict[Game_Move_Type, int]:
        return { move: len(list(filter(lambda m: m == move, self.buffer))) for move in Game_Moves }

    def last(self) -> Game_Move_Type | None:
        if self.count == 0:
            return None
        return self.buffer[(self.index - 1) % self.size]

class TekoalyBase:
    def __init__(self, muistin_koko: int = 0):
        self._muisti = MoveBuffer(muistin_koko)

    def _add_player_move_to_memory(self, value: Game_Move_Type):
        self._muisti.insert(value)

    def _get_last_player_move(self) -> Game_Move_Type:
        return self._muisti.last()
    
    def _get_player_move_counts(self):
        return self._muisti.get_move_counts()

    @abstractmethod
    def aseta_siirto(self, siirto: Game_Move_Type):
        pass
    
    @abstractmethod
    def anna_siirto(self) -> Game_Move_Type:
        pass