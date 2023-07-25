from tilitapahtumat import Tilitapahtumat
from veloitus import Veloitus
from hyvitys import Hyvitys
from csv_lukija import CsvLukija
from oma_kategoria import OmaKategoria
from virheellinen_csv_error import VirheellinenCSVError


'''Tämä luokka mallintaa sovellusta, mikä sisältää ohjelman keskeisen toiminnan'''


class Sovellus:
    def __init__(self):
        self.__tilitapahtumat = Tilitapahtumat()      #     sovelluksen keräämä tieto transaktioista säilötään luokan Tilitapahtumat-olioon
        self.__omat_kategoriat = []                #   tiedot itse luoduista kategorioista (lista OmaKategoria-olioista)

    def get_transaktiot(self):
        return self.__tilitapahtumat.get_transaktiot()

    def luo_transaktio(self, kaupannimi, tyyppi, summa):    #   luo transaktio-olion (veloitus/hyvitys) ja lisää sen applikaation Tilitapahtumat-olioon
        if tyyppi == 'hyvitys':
            transaktio = Hyvitys(kaupannimi, summa)
        elif tyyppi == 'veloitus':
            transaktio = Veloitus(kaupannimi, summa)
        self.__tilitapahtumat.lisaa_transaktio(transaktio)

    def luo_oma_kategoria(self, nimi):
        for oma_kategoria in self.__omat_kategoriat:        #   aluksi tarkistetaan, ettei ole jo valmiiksi toista 'nimi'-nimistä kategoriaa luotuna
            if oma_kategoria.get_nimi() == nimi:
                return False
        kategorian_nimi = nimi
        oma_kategoria = OmaKategoria(kategorian_nimi)       #   jos ei, niin luodaan uusi kategoria-olio ja iitetään se sovelluksen omiin kategorioihin
        self.__omat_kategoriat.append(oma_kategoria)
        return oma_kategoria

    def tarkista_kauppa(self, kaupannimi):      #   tarkistetaan, kuuluuko kauppa mihinkään kategoriaan. Jos ei, metodi palauttaa True, muuten False
        for kategoria in self.__omat_kategoriat:
            for kauppa in kategoria.get_kaupat():
                if kauppa == kaupannimi:
                    return False
        return True

    def poista_kategoria(self, kategorian_nimi):
        for oma_kategoria in self.__omat_kategoriat:
            if oma_kategoria.get_nimi() == kategorian_nimi:     #   poistettava kategoria löytyi, jolloin poistetaan se sovelluksen kategorioista ja metodi palauttaa True
                self.__omat_kategoriat.remove(oma_kategoria)
                return True
        return False

    def luo_yhteenveto_kaupoittain(self):                      #    luo yhteenvedon transaktioista kaupoittain. Ignooraa kategoriat
        transaktiot = self.get_transaktiot()
        lista = []
        lista_kaupat_nimet = []
        lista_summat = []
        for kauppa in transaktiot:
            i = 0
            for transaktio in transaktiot[kauppa]:           #    veloitukset lisätään kokonaiskulutukseen, ja hyvitykset vähennetään siitä
                if transaktio.get_tyyppi() == 'veloitus':
                    i += transaktio.get_summa()
                elif transaktio.get_tyyppi() == 'hyvitys':
                    i -= transaktio.get_summa()
            lista.append(f'Kulutus yhteensä kaupassa {kauppa}: {i} euroa')
            lista_kaupat_nimet.append(kauppa)
            lista_summat.append(i)
        return lista, lista_kaupat_nimet, lista_summat

    def luo_yhteenveto_kategorioittain(self):
        lista_kategorioilla = []
        lista_nimet = []
        lista_summat = []
        lista = []                         #    lisätään aluksi tähän listaan kaikki kaupat, jotka kuuluvat johonkin omaan kategoriaan
        for kategoria in self.__omat_kategoriat:
            for x in kategoria.get_kaupat():
                lista.append(x)
        transaktiot = self.get_transaktiot()       #   tilitapahtumat-sanakirja
        for kaupan_nimi in transaktiot:    #    Katsotaan kauppa kerrallaan, kuuluuko se mihinkään kategoriaan, jos ei niin kauppaan mennyt kulutus tulostuu sellaisenaan
            if kaupan_nimi not in lista:
                i = 0
                for transaktio in transaktiot[kaupan_nimi]:
                    if transaktio.get_tyyppi() == 'veloitus':
                        i += transaktio.get_summa()
                    else:
                        i -= transaktio.get_summa()
                lista_kategorioilla.append(f'Kulutus yhteensä kaupassa {kaupan_nimi}: {i} euroa\n')
                lista_nimet.append(kaupan_nimi)
                lista_summat.append(i)
        for kategoria in self.__omat_kategoriat:
            kategorian_kaupat = kategoria.get_kaupat()
            i = 0
            for kaupannimi in kategorian_kaupat:
                if kaupannimi in transaktiot:
                    for x in transaktiot[kaupannimi]:
                        if x.get_tyyppi() == "veloitus":
                            i += x.get_summa()
                        else:
                            i -= x.get_summa()
            lista_kategorioilla.append(f'Kulutus yhteensä kategoriassa {kategoria.get_nimi()}: {i} euroa\n')
            lista_nimet.append(kategoria.get_nimi())
            lista_summat.append(i)
        return lista_kategorioilla, lista_nimet, lista_summat


