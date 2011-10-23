#!/usr/bin/python
# -*- encoding: utf-8 -*-

from collections import deque
import random

class Mind(object):
    def __init__(self):
        self.richtige = 0
        self.fertige = 0
        self.liste = []
        self.anzahl = None

    def setAufgaben(self, liste):
        random.shuffle(liste)
        self.liste = liste
        self.anzahl = len(liste)

    def gibNextId(self):
        if self.liste[0][2] is None:
            return self.liste[0][0]
        else:
            return None

    def werteaus(self, wahl):
        if wahl != "s":
            self.liste[0][2] = wahl
            if wahl == self.liste[0][1].lower():
                self.richtige += 1
                self.fertige += 1
                self.liste = self._rotiere(self.liste)
            elif wahl != "x":
                self.fertige += 1
                self.liste = self._rotiere(self.liste)
        else:
            if self.fertige == 0:
                self.liste = self._rotiere(self.liste)
            else:
                schlange = deque(self.liste[:-self.fertige])
                schlange.rotate(-1)
                self.liste = list(schlange) + self.liste[self.anzahl-self.fertige:]

    def gibErgebnis(self):
        return self.richtige, self.fertige, self.anzahl

    def gibAntString(self):
        l = self.liste
        for i in xrange(self.anzahl-self.fertige):
            l[i][2] = "x"
        l.sort()
        antstring = ""
        for a in l:
            for b in a:
                antstring += str(b)
        return antstring

    def _rotiere(self, liste):
        """Rotiert ganze Liste."""
        schlange = deque(liste)
        schlange.rotate(-1)
        return list(schlange)
