from player import PlayerReader, PlayerStats
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console

console = Console()

def main():
    url = "https://studies.cs.helsinki.fi/nhlstats/2024-25/players"
    reader = PlayerReader(url)
    stats = PlayerStats(reader)

    # Which year?
    print("Fetch NHL Player statistics. Choose filters.")
    season = Prompt.ask("Season", choices=stats.get_available_seasons(), default="2024-25")

    while True:
        nationality = Prompt.ask("Nationality", choices=stats.get_available_nationalities(), default="")
        if len(nationality) == 0: continue

        players = stats.top_scorers_by_nationality(nationality.upper())

        table = Table(show_header=True, header_style="bold white", title=f"Season {season} players from {nationality}")

        table.add_column("Released", style="cyan", justify="left")
        table.add_column("teams", style="magenta", justify="center")
        table.add_column("goals", style="green", justify="center")
        table.add_column("assists", style="green", justify="center")
        table.add_column("points", style="green", justify="center")

        for player in players:
            table.add_row(player.name, player.team, str(player.goals), str(player.assists), str(player.goals + player.assists))

        console.print(table)

if __name__ == "__main__":
    main()
