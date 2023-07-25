
import csv
from virheellinen_csv_error import VirheellinenCSVError

#   tämä luokka lukee tekstitiedoston, jossa jokainen rivi (paitsi otsikkorivi) on muotoa:
#   veloitus,2023-04-05 15:26:27.392461,kaupannimi,summa
class CsvLukija:
    def __init__(self, tiedostonimi, sovellus):
        self.__tiedostonimi = tiedostonimi
        self.__sovellus = sovellus

    def lue_tiedosto(self):
        try:
            with open(self.__tiedostonimi, 'r') as csv_tiedosto:
                csv_lukija = csv.reader(csv_tiedosto)
                next(csv_lukija)                        #   otsikon skippaaminen
                for rivi in csv_lukija:
                    tyyppi = rivi[0].strip().lower()
                    if tyyppi not in ('veloitus', 'hyvitys'):
                        raise VirheellinenCSVError('Virheellinen transaktiotyyppi tiedostossa (tapahtumatyypin tulee olla veloitus tai hyvitys)')
                    kaupannimi = rivi[2].strip().lower()
                    summa = rivi[3].strip()
                    summa = float(summa)
                    self.__sovellus.luo_transaktio(kaupannimi, tyyppi, summa)
                return "Tiedosto luettu."
        except IndexError:
            raise VirheellinenCSVError('Virheellinen rivi tiedostossa')
        except ValueError:
            raise VirheellinenCSVError('Virheellinen summa rivissä')

