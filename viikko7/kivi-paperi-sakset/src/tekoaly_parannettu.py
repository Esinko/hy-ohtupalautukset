from tekoaly_base import TekoalyBase
from kps_peli import Game_Move_Type

# "Muistava tekoäly"
class TekoalyParannettu(TekoalyBase):
    def aseta_siirto(self, siirto: Game_Move_Type):
        self._add_player_move_to_memory(siirto)

    def anna_siirto(self):
        viimeisin_siirto = self._get_last_player_move()
        if viimeisin_siirto is None:
            return "k"

        move_counts = self._get_player_move_counts()

        # Tehdään siirron valinta esimerkiksi seuraavasti;
        # - jos kiviä eniten, annetaan aina paperi
        # - jos papereita eniten, annetaan aina sakset
        # muulloin annetaan aina kivi
        if move_counts["k"] > move_counts["p"] or move_counts["k"] > move_counts["s"]:
            return "p"
        elif move_counts["p"] > move_counts["k"] or move_counts["p"] > move_counts["s"]:
            return "s"
        else:
            return "k"

        # Tehokkaampiakin tapoja löytyy, mutta niistä lisää
        # Johdatus Tekoälyyn kurssilla!
