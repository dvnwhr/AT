#!/usr/bin/python
# -*- encoding: utf-8 -*-

import MySQLdb

class Datenbank(object):
    def __init__(self):
        self.cn = None
        self.TicketId = None
        self.Aufgabenanzahl = None
        self._verbinde()

    def __del__(self):
        self._schliesse()

    def _verbinde(self):
        self.cn = MySQLdb.connect( host = "aufgabentrainer.db.7930692.hostedresource.com",
                            user = "aufgabentrainer",
                            passwd = "Agtrainer1",
                            db = "aufgabentrainer",
                            use_unicode = True,
                            #charset="utf8"
                            )

    def _schliesse(self):
        try:
            self.cn.close()
        except MySQLdb.ProgrammingError as e:
            if e[0] == "closing a closed connection":
                #print "Catched:",  e[0]
                pass
            else:
                print "Exception:", e

    def getModul(self, modulid):
        sql = "SELECT Modultitel, Introtext FROM module WHERE %s=Id"
        modul = self._getone(sql, (modulid,))
        return modul

    def getAufgaben(self, modulid):
        sql = """SELECT Id, Frage, A, B, C, D, Loesungsbuchstabe
            FROM aufgaben WHERE ModulId=%s""" # evtl. noch ORDER BY Id ASC"""
        aufgaben = self._getall(sql, (modulid,))
        self.Aufgabenanzahl = len(aufgaben)
        Aufgaben = {}
        for i in xrange(self.Aufgabenanzahl):
            Aufgaben[aufgaben[i][0]] = (aufgaben[i][1],
                    (aufgaben[i][2],aufgaben[i][3],aufgaben[i][4],aufgaben[i][5])
                    ,aufgaben[i][6])
        return Aufgaben

    def gibAufgabenanzahl(self):
        return self.Aufgabenanzahl

    def ticketanmeldung(self, benutzername, passwort):
        sql = """SELECT EinlogZeit, TestId, Id FROM tickets 
            WHERE Benutzername=%s AND Passwort=%s"""
        ticket = self._getone(sql, (benutzername, passwort))
        if ticket:
            EinlogZeit = ticket[0]
            if EinlogZeit is None:
                TestId = ticket[1]
                self.TicketId = ticket[2]
                sql = """SELECT name, modulid FROM tests WHERE %s=id
                    AND gueltigvon < NOW() AND NOW() < gueltigbis"""
                test = self._getone(sql, (TestId,))
                if test:
                    return test
                else:
                    return -3 # Nicht innerhalb des Zeitfensters
            else:
                return -2 # Schon bearbeitet
        else:
            return -1 # Kein Ticket gefunden

    def setEinlogZeit(self, TicketId = None):
        if TicketId is None:
            TicketId = self.TicketId
        self._exe("""UPDATE tickets SET EinlogZeit = NOW()
                    WHERE Id=%s""", (TicketId,) )

    def setErgebnis(self, anzahlrichtige, bearbeitungszeit, antwortenstring):
        self._exe("""UPDATE tickets SET AnzahlRichtige = %s,
                Bearbeitungszeit = %s, Antwortenstring = %s WHERE Id=%s""",
                (anzahlrichtige, "%.2f" % bearbeitungszeit, antwortenstring,
                    self.TicketId))

    def _exe(self, befehl, argumente):
        self._getall(befehl, argumente)

    def _getone(self, befehl, argumente):
        try:
            cursor = self.cn.cursor()
            cursor.execute(befehl, argumente)
            return cursor.fetchone()
        except MySQLdb.OperationalError as e:
            if e[0] == 2006:
                #print "Caught", e
                self._schliesse()
                self._verbinde()
                cursor = self.cn.cursor()
                cursor.execute(befehl, argumente)
                return cursor.fetchone()
        finally:
            cursor.close()

    def _getall(self, befehl, argumente):
        try:
            cursor = self.cn.cursor()
            cursor.execute(befehl, argumente)
            return cursor.fetchall()
        except MySQLdb.OperationalError as e:
            if e[0] == 2006:
                self._schliesse()
                self._verbinde()
                cursor = self.cn.cursor()
                cursor.execute(befehl, argumente)
                return cursor.fetchall()
        finally:
            cursor.close()

