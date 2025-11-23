import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        viitegeneraattori_mock.uusi.return_value = 42

        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 25
            if tuote_id == 3:
                return 0


        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "keksi", 1)
            if tuote_id == 3:
                return Tuote(3, "kakku", 18)
        

        varasto_mock = Mock()
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)
        self.kauppa = kauppa
        self.pankki_mock = pankki_mock
        self.viitegeneraattori_mock = viitegeneraattori_mock
        self.varasto_mock = varasto_mock

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called()

    def test_kutsutaan_tilimaksu_oikeilla_tiedoilla(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", self.kauppa._kaupan_tili, 5)

    def test_kutsutaan_tilimaksu_oikeilla_tiedoilla_kahdelle_eri_tuotteelle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", self.kauppa._kaupan_tili, 6)

    def test_kutsutaan_tilimaksu_oikeilla_tiedoilla_kahdelle_samalle_tuotteelle(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", self.kauppa._kaupan_tili, 10)

    def test_kutsutaan_tilimaksu_oikeilla_tiedoilla_kahdelle_joista_yksi_loppu(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", self.kauppa._kaupan_tili, 5)

    def test_aloita_asiointi_nollaa(self):
        ostoskori_mock = Mock()
        self.kauppa._ostoskori = ostoskori_mock
        self.kauppa.aloita_asiointi()
        ostoskori_mock.assert_not_called()

    def test_kauppa_pyytaa_aina_viitenumeron(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.viitegeneraattori_mock.uusi.assert_called()
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")
        self.viitegeneraattori_mock.uusi.assert_called()

    def test_poista_kortista_poistaa(self):
        ostoskori_mock = Mock()
        maito = Tuote(1, "maito", 5)
        self.kauppa.aloita_asiointi()
        self.kauppa._ostoskori = ostoskori_mock
        self.kauppa.lisaa_koriin(1)
        self.kauppa.poista_korista(1)
        self.varasto_mock.palauta_varastoon.assert_called_with(maito)
        ostoskori_mock.poista.assert_called_with(maito)