class VirheellinenCSVError(Exception):

    #   oma virhe-luokka, jonka avulla voi antaa sopivaa informaatiota siitä mikä aiheutti virheen heittämisen

    def __init__(self, kuvaus):
        self.__kuvaus = kuvaus

    @property
    def kuvaus(self):
        return self.__kuvaus
