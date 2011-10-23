#!/usr/bin/python
# -*- encoding: utf-8 -*-

class TrainerConsole(object):
    def begruessung(self):
        print "Aufgabentrainer"
        print "===============\n"

    def getLogin(self):
        print "Wie lautet ihr Benutzername?",
        benutzername = raw_input()
        print "Wie lautet ihr Passwort?",
        passwort = raw_input()
        return benutzername, passwort

    def keinticket(self):
        print "Mit dieser Kombination aus Benutzername und Passwort gibt es kein Ticket"
    def schonbearbeitet(self):
        print "Dieses Ticket wurde schon einmal benutzt."
    def abgelaufen(self):
        print "Leider ist dieser Test schon abgelaufen."

    def neuerversuch(self):
        print "Bitte versuchen Sie es erneut."

    def eingeloggt(self):
        print "Login war erfolgreich.\n"

    def startinfo(self, Testname, Modultitel, Modulbeschreibung, AnzahlAufgaben):
        print "Test:",  Testname
        print "Modul:", Modultitel
        print "Modulbeschreibung:", Modulbeschreibung
        print "Anzahl Aufgaben:", str(AnzahlAufgaben)

    def starten(self):
        print "Wollen Sie diesen Test jetzt bearbeiten [j/n]:",
        return raw_input()

    def ende(self):
        print "Auf Wiedersehen."

    def zeigeaufgabe(self, Id, Aufgabe):
        print ""
        print "Id:", Id
        print "Frage:",  Aufgabe[0]
        for i in range(4):
            print chr(65+i) + ":", Aufgabe[1][i]

    def antwort(self):
        print "[a/b/c/d], s für Schieben oder x für Abbrechen:",
        return raw_input()

    def geschoben(self):
        print "Frage geschoben"

    def wirklichabbrechen(self):
        print "Wollen Sie wirklich abbrechen? [j/n]",
        return raw_input()

    def zeit(self, (m, s)):
        print "%d min %.2f sec" % (m, s)

    def ergebnis(self, test, (richtige, fertige, anzahl), (m, s)):
        print "\n=================="
        print "Auswertung"
        print "Test:", test
        print "Richtige:", richtige
        print "Es wurden", fertige, "von", anzahl, "Aufgaben bearbeitet."
        print "Zeit:", "%d min %.2f sec" % (m, s)


