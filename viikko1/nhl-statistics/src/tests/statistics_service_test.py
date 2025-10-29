import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub() # type: ignore
        )

    def test_get_empty(self):
        self.assertEqual(len(self.stats.top(-1)), 0)

    def test_search_empty(self):
        self.assertEqual(self.stats.search("foobar"), None)
    
    def test_search(self):
        self.assertEqual(str(self.stats.search("Semenko")), str(PlayerReaderStub().get_players()[0]))

    def test_team_list(self):
        self.assertEqual(len(self.stats.team("EDM")), 3)
        for player in self.stats.team("EDM"):
            self.assertEqual(player.team, "EDM")
    
    def test_top_limit(self):
        self.assertEqual(len(self.stats.top(2)), 3)