# tilitapahtumien_seuranta
harjoitustyö pythonilla, johon voi syöttää tilitapahtumia ja saada yhteenvedon rahankulutuksesta

**Käyttöohje**


Sovellus käynnistetään ajamalla main-moduuli.


**Tilitapahtumien lukeminen ja syöttäminen
**
Sovelluksen käynnistettyään käyttäjä voi painaa Tuo CSV-tiedosto -nappia (CTRL + F), jolloin käyttäjä ohjataan valitsemaan tietokoneeltaan CSV-tiedoston (tekstitiedosto joka
vastaa CSV-tiedostoa). Kun käyttäjä tuplaklikkaa tiedostoa, ohjelma lukee tiedoston ja tallentaa tilitapahtumat ohjelmaan. Ohjelma tarkistaa tiedoston rivit ja 
käyttöliittymä ilmoittaa, onnistuiko tiedoston lukeminen.
(esimerkkitiedostosta "esimerkki.csv" näkee millaisia tiedostoja ohjelma lukee)

Vaihtoehtoisesti tilitapahtumia voi myös syöttää manuaalisesti veloitus- sekä hyvityskenttiin. Tällöin käyttäjän tulee syöttää jompaankumpaan kenttään kaupan nimi sekä summa
pilkulla erotettuna. Ohjelma tarkistaa rivin ja ilmoittaa käyttäjälle, onnistuiko transaktion tallentaminen.

Käyttävä voi syöttää useita tilitapahtumia ja tiedostoja missä tahansa järjestykessä.



**Kategorian luominen
**
Painamalla "Luo kategoria" -nappia, ohjelma pyytää käyttäjää syöttämään kategorian nimen, minkä jälkeen ohjelma kyselee kauppojen nimiä jotka käyttäjä sisällyttää kategoriaan.
Ohjelma tarkastaa, että saman nimistä kategoriaa ei ole aikaisemmin luotu, ja että lisättävä kauppa ei ole valmiiksi jo jossakin muussa kategoriassa. Kauppa voi sisältyä
vain yhteen kategoriaan, jotta siihen mennyt kulutus otetaan huomioon vain kerran yhteenvetoa tulostettaessa. Lopuksi käyttäjän tulee painaa "cancel", kun kaikki kaupat on lisätty.

Jos käyttäjä haluaa poistaa luomansa kategorian, voi hän painaa "Poista kategoria" -nappia, jolloin ohjelma kysyy poistettavan kategorian nimen ja poistaa kategorian.



**Yhteenveto kulutuksesta
**
Käyttäjä saa yhteenvedon tilitapahtumista painamalla "Luo yhteenveto kaupoittain" tai "Luo yhteenveto kategorioilla" -nappeja, jolloin ohjelma näyttää piirakkadiagrammin
sekä kauppojen/kategorioiden prosentuaalisen kulutuksen jakautumisen. Jos kauppa ei sisälly mihinkään kategoriaan yhteenvedossa kategorioilla, tulostuu kaupan kulutus sellaisenaan.
Yhteenvedon luomisen jälkeen voi lisätä uusia tilitapahtumia ja kategorioita, ja tulostaa päivitetyn yhteenvedon. Painamalla vuorotellen "Luo yhteenveto kaupoittain" ja 
"Luo yhteenveto kategorioilla", käyttäjä voi saada yhteenvedon ilman kategorioita sekä niiden kanssa.

