#!/usr/bin/python
# -*- encoding: utf-8 -*-

import cli
import db
import mind
import time

class Trainer(object):
    def __init__(self):
        self.ui = cli.TrainerConsole()
        self.db = db.Datenbank()
        self.mind = mind.Mind()

    def main(self):
        self.ui.begruessung()
        while True:
            benutzername, passwort = self.ui.getLogin()
            if benutzername is None:
                return -1   # Programmende
            test = self.db.ticketanmeldung(benutzername, passwort)
            if test == -1:
                self.ui.keinticket()
            elif test == -2:
                self.ui.schonbearbeitet()
            elif test == -3:
                self.ui.abgelaufen()
            else:
                Testname = test[0]
                ModulId = test[1]
                self.ui.eingeloggt()
                break
            self.ui.neuerversuch()

        ModulInfos = self.db.getModul(ModulId)
        Aufgaben = self.db.getAufgaben(ModulId)
        anzahl = self.db.gibAufgabenanzahl()

        self.ui.startinfo(Testname,ModulInfos[0],ModulInfos[1],anzahl)
        while True:
            antwort = self.ui.starten()
            if antwort == "n":
                self.ui.ende()
                return -1           # Programmende
            elif antwort == "j":
                break

        self.db.setEinlogZeit()

        self.mind.setAufgaben([ [key,Aufgaben[key][2],None]
            for key in Aufgaben ])

        initzeit = time.time()
        zeit = 0.0
        while self.mind.gibNextId():
            self.ui.zeigeaufgabe(self.mind.gibNextId(),
                    Aufgaben[self.mind.gibNextId()])
            wahl = self.ui.antwort()
            while True:
                if wahl == "x":
                    if self.ui.wirklichabbrechen() == "j":
                        self.mind.werteaus(wahl)
                        break
                    else:
                        wahl = self.ui.antwort()
                elif wahl == "s":
                    self.ui.geschoben()
                    self.mind.werteaus(wahl)
                    break
                elif wahl in ["a","b","c","d"]:
                    self.mind.werteaus(wahl)
                    break
                else:
                    wahl = self.ui.antwort()

            zeit = time.time()-initzeit
            self.ui.zeit(divmod(zeit, 60))

        ergebnis = self.mind.gibErgebnis()
        self.db.setErgebnis(ergebnis[0],zeit,self.mind.gibAntString())
        self.ui.ergebnis(Testname,ergebnis,(divmod(zeit, 60)))

if __name__ == "__main__":
    foo = Trainer()
    foo.main()
