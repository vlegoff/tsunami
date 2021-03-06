# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the copyright holder nor the names of its contributors
#   may be used to endorse or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.


"""Fichier contenant le module primaire temps."""

from time import time

from abstraits.module import *
from primaires.meteo.perturbations.base import OPAQUE
from .config import cfg_temps
from .temps import Temps
from .variable import TempsVariable
from . import commandes

class Module(BaseModule):

    """Cette classe contient les informations du module primaire temps.

    Ce module gère le temps, son écoulement et sa mesure. Une configuration
    complète de ce module permet de savoir :
    -   quelles sont les unités de temps (années, saisons, mois...)
    -   à quelle vitesse s'écoule le temps

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "temps", "primaire")
        self.cfg = None
        self.temps = None
        self.met_changer_jour = []
        self.met_changer_mois = []
        self.met_changer_annee = []
        self.synchroniser = False

    def config(self):
        """Méthode de configuration du module"""
        self.cfg = type(self.importeur).anaconf.get_config("temps",
            "temps/temps.cfg", "config temps", cfg_temps)

        self.synchroniser = self.cfg.synchro

        # On crée les hooks du module
        importeur.hook.ajouter_hook("temps:minute",
                "Hook appelé quand on change de minute.")
        importeur.hook.ajouter_hook("temps:heure",
                "Hook appelé quand on change d'heure.")
        importeur.hook.ajouter_hook("temps:jour",
                "Hook appelé quand on change de jour.")
        importeur.hook.ajouter_hook("temps:mois",
                "Hook appelé quand on change de mois.")
        importeur.hook.ajouter_hook("temps:annee",
                "Hook appelé quand on change d'année.")

        BaseModule.config(self)

    def init(self):
        """Initialisation du module"""
        # On récupère ou crée le temps
        temps = self.importeur.supenr.charger_unique(Temps)
        if temps is None:
            temps = Temps(self.cfg)
        else:
            temps.formatage_date = self.cfg.formatage_date
            temps.formatage_heure = self.cfg.formatage_heure

        self.temps = temps

        self.importeur.hook["salle:regarder"].ajouter_evenement(
                self.voir_ciel)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.temps.CmdTemps(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

    def preparer(self):
        """Préparation du module"""
        self.inc()

    def inc(self):
        """Incrémentation du temps"""
        self.importeur.diffact.ajouter_action("inc_temps",
                1, self.inc)

        t2 = time()
        if self.synchroniser:
            t1 = self.temps.timestamp
            delta = int(t2 - t1)
            if delta > 3600:
                print("Hoquet temporel :", delta, "secondes")
                self.temps.timestamp = t2
                return

            if delta > 100:
                delta = 100
            t2 = t1 + delta
        else:
            delta = 1

        for i in range(delta):
            self.temps.inc()

        self.temps.timestamp = t2

    def avancer(self, secondes):
        """Avance le temps du nombre de secondes IRL données."""
        for i in range(secondes):
            self.temps.inc()

    def voir_ciel(self, salle, liste_messages, flags):
        """Renvoie l'apparence du ciel"""
        opaque = False
        for pertu in self.importeur.meteo.perturbations_actuelles:
            if pertu.est_sur(salle):
                opaque = True
                break
        if salle.exterieur and not opaque:
            liste_messages.append("|cy|" + self.temps.ciel_actuel + "|ff|")

    @property
    def variable(self):
        """Retourne le temps variable."""
        return TempsVariable()

    def changer_minute(self):
        """Change de minute."""
        importeur.hook["temps:minute"].executer(self.temps)

    def changer_heure(self):
        """Change d'heure."""
        importeur.hook["temps:heure"].executer(self.temps)

    def changer_jour(self):
        """Change de jour."""
        importeur.hook["temps:jour"].executer(self.temps)

    def changer_mois(self):
        """Change de mois."""
        importeur.hook["temps:mois"].executer(self.temps)

    def changer_annee(self):
        """Appel les callbacks contenus dans met_changer_annee."""
        importeur.hook["temps:annee"].executer(self.temps)
