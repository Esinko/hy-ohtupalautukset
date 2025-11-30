from dataclasses import dataclass
from typing import Literal, Dict, TypeAlias
from random import randint

TennisPlayerId: TypeAlias = int
TennisScore: TypeAlias = str

@dataclass
class TennisPlayer:
    id: TennisPlayerId
    name: str

tennis_score_to_text = {
    0: "Love",
    1: "Fifteen",
    2: "Thirty",
    3: "Forty"
}

tennis_minimum_points_to_win = 4
tennis_lead_to_win = 2

class TennisGame:
    players: Dict[TennisPlayerId, TennisPlayer]
    scores: Dict[TennisPlayerId, int]
    state: Literal["setup", "on-going", "concluded"]
    winner: TennisPlayer | None

    def __init__(self, player1_name: str, player2_name: str):
        self.players = {}
        self.scores = {}
        self.winner = None
        self.state = "setup"

        # NOTE: We specifically support a 2 player game for now (no teams)
        player_names = [player1_name, player2_name]
        for player_name in player_names:
            self.add_player(player_name)

        self.state = "on-going"


    def add_player(self, player_name: str):
        if self.state != "setup":
            raise Exception("Game not in setup state.")
        
        if len(self.players.keys()) == 2:
            raise Exception("Game is full.")
        
        new_player_id = randint(1, 100000)
        while new_player_id in self.players: # Ensure unique ids
            new_player_id = randint(1, 100000)

        self.players[new_player_id] = TennisPlayer(id=new_player_id,
                                                   name=player_name)
        self.scores[new_player_id] = 0
    

    def get_player_by_id(self, player_id: int) -> TennisPlayer | None:
        return self.players.get(player_id)


    def get_player_by_name(self, player_name: str) -> TennisPlayer | None:
        for player_id in self.players:
            if self.players[player_id].name == player_name:
                return self.players[player_id]
            
        return None


    def won_point(self, player_name: str):
        if self.state != "on-going":
            raise Exception("Game not on-going.")

        player = self.get_player_by_name(player_name)
        if player is None:
            raise Exception("Player not found.")
        
        self.scores[player.id] += 1
        if self.scores[player.id] >= tennis_minimum_points_to_win:
            self._check_for_winner()


    def _check_for_winner(self):
        # NOTE: Scrap for team support
        all_scores = [self.scores[player_id] for player_id in self.scores]
        smallest_score = min(all_scores)

        for player_id in self.players:
            player_score = self.scores[player_id]
            if player_score - smallest_score >= tennis_lead_to_win:
                self.state = "concluded"
                self.winner = self.players[player_id]
                break


    def get_score(self) -> TennisScore:
        # See _check_for_winner() for more info
        if self.state == "concluded":
            return f"Win for {self.winner.name}"

        all_scores = [self.scores[player_id] for player_id in self.scores]
        unique_scores = set(self.scores[player_id] for player_id in self.scores)
        highest_score = max(all_scores)

        # When all scores match, simplify
        if len(unique_scores) == 1:
            if all_scores[0] > 2:
                return "Deuce"
            
            return f"{tennis_score_to_text[all_scores[0]]}-All"
        
        # When advantage
        if highest_score >= tennis_minimum_points_to_win:
            # NOTE: Scrap for team support
            for player_id in self.players:
                player_score = self.scores[player_id]
                if player_score == highest_score:
                    return f"Advantage {self.players[player_id].name}"
            
        # Regular score text
        score = ""
        for player_id in self.players:
            player_score = self.scores[player_id]
            score += f"{"-" if len(score) != 0 else ""}{tennis_score_to_text[player_score]}"

        return score
