from stats import Statistics
from player_reader import PlayerReader
from matchers import And, HasAtLeast, PlaysIn, Not, HasFewerThan, All, Or

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players.txt"
    reader = PlayerReader(url)
    stats = Statistics(reader)

    #matcher = And(
    #    HasAtLeast(5, "goals"),
    #    HasAtLeast(20, "assists"),
    #    PlaysIn("PHI")
    #)
    #matcher = And(
    #    HasFewerThan(2, "goals"),
    #    PlaysIn("NYR")
    #)
    #matcher = Or(
    #    HasAtLeast(45, "goals"),
    #    HasAtLeast(70, "assists")
    #)
    matcher = And(
        HasAtLeast(70, "points"),
        Or(
            PlaysIn("COL"),
            PlaysIn("FLA"),
            PlaysIn("BOS")
        )
    )

    for player in stats.matches(matcher):
        print(player)


if __name__ == "__main__":
    main()
