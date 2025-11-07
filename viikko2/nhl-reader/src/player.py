from typing import List
from requests import get

class Player:
    def __init__(self, dict):
        self.name = dict["name"]
        self.nationality = str(dict["nationality"]).upper()
        self.assists = dict["assists"]
        self.goals = dict["goals"]
        self.games = dict["games"]
        self.team = dict["team"]
    
    def __str__(self):
        return f"{self.name:20} {self.team:20} {self.goals:2} + {self.assists:2} = {self.goals + self.assists}"

class PlayerReader:
    def __init__(self, url: str) -> None:
        self.url = url
    
    def get(self) -> List[Player]:
        response = get(self.url).json()
        return [Player(player_dict) for player_dict in response]
    
class PlayerStats:
    def __init__(self, reader: PlayerReader) -> None:
        self.player_reader = reader

    def top_scorers_by_nationality(self, nationality: str) -> List[Player]:
        return [player for player in self.player_reader.get() if player.nationality == nationality]
    
    def get_available_seasons(self) -> List[str]:
        return ["2018-19", "2019-20", "2020-21", "2021-22", "2022-23", "2023-24", "2024-25", "2025-26"]
    
    def get_available_nationalities(self) -> List[str]:
        return list(set([player.nationality for player in self.player_reader.get()]))