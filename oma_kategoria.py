from hyvitys import Hyvitys
from veloitus import Veloitus


class OmaKategoria:

    ''' luokka käyttäjän itse luomia kategorioita varten'''

    def __init__(self, nimi):
        self.__nimi = nimi
        self.__kaupat = []          #   lista kaupannimistä, jotka kuuluvat OmaKategoria-oliolle

    def get_nimi(self):
        return self.__nimi

    def get_kaupat(self):               #   palauttaa listan kaupannimistä, jotka kuuluvat kategoriaan
        return self.__kaupat

    def lisaa_kauppa(self, kaupannimi):
        self.__kaupat.append(kaupannimi)

