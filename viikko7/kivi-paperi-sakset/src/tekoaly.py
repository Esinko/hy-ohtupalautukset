from tekoaly_base import TekoalyBase
from kps_peli import Game_Moves

class Tekoaly(TekoalyBase):
    def __init__(self):
        # Stub to initialize a non-remembering, deterministic model
        self._counter = 0

    def anna_siirto(self):
        self._counter += 1
        siirto = self._counter % 3
        return Game_Moves[siirto]

    def aseta_siirto(self, siirto):
        # ei tehdä mitään
        pass
