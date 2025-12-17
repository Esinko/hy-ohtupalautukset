from kps_peli import KiviPaperiSakset
from tekoaly_parannettu import TekoalyParannettu


class KPSParempiTekoaly(KiviPaperiSakset):
    def pelaa(self):
        tekoaly = TekoalyParannettu(10)

        while True:
            ekan_siirto = self.prompt_for_move(0)
            if ekan_siirto is None:
                break

            tokan_siirto = tekoaly.anna_siirto()

            print(f"Tietokone valitsi: {tokan_siirto}")
            tekoaly.aseta_siirto(ekan_siirto)

            self.record_moves(ekan_siirto, tokan_siirto)
            print(self.get_score())

        print("Kiitos!")
        print(self.get_score())
