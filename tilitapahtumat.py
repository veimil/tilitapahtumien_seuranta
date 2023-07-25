
'''kaikki kirjatut tapahtumat tallennetaan tämän luokan olioon'''


class Tilitapahtumat:
    def __init__(self):
        self.__transaktiot = {}      #   kaikki sovelluksen transaktiot säilötään tähän muuttujaan (kaupannimi: [transaktio1, transaktio2...])

    def get_transaktiot(self):
        return self.__transaktiot

    def lisaa_transaktio(self, transaktio):
        kauppa = transaktio.get_kauppa()
        if kauppa not in self.__transaktiot:
            self.__transaktiot[kauppa] = []
        self.__transaktiot[kauppa].append(transaktio)


