from abc import abstractmethod
from typing import Literal

Game_Moves = ["k", "p", "s"]
Game_Move_Type = Literal["k", "p", "s"]
Winning_Combos = {
    # Winning move -> Losing move (for the winning move)
    "k": "s",
    "s": "p",
    "p": "k"
}

class KiviPaperiSakset:
    player1_points: int
    player2_points: int
    tie_count: int

    def __init__(self):
        self.player1_points = 0
        self.player2_points = 0
        self.tie_count = 0


    def _game_tick(self, player1_move: Game_Move_Type, player2_move: Game_Move_Type):
        # Record tie
        if player1_move == player2_move:
            self.tie_count += 1
            return

        # Check both players for winning moves
        for winning_move in Winning_Combos.keys():
            losing_move = Winning_Combos[winning_move]
            if player1_move == winning_move and player2_move == losing_move:
                self.player1_points += 1
                break
            elif player2_move == winning_move and player1_move == losing_move:
                self.player2_points += 1
                break


    def get_score(self) -> str:
        return f"Pelitilanne: {self.player1_points} - {self.player2_points}\nTasapelit: {self.tie_count}" 


    def prompt_for_move(self, player: int = 0) -> Game_Move_Type | None:
        messages = {
            0: "Ensimmäisen pelaajan siirto: ",
            1: "Toisen pelaajan siirto: "
        }

        move = input(messages[player]) or "-"

        return move if move in Game_Moves else None


    def record_moves(self, player1_move: Game_Move_Type, player2_move: Game_Move_Type):
        self._game_tick(player1_move, player2_move)
        

    @abstractmethod
    def pelaa():
        pass    

