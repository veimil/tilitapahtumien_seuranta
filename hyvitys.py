from transaktio import Transaktio

#   aliluokka transaktioille, jotka ovat hyvityksiä (rahan palautus tilille)
class Hyvitys(Transaktio):
    def __init__(self, kauppa, summa):
        super().__init__(kauppa, summa)
        self.tyyppi = 'hyvitys'

    def get_tyyppi(self):
        return self.tyyppi
