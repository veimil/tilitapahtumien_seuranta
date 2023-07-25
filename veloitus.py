from transaktio import Transaktio

#   aliluokka transaktioille, jotka ovat veloituksia tililtä
class Veloitus(Transaktio):
    def __init__(self, kaupannimi, summa):
        super().__init__(kaupannimi, summa)
        self.tyyppi = 'veloitus'

    def get_tyyppi(self):
        return self.tyyppi

