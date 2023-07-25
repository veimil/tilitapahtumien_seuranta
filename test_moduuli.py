import unittest
from virheellinen_csv_error import VirheellinenCSVError
from csv_lukija import CsvLukija
from sovellus import Sovellus
from oma_kategoria import OmaKategoria
from tilitapahtumat import Tilitapahtumat
from veloitus import Veloitus
from hyvitys import Hyvitys


class TestCSVLukija(unittest.TestCase):

    def test_with_tiedosto_ok(self):
        with open('testifile.txt', 'w') as testi_tiedosto:
            testi_tiedosto.write('tyyppi(veloitus tai hyvitys),timestamp,kauppa,summa\n')
            testi_tiedosto.write('veloitus,2023-04-05 15:26:27.392461,Alepa Otaniemi,20\n')
            testi_tiedosto.write('hyvitys,2023-04-05 19:26:27.392461,Alepa Otaniemi,10')
        testi_sovellus = Sovellus()
        testi_csvlukija = CsvLukija('testifile.txt', testi_sovellus)

        self.assertEqual(testi_csvlukija.lue_tiedosto(), 'Tiedosto luettu.')

    def test_virheellinen_transaktiotyyppi(self):
        with open('testifile.txt', 'w') as testi_tiedosto:
            testi_tiedosto.write('tyyppi(veloitus tai hyvitys),timestamp,kauppa,summa\n')
            testi_tiedosto.write('maksu,2023-04-05 15:26:27.392461,Alepa Otaniemi,20')
        testi_sovellus = Sovellus()
        testi_csvlukija = CsvLukija('testifile.txt', testi_sovellus)

        with self.assertRaises(VirheellinenCSVError):
            testi_csvlukija.lue_tiedosto()

    def test_virheellinen_summa(self):
        with open('testifile.txt', 'w') as testi_tiedosto:
            testi_tiedosto.write('tyyppi(veloitus tai hyvitys),timestamp,kauppa,summa\n')
            testi_tiedosto.write('veloitus,2023-04-05 15:26:27.392461,Alepa Otaniemi,xxx')
        testi_sovellus = Sovellus()
        testi_csvlukija = CsvLukija('testifile.txt', testi_sovellus)

        with self.assertRaises(VirheellinenCSVError):
            testi_csvlukija.lue_tiedosto()

    def test_tietoja_puuttuu(self):
        with open('testifile.txt', 'w') as testi_tiedosto:
            testi_tiedosto.write('tyyppi(veloitus tai hyvitys),timestamp,kauppa,summa\n')
            testi_tiedosto.write('veloitus,Alepa Otaniemi,20')
        testi_sovellus = Sovellus()
        testi_csvlukija = CsvLukija('testifile.txt', testi_sovellus)

        with self.assertRaises(VirheellinenCSVError):
            testi_csvlukija.lue_tiedosto()


class TestOmaKategoria(unittest.TestCase):

    def test_lisaa_kauppa(self):
        testikategoria = OmaKategoria('ruoka')
        testikategoria.lisaa_kauppa('valintatalo')
        testikategoria.lisaa_kauppa('sale')

        self.assertEqual(testikategoria.get_kaupat(), ['valintatalo', 'sale'], 'OmaKategoria ei palauttanut oikeita kauppoja')


class TestTilitapahtumat(unittest.TestCase):

    def test_lisaa_transaktio_uusi_kauppa(self):
        testitilitapahtumat = Tilitapahtumat()
        testitransaktio = Veloitus('sale', 20)
        testitransaktio2 = Hyvitys('siwa', 30)
        testitilitapahtumat.lisaa_transaktio(testitransaktio)
        testitilitapahtumat.lisaa_transaktio(testitransaktio2)

        self.assertEqual(testitilitapahtumat.get_transaktiot(), {'sale': [testitransaktio], 'siwa': [testitransaktio2]}, 'Metodi lisaa_transaktio ei toimi kunnolla')

    def test_lisaa_transaktio_vanha_kauppa(self):
        testitilitapahtumat = Tilitapahtumat()
        testitransaktio = Veloitus('sale', 20)
        testitransaktio2 = Hyvitys('siwa', 30)
        testitilitapahtumat.lisaa_transaktio(testitransaktio)
        testitilitapahtumat.lisaa_transaktio(testitransaktio2)
        testitransaktio3 = Veloitus('sale', 40)
        testitransaktio4 = Veloitus('siwa', 40)
        testitilitapahtumat.lisaa_transaktio(testitransaktio3)
        testitilitapahtumat.lisaa_transaktio(testitransaktio4)

        self.assertEqual(testitilitapahtumat.get_transaktiot(), {'sale': [testitransaktio, testitransaktio3], 'siwa': [testitransaktio2, testitransaktio4]}, 'Metodi lisaa_transaktio ei toimi kunnolla')


class TestSovellusLuoYhteenveto(unittest.TestCase):

    def test_luo_yhteenveto_kategorioittain(self):
        sovellus = Sovellus()
        kategoria = sovellus.luo_oma_kategoria('ruoka')
        kategoria.lisaa_kauppa('alepa')
        kategoria.lisaa_kauppa('k')
        kategoria2 = sovellus.luo_oma_kategoria('urheilu')
        kategoria2.lisaa_kauppa('xxl')

        self.assertEqual(sovellus.luo_yhteenveto_kategorioittain(), ([f'Kulutus yhteensä kategoriassa ruoka: 0 euroa\n', f'Kulutus yhteensä kategoriassa urheilu: 0 euroa\n'], ['ruoka', 'urheilu'], [0, 0]))



if __name__ == '__main__':
    unittest.main()
