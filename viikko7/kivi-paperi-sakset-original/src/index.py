from string import ascii_lowercase
from typing import Dict, Type
from kps_peli import KiviPaperiSakset
from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


Available_Games: Dict[str, Type[KiviPaperiSakset]] = {
    "Ihmistä vastaan": KPSPelaajaVsPelaaja,
    "Tekoälyä vastaan": KPSTekoaly,
    "Parannettua tekoälyä vastaan": KPSParempiTekoaly
}


def pick_game() -> KiviPaperiSakset | None:
    print("Valitse pelataanko")
    print("\n".join(map(lambda row: f" ({ascii_lowercase[row[0]]}) {row[1]}", enumerate(Available_Games.keys()))))
    print("Muilla valinnoilla lopetetaan")
    
    vastaus = input().strip() or "-"
    if vastaus not in ascii_lowercase: # No answer
        return None

    game_index = ascii_lowercase.index(vastaus)
    game_keys = list(Available_Games.keys())
    
    if len(game_keys) - 1 < game_index: # Invalid answer
        return None
    
    return Available_Games[game_keys[game_index]]() # Create game instance


def main():
    while True:
        peli = pick_game()
        if not peli:
            # Didn't pick a game
            break

        peli.pelaa() # Hangs until game over


if __name__ == "__main__":
    main()
