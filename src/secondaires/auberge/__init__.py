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


"""Fichier contenant le module secondaire auberge."""

from abstraits.module import *
from primaires.format.fonctions import format_nb, supprimer_accents
from primaires.pnj.prototype import FLAGS as FLAGS_PNJ
from primaires.salle.salle import Salle
from secondaires.auberge.auberge import Auberge
from secondaires.auberge.commandes import *
from secondaires.auberge import editeurs
from secondaires.auberge import masques

class Module(BaseModule):

    """Module secondaire définissant les auberges.

    Les auberges sont des lieux dans lesquels un joueur peut louer
    une ou plusieurs chambres pour une durée spécifique. Les chambres
    ne peuvent être ouvertes ou fermées que par le propriétaire de
    la chambre.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "auberge", "secondaire")
        self.auberges = {}
        self.commandes = []
        self.logger = self.importeur.man_logs.creer_logger(
                "auberge", "auberge", "auberge.log")
        type(importeur).espace["auberges"] = self.auberges

    def config(self):
        """Configuration du module."""
        # Ajout des flags de salle
        FLAGS_PNJ.ajouter("peut visiter les auberges", 1)
        BaseModule.config(self)

    def init(self):
        """Chargement des navires et modèles."""
        # On récupère les auberges
        auberges = self.importeur.supenr.charger_groupe(Auberge)
        for auberge in auberges:
            self.ajouter_auberge(auberge)

        nb_auberges = len(auberges)
        self.logger.info(format_nb(nb_auberges,
                "{nb} auberge{s} récupérée{s}", fem=True))

        Salle.peut_entrer = Module.peut_entrer

        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.expulser_joueur)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.auberge.CmdAuberge(),
            commandes.louer.CmdLouer(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs
        self.importeur.interpreteur.ajouter_editeur(
                editeurs.aubedit.EdtAubedit)

    def preparer(self):
        """Préparation du module."""
        self.verifier_auberges()

    @property
    def vacances(self):
        """Retourne la liste des joueurs en mode vacance."""
        joueurs = []
        for auberge in self.auberges.values():
            for joueur in auberge.vacances:
                if joueur:
                    joueurs.append(joueur)

        joueurs = sorted(joueurs,
                key=lambda joueur: supprimer_accents(joueur.nom))
        return joueurs

    def verifier_auberges(self):
        """Vérification cyclique des auberges et expirations."""
        importeur.diffact.ajouter_action("auberges", 3600,
                self.verifier_auberges)
        for auberge in self.auberges.values():
            auberge.verifier_chambres()

    def get_auberge(self, salle):
        """Retourne, si trouvé, l'auberge définie dans la salle.

        Si l'auberge n'est pas trouvé, lève une exception KeyError.

        """
        for auberge in self.auberges.values():
            if auberge.comptoir is salle:
                return auberge

        raise KeyError(salle)

    def creer_auberge(self, cle):
        """Crée une nouvelle auberge."""
        if cle in self.auberges:
            raise ValueError("la clé d'auberge {} existe déjà".format(
                    repr(cle)))

        auberge = Auberge(cle)
        self.ajouter_auberge(auberge)
        return auberge

    def ajouter_auberge(self, auberge):
        """Ajoute l'auberge au dictionnaire."""
        if auberge.cle in self.auberges:
            raise ValueError("la clé d'auberge {} existe déjà".format(
                    repr(auberge.cle)))

        self.auberges[auberge.cle] = auberge

    def supprimer_auberge(self, cle):
        """Supprime l'auberge."""
        if cle not in self.auberges:
            raise ValueError("la clé d'auberge {} n'existe pas".format(
                    repr(cle)))

        auberge = self.auberges.pop(cle)
        auberge.detruire()

    @staticmethod
    def peut_entrer(salle, personnage):
        """Retourne True si le personnage peut entrer dans la salle."""
        if hasattr(personnage, "identifiant") and personnage.prototype.a_flag(
                "peut visiter les auberges"):
            return True

        for auberge in importeur.auberge.auberges.values():
            if salle.ident in auberge.chambres:
                chambre = auberge.chambres[salle.ident]
                return personnage is chambre.proprietaire

        return True

    def expulser_joueur(self, joueur):
        """Expulse un joueur si il est dans une chambre qui n'est pas à lui.

        Cette méthode est appelée quand un joueur se connecte.

        """
        salle = joueur.salle
        for auberge in self.auberges.values():
            for chambre in auberge.chambres.values():
                if salle in chambre.salles:
                    chambre.verifier_expiration()
                    if chambre.proprietaire is not joueur:
                        # On téléporte le joueur dans la salle de l'auberge
                        joueur << "|att|Vous n'êtes pas le propriétaire. " \
                                "Vous êtes expulsé de cette chambre !|ff|"
                        joueur.salle = auberge.comptoir
