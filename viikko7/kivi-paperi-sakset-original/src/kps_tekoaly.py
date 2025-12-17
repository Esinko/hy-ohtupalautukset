from kps_peli import KiviPaperiSakset
from tekoaly import Tekoaly


class KPSTekoaly(KiviPaperiSakset):
    def pelaa(self):
        tekoaly = Tekoaly()

        while True:
            ekan_siirto = self.prompt_for_move(0)
            if ekan_siirto is None:
                break

            tokan_siirto = tekoaly.anna_siirto()
            print(f"Tietokone valitsi: {tokan_siirto}")
            
            self.record_moves(ekan_siirto, tokan_siirto)
            print(self.get_score())

        print("Kiitos!")
        print(self.get_score())
