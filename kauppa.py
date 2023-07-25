
class Kauppa:

    def __init__(self, nimi):
        self.__nimi = nimi
        self.__transaktiot = []

    def get_transaktiot(self):
        return self.__transaktiot

    def lisaa_transaktio(self, summa):
        self.__transaktiot.append(summa)
