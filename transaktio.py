
class Transaktio:
    def __init__(self, kauppa, summa):
        self.__kauppa = kauppa
        self.__summa = summa

    def get_kauppa(self):
        return self.__kauppa

    def get_summa(self):
        return self.__summa
