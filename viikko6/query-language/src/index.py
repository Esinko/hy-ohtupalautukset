from stats import Statistics
from player_reader import PlayerReader
from builder import QueryBuilder

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
    #matcher = And(
    #    HasAtLeast(70, "points"),
    #    Or(
    #        PlaysIn("COL"),
    #        PlaysIn("FLA"),
    #        PlaysIn("BOS")
    #    )
    #)

    query = QueryBuilder()
    matcher = (
        query
        .plays_in("NYR")
        .has_at_least(10, "goals")
        .has_fewer_than(20, "goals")
        .build()
    )

    for player in stats.matches(matcher):
        print(player)


if __name__ == "__main__":
    main()
