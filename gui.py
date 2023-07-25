
from PyQt6 import QtWidgets, QtGui
from csv_lukija import CsvLukija
from virheellinen_csv_error import VirheellinenCSVError
from random import randint


class GUI(QtWidgets.QMainWindow):
    def __init__(self, sovellus):
        super().__init__()
        self.sovellus = sovellus
        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setGeometry(300, 0, 1000, 500)
        self.init_ui()

    def init_ui(self):
        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)
        self.setGeometry(50, 50, 850, 600)
        self.setWindowTitle('Rahankäytön seuranta -laskin')

        self.hbox = QtWidgets.QHBoxLayout()
        self.central_widget.setLayout(self.hbox)

        otsikko = QtWidgets.QLabel('Tällä laskimella voit seurata rahankäyttöäsi. Ole hyvä ja valitse toiminto alta:', self)
        self.vbox = QtWidgets.QVBoxLayout()
        self.hbox.addLayout(self.vbox)
        self.vbox.addWidget(otsikko)
        self.vbox.addWidget(QtWidgets.QLabel('Valitse CSV-tiedosto, jolta tilitapahtumat luetaan:'))
        self.tuo_csv_nappi = QtWidgets.QPushButton('Tuo CSV-tiedosto (Ctrl + F)', self)
        self.tuo_csv_nappi.setShortcut('Ctrl+F')
        self.tuo_csv_nappi.clicked.connect(self.tuo_csv)
        self.vbox.addWidget(self.tuo_csv_nappi)

        self.vbox.addWidget(QtWidgets.QLabel('Vaihtoehtoisesti voit syöttää tilitapahtumia manuaalisesti yksitellen:'))
        self.vbox.addWidget(
            QtWidgets.QLabel('Syötä veloituksen kauppa ja summa pilkulla erotettuna.'))
        veloitus_hbox = QtWidgets.QHBoxLayout()
        self.rivi_veloitus = QtWidgets.QLineEdit()
        self.kirjaa_veloitus_nappi = QtWidgets.QPushButton('Kirjaa veloitus', self)
        self.kirjaa_veloitus_nappi.clicked.connect(self.tarkista_rivi_veloitus)
        veloitus_hbox.addWidget(self.rivi_veloitus)
        veloitus_hbox.addWidget(self.kirjaa_veloitus_nappi)
        self.vbox.addLayout(veloitus_hbox)
        self.veloitus_kunnossa = QtWidgets.QLabel('')
        self.vbox.addWidget(self.veloitus_kunnossa)

        self.vbox.addWidget(
            QtWidgets.QLabel('Jos sinulla on hyvityksiä joistakin veloituksista, voit syöttää ne tähän.'))
        self.vbox.addWidget(
            QtWidgets.QLabel('HUOM. kauppaan kohdistuva kokonaiskulutus ei voi kuitenkaan olla negatiivinen!'))
        self.vbox.addWidget(
            QtWidgets.QLabel('Syötä hyvityksen kauppa ja summa pilkulla erotettuna.'))
        hyvitys_hbox = QtWidgets.QHBoxLayout()
        self.rivi_hyvitys = QtWidgets.QLineEdit()
        self.kirjaa_hyvitys_nappi = QtWidgets.QPushButton('Kirjaa hyvitys', self)
        self.kirjaa_hyvitys_nappi.clicked.connect(self.tarkista_rivi_hyvitys)
        hyvitys_hbox.addWidget(self.rivi_hyvitys)
        hyvitys_hbox.addWidget(self.kirjaa_hyvitys_nappi)
        self.vbox.addLayout(hyvitys_hbox)
        self.hyvitys_kunnossa = QtWidgets.QLabel('')
        self.vbox.addWidget(self.hyvitys_kunnossa)

        self.luo_kategoria_nappi = QtWidgets.QPushButton('Luo kategoria', self)
        self.luo_kategoria_nappi.setShortcut('Ctrl+K')
        self.luo_kategoria_nappi.clicked.connect(self.luo_kategoria)
        self.vbox.addWidget(self.luo_kategoria_nappi)

        self.poista_kategoria_nappi = QtWidgets.QPushButton('Poista kategoria', self)
        self.poista_kategoria_nappi.clicked.connect(self.poista_kategoria)
        self.poista_kategoria_nappi.setShortcut('Ctrl+D')
        self.vbox.addWidget(self.poista_kategoria_nappi)

        self.luo_yhteenveto_nappi = QtWidgets.QPushButton('Luo yhteenveto kaupoittain', self)
        self.luo_yhteenveto_nappi.clicked.connect(self.luo_yhteenveto)
        self.luo_kategorioittain_nappi = QtWidgets.QPushButton('Luo yhteenveto kategorioilla', self)
        self.luo_kategorioittain_nappi.clicked.connect(self.luo_kategorioilla)
        self.yhteenveto_napit_hbox = QtWidgets.QHBoxLayout()
        self.yhteenveto_napit_hbox.addWidget(self.luo_yhteenveto_nappi)
        self.yhteenveto_napit_hbox.addWidget(self.luo_kategorioittain_nappi)
        self.vbox.addLayout(self.yhteenveto_napit_hbox)
        self.info_alhaalla = QtWidgets.QLabel('')
        self.vbox.addWidget(self.info_alhaalla)

        self.vbox_oikea = QtWidgets.QVBoxLayout()
        self.yhteenveto_otsikko = QtWidgets.QLabel('Yhteenveto kulutuksesta:')
        self.groupbox = QtWidgets.QGroupBox()
        self.vbox_oikea.addWidget(self.yhteenveto_otsikko)
        self.hbox.addLayout(self.vbox_oikea)

        self.vbox_oikea.addWidget(self.view)

        self.show()

    def luo_kategoria(self):
        nimi_dialog, ok = QtWidgets.QInputDialog.getText(self, 'Luo oma kategoria', 'Kirjoita kategorian nimi:')
        kategorian_nimi = nimi_dialog.strip().lower()
        if ok:
            if len(kategorian_nimi) == 0:
                self.info_alhaalla.setText('Syötä kategorian nimi kenttään ja paina OK')
                self.info_alhaalla.setStyleSheet("background-color : pink;")
            else:
                self.uusi_kategoria_nimi = kategorian_nimi
                self.kategoria = self.sovellus.luo_oma_kategoria(self.uusi_kategoria_nimi)
                if not self.kategoria:                                                      #   jos sovelluksessa on jo kategorian_nimi -niminen kategoria, metodi palauttaa False
                    self.info_alhaalla.setText('Kategoria löytyy jo annetulla nimellä')
                    self.info_alhaalla.setStyleSheet("background-color : pink;")
                else:
                    self.info_alhaalla.setText(f'Luotu kategoria {self.uusi_kategoria_nimi}.')
                    self.info_alhaalla.setStyleSheet("background-color : green;")
                    self.lisaa_kauppa_kategoriaan()

    def poista_kategoria(self):
        nimi_dialog, ok = QtWidgets.QInputDialog.getText(self, 'Poista kategoria', 'Syötä poistettavan kategorian nimi:')
        if ok:
            kategorian_nimi = nimi_dialog.strip().lower()
            if not self.sovellus.poista_kategoria(kategorian_nimi):         #   tarkistetaan, löytyykö kategoriaa 'kategorian_nimi', missä tapauksessa se poistetaan
                self.info_alhaalla.setText(f'Kategoriaa {kategorian_nimi} ei löytynyt.')
                self.info_alhaalla.setStyleSheet("background-color : pink;")
            else:
                self.info_alhaalla.setText(f'Poistettu kategoria {kategorian_nimi}')
                self.info_alhaalla.setStyleSheet("background-color : green;")

    def lisaa_kauppa_kategoriaan(self):
        kauppa_dialog, ok = QtWidgets.QInputDialog.getText(self, 'Lisää kauppa', 'Kirjoita lisättävän kaupan nimi:')
        if ok:
            kaupan_nimi = kauppa_dialog.strip().lower()
            if len(kaupan_nimi) == 0:
                self.info_alhaalla.setText('Syötä kaupan nimi kenttään ja paina OK')
                self.info_alhaalla.setStyleSheet("background-color : pink;")
            elif self.sovellus.tarkista_kauppa(kaupan_nimi):      #   tarkistetaan, kuuluuko kauppa mihinkään valmiiseen kategoriaan, koska ei haluta lisätä samaa kulutusta useaan otteeseen
                self.kategoria.lisaa_kauppa(kaupan_nimi)        #   lisätään äsken luotuun kategoriaan kauppa OmaKategoria-luokan lisaa_kauppa -metodilla
                self.info_alhaalla.setText(f'Lisätty kauppa {kaupan_nimi}')
                self.info_alhaalla.setStyleSheet("background-color : green;")
            else:
                self.info_alhaalla.setText(f'Kauppa sisältyy jo johonkin kategoriaan')
                self.info_alhaalla.setStyleSheet("background-color : pink;")
            self.lisaa_kauppa_kategoriaan()              #   jatketaan kysymistä ja kauppojen lisäämistä kategoriaan niin kauan kunnes käyttäjä painaa cancel
        self.info_alhaalla.setText('Kategorian luonti onnistui.')
        self.info_alhaalla.setStyleSheet("background-color : green;")

    def tuo_csv(self):
        tiedostonimi = QtWidgets.QFileDialog.getOpenFileName(self, 'Open CSV-file')
        if tiedostonimi[0]:
            self.csv_lukija = CsvLukija(tiedostonimi[0], self.sovellus)         #   luodaan CsvLukija-olio jolle annetaan parametreiksi tiedostonimi sekä sovellus, jota gui käyttää
            try:
                palaute = self.csv_lukija.lue_tiedosto()
                if palaute == 'Tiedosto luettu.':
                    self.info_alhaalla.setText('Tiedosto luettu.')
                    self.info_alhaalla.setStyleSheet("background-color : green;")
            except VirheellinenCSVError as e:                   #   tulostetaan CsvLukija-luokan lue_tiedosto-metodin heittämän VirheellinenCSVError -errorin kuvaus
                error_kuvaus = e.kuvaus
                self.info_alhaalla.setText(error_kuvaus)
                self.info_alhaalla.setStyleSheet("background-color : pink;")

    def tarkista_rivi_veloitus(self):
        ok = True
        palaute = ''
        try:
            osat = self.rivi_veloitus.text().split(',')
            if len(osat) > 2 or len(osat) < 2:          #   varmistetaan, että käyttäjä antaa vain kaksi arvoa pilkulla erotettuna
                raise ValueError
            kaupannimi = osat[0].strip().lower()
            summa = osat[1].strip()
            summa = float(summa)
        except IndexError:
            palaute = 'Virheellinen rivi, yritä uudestaan'
            ok = False
        except ValueError:
            palaute = 'Virheellinen rivi, yritä uudestaan'
            ok = False
        if ok:
            self.sovellus.luo_transaktio(kaupannimi, 'veloitus', summa)     #   sovellus huolehtii transaktion luomisesta
            palaute = 'OK'
        self.veloitus_kunnossa.setText(palaute)
        if palaute == 'OK':
            self.veloitus_kunnossa.setStyleSheet("background-color : green;")
        else:
            self.veloitus_kunnossa.setStyleSheet("background-color : pink;")
        self.rivi_veloitus.clear()

    def tarkista_rivi_hyvitys(self):
        ok = True
        palaute = ''
        try:
            osat = self.rivi_hyvitys.text().split(',')
            if len(osat) > 2 or len(osat) < 2:
                raise ValueError
            kaupannimi = osat[0].strip().lower()
            summa = osat[1].strip()
            summa = float(summa)
        except IndexError:
            palaute = 'Virheellinen rivi, yritä uudestaan'
            ok = False
        except ValueError:
            palaute = 'Virheellinen rivi, yritä uudestaan'
            ok = False
        if ok:
            self.sovellus.luo_transaktio(kaupannimi, 'hyvitys', summa)
            palaute = 'OK'
        self.hyvitys_kunnossa.setText(palaute)
        if palaute == 'OK':
            self.hyvitys_kunnossa.setStyleSheet("background-color : green;")
        else:
            self.hyvitys_kunnossa.setStyleSheet("background-color : pink;")
        self.rivi_hyvitys.clear()

    def luo_yhteenveto(self):
        self.scene.clear()
        asteet = 16
        start = 0
        mones_kauppa = 0
        otsikkoteksti = QtWidgets.QGraphicsTextItem('Yhteenveto kaupoittain:')
        self.scene.addItem(otsikkoteksti)
        lista, lista_kaupat, lista_summat = self.sovellus.luo_yhteenveto_kaupoittain()
        kokonaissumma = 0
        tekstipositio = 35
        for i in lista_summat:
            kokonaissumma += i
        for kauppa in lista:
            summan_osuus = lista_summat[mones_kauppa] / kokonaissumma * 360         #   lasketaan, jotta tiedetään kuinka paljon piirakkadiagrammia piirretään
            kulutus_per_kauppa_teksti = QtWidgets.QGraphicsTextItem(kauppa)
            kulutus_per_kauppa_teksti.setPos(20, tekstipositio)
            kulutus_per_kauppa_vari = QtWidgets.QGraphicsEllipseItem(0, tekstipositio + 8, 10, 10)
            kulutus_per_kauppa_vari.setStartAngle(1 * asteet)
            kulutus_per_kauppa_vari.setSpanAngle(360 * asteet)
            kaupan_vari = QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255))
            kulutus_per_kauppa_vari.setBrush(kaupan_vari)
            ellipsi = QtWidgets.QGraphicsEllipseItem(10, 350, 160, 160)
            ellipsi.setStartAngle(int(start) * asteet)
            ellipsi.setSpanAngle(int(summan_osuus) * asteet)
            ellipsi.setBrush(kaupan_vari)
            self.scene.addItem(kulutus_per_kauppa_teksti)
            self.scene.addItem(kulutus_per_kauppa_vari)

            prosentti = QtWidgets.QGraphicsTextItem(
                f'{int(lista_summat[mones_kauppa] / kokonaissumma * 100)} %')
            prosentti.setPos(int(len(kauppa) * 5) + 50, tekstipositio)
            self.scene.addItem(prosentti)

            start += summan_osuus
            mones_kauppa += 1
            tekstipositio += 18
            self.scene.addItem(ellipsi)

    def luo_kategorioilla(self):
        self.scene.clear()
        asteet = 16
        start = 0
        mones_kauppa_tai_kategoria = 0
        otsikkoteksti = QtWidgets.QGraphicsTextItem('Yhteenveto kategorioilla:')
        self.scene.addItem(otsikkoteksti)
        lista, lista_nimet, lista_summat = self.sovellus.luo_yhteenveto_kategorioittain()
        kokonaissumma = 0
        tekstipositio = 35
        for i in lista_summat:
            kokonaissumma += i
        if kokonaissumma == 0:
            for kauppa in lista:
                kulutus_per_kauppa_tai_kategoria_teksti = QtWidgets.QGraphicsTextItem(kauppa)
                kulutus_per_kauppa_tai_kategoria_teksti.setPos(20, tekstipositio)
                self.scene.addItem(kulutus_per_kauppa_tai_kategoria_teksti)
                prosentti = QtWidgets.QGraphicsTextItem('0 %')
                prosentti.setPos(int(len(kauppa) * 5) + 50, tekstipositio)
                self.scene.addItem(prosentti)
                tekstipositio += 18
        else:
            for kauppa in lista:
                summan_osuus = lista_summat[mones_kauppa_tai_kategoria] / kokonaissumma * 360
                kulutus_per_kauppa_tai_kategoria_teksti = QtWidgets.QGraphicsTextItem(kauppa)
                kulutus_per_kauppa_tai_kategoria_teksti.setPos(20, tekstipositio)
                kulutus_per_kauppa_tai_kategoria_vari = QtWidgets.QGraphicsEllipseItem(0, tekstipositio + 8, 10, 10)
                kulutus_per_kauppa_tai_kategoria_vari.setStartAngle(1 * asteet)
                kulutus_per_kauppa_tai_kategoria_vari.setSpanAngle(360 * asteet)
                kaupan_tai_kategorian_vari = QtGui.QColor(randint(0, 255), randint(0, 255), randint(0, 255))
                kulutus_per_kauppa_tai_kategoria_vari.setBrush(kaupan_tai_kategorian_vari)
                self.scene.addItem(kulutus_per_kauppa_tai_kategoria_vari)
                self.scene.addItem(kulutus_per_kauppa_tai_kategoria_teksti)

                ellipsi = QtWidgets.QGraphicsEllipseItem(10, 350, 160, 160)
                ellipsi.setStartAngle(int(start) * asteet)
                ellipsi.setSpanAngle(int(summan_osuus) * asteet)
                ellipsi.setBrush(kaupan_tai_kategorian_vari)

                prosentti = QtWidgets.QGraphicsTextItem(f'{int(lista_summat[mones_kauppa_tai_kategoria] / kokonaissumma * 100)} %')
                prosentti.setPos(int(len(kauppa) * 5) + 50, tekstipositio)
                self.scene.addItem(prosentti)

                start += summan_osuus
                mones_kauppa_tai_kategoria += 1
                tekstipositio += 18
                self.scene.addItem(ellipsi)


