from kps_peli import KiviPaperiSakset


class KPSPelaajaVsPelaaja(KiviPaperiSakset):
    def pelaa(self):
        while True:
            ekan_siirto = self.prompt_for_move(0)
            if ekan_siirto is None:
                break

            tokan_siirto = self.prompt_for_move(1)
            if tokan_siirto is None:
                break

            self.record_moves(ekan_siirto, tokan_siirto)
            print(self.get_score())

        print("Kiitos!")
        print(self.get_score())

