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


"""Fichier contenant le module primaire aide."""

try:
    import psutil
except ImportError:
    psutil = None

from abstraits.module import *
from primaires.format.fonctions import *
from primaires.information.config import cfg_info
from primaires.information import commandes

from .editeurs.hedit import EdtHedit
from .editeurs.nledit import EdtNledit
from .roadmap import Roadmap
from .newsletter import Newsletter
from .sujet import SujetAide
from .tips import Tips
from .versions import Versions
from .annonces import Annonces
from primaires.information.reboot import Reboot

class Module(BaseModule):

    """Cette classe représente le module primaire information.

    Ce module gère l'aide in-game, c'est-à-dire les sujets d'aide
    (fichier ./sujet.py), ainsi que le système de versions.

    """

    def __init__(self, importeur):
        """Constructeur du module"""
        BaseModule.__init__(self, importeur, "information", "primaire")
        self.__sujets = []
        self.tips = None
        self.versions = None
        self.annonces = None
        self.newsletters = []
        self.roadmaps = []
        self.logger = importeur.man_logs.creer_logger(
                "information", "information")
        self.reboot = None

    def config(self):
        """Configuration du module"""
        self.cfg_info = type(self.importeur).anaconf.get_config("config_info",
            "information/config.cfg", "config information", cfg_info)

        BaseModule.config(self)

    def init(self):
        """Initialisation du module.

        On récupère les sujets d'aide enregistrés, les versions,
        les newsletters et la roadmap.

        """
        sujets = self.importeur.supenr.charger_groupe(SujetAide)
        self.__sujets = sujets
        nb_sujets = len(sujets)
        self.logger.info(format_nb(nb_sujets, "{nb} sujet{s} d'aide " \
                "récupéré{s}"))

        versions = self.importeur.supenr.charger_unique(Versions)
        if versions is None:
            versions = Versions()
        self.versions = versions

        annonces = self.importeur.supenr.charger_unique(Annonces)
        if annonces is None:
            annonces = Annonces()
        self.annonces = annonces

        tips = self.importeur.supenr.charger_unique(Tips)
        if not tips:
            tips = Tips()
        self.tips = tips

        self.newsletters = sorted(importeur.supenr.charger_groupe(Newsletter),
                key=lambda nl: nl.date_creation)

        self.roadmaps = sorted(importeur.supenr.charger_groupe(Roadmap),
                key=lambda r: r.no)

        # On lie la méthode joueur_connecte avec l'hook joueur_connecte
        # La méthode joueur_connecte sera ainsi appelée quand un joueur
        # se connecte
        self.importeur.hook["joueur:connecte"].ajouter_evenement(
                self.joueur_connecte)

        # diffact pour psutil
        if psutil:
            importeur.diffact.ajouter_action("ver_mem", 60, self.surveiller_memoire)

        BaseModule.init(self)

    def ajouter_commandes(self):
        """Ajout des commandes dans l'interpréteur"""
        self.commandes = [
            commandes.aide.CmdAide(),
            commandes.annonces.CmdAnnonces(),
            commandes.hedit.CmdHedit(),
            commandes.newsletter.CmdNewsletter(),
            commandes.reboot.CmdReboot(),
            commandes.roadmap.CmdRoadmap(),
            commandes.tips.CmdTips(),
            commandes.versions.CmdVersions(),
        ]

        for cmd in self.commandes:
            self.importeur.interpreteur.ajouter_commande(cmd)

        # Ajout des éditeurs 'hedit' et 'nledit'
        self.importeur.interpreteur.ajouter_editeur(EdtHedit)
        self.importeur.interpreteur.ajouter_editeur(EdtNledit)

    def __getitem__(self, titre):
        """Retourne le sujet portant ce titre.

        Si le titre n'est pas trouvé, lève l'exception KeyError.
        La recherche du sujet se fait sans tenir compte des accents ni de
        la casse.

        """
        titre = supprimer_accents(titre).lower()
        for sujet in self.__sujets:
            if supprimer_accents(sujet.titre).lower() == titre:
                return sujet
        raise KeyError("le titre {} n'a pas pu être trouvé".format(titre))

    def __delitem__(self, titre):
        """Détruit un sujet d'aide de manière définitive."""
        titre = supprimer_accents(titre).lower()
        for sujet in self.__sujets:
            if supprimer_accents(sujet.titre).lower() == titre:
                titre = sujet
                break
        self.__sujets.remove(titre)
        titre.vider()
        titre.detruire()

    def get_sujet_par_mot_cle(self, mot):
        """Retourne le sujet correspondant à ce mot-clé."""
        mot = supprimer_accents(mot.lower())
        for sujet in self.__sujets:
            if mot in [supprimer_accents(m) for m in sujet.mots_cles]:
                return sujet
        return None

    def get_sujet(self, nom_sujet):
        """Retourne un sujet ou None si le sujet recherché n'existe pas.
        Contrairement à __getitem__ et get_sujet_par_mot_cle, le sujet est
        renvoyé indifféremment en fonction de son nom ou d'un mot-clé.

        """
        sujet = None
        try:
            sujet = self[nom_sujet]
        except KeyError:
            sujet = self.get_sujet_par_mot_cle(nom_sujet)
        return sujet

    @property
    def sujets(self):
        """Retourne un dictionnaire {cle: sujet} des sujets existants."""
        dic = {}
        for sujet in self.__sujets:
            dic[sujet.cle] = sujet

        return dic

    def ajouter_sujet(self, cle):
        """Ajoute un sujet à la liste des sujets d'aide.

        La clé du sujet doit être fournie en paramètre.
        Si la clé est déjà utilisée, lève une exception. Sinon, retourne
        le sujet nouvellement créé.

        """
        if cle in self.sujets.keys():
            raise ValueError("la clé {} est déjà utilisée".format(cle))
        sujet = SujetAide(cle)
        self.__sujets.append(sujet)
        return sujet

    def creer_newsletter(self, sujet):
        """Créée et retourne la News Letter."""
        newsletter = Newsletter(sujet)
        self.newsletters.append(newsletter)
        return newsletter

    def creer_roadmap(self, texte):
        """Crée un nouvel élément de la roadmap.

        Le texte contient le titre sous la forme "titre : texte".
        Par exemple, "exploration : 500 salles ouvrables". Si le
        deux point ne peut être trouvé, l'élément n'a pas de texte,
        juste un titre.

        """
        try:
            titre, texte = texte.split(":")
        except ValueError:
            titre = texte
            texte = ""

        # On nettoie le titre et le texte
        titre = titre.strip().lower()
        texte = texte.strip()

        if not titre:
            raise ValueError("Le titre de cette élément de feuille " \
                    "de route est vide.")

        # On crée l'élément de la feuille de route
        roadmap = Roadmap(titre, texte)
        self.roadmaps.append(roadmap)
        return roadmap

    def supprimer_roadmap(self, index):
        """Supprime un élément de la roadmap."""
        roadmap = self.roadmaps[index]
        roadmap.detruire()
        del self.roadmaps[index]

        for i, roadmap in enumerate(self.roadmaps):
            roadmap.no = i + 1

        Roadmap.no_actuel = len(self.roadmaps)

    def construire_sommaire_pour(self, personnage):
        """Retourne le sommaire de la rubrique d'aide pour personnage."""
        # On affiche la liste des sujets d'aides
        peut_lire = []
        for sujet in self.__sujets:
            if importeur.interpreteur.groupes.explorer_groupes_inclus(
                    personnage.grp, sujet.str_groupe):
                peut_lire.append(sujet)

        sujets_lire = []
        taille_max = 0
        for s in peut_lire:
            if len(s.titre) > taille_max:
                taille_max = len(s.titre)
        for sujet in peut_lire:
            if sujet.pere is None:
                cle = " (" + sujet.cle + ")" if personnage.est_immortel else ""
                sujets_lire.append(
                        "|ent|" + sujet.titre.ljust(taille_max) + "|ff|" + cle)

        msg = self.cfg_info.accueil_aide + "\n\n"
        if not sujets_lire:
            msg += "|att|Aucun sujet disponible.|ff|"
        else:
            msg += "Sujets disponibles :\n\n  " + "\n  ".join(sorted(
                    sujets_lire))
        return msg

    def joueur_connecte(self, joueur):
        """On avertit le joueur s'il y a de nouvelles versions."""

        versions = self.versions.afficher_dernieres_pour(joueur, lire=False)
        if versions:
            joueur << "|vrc|De nouvelles modifications ont été apportées. " \
                    "Pour les consulter, utilisez\nla commande |ff|" \
                    "|cmd|versions|ff||vrc|.|ff|"

        annonces = self.annonces.afficher_dernieres_pour(joueur, lire=False)
        if annonces:
            joueur << "|vrc|De nouvelles annonces ont été créées. " \
                    "Pour les consulter, utilisez\nla commande |ff|" \
                    "|cmd|annonces|ff||vrc|.|ff|"

        # Feuilles de route
        elts = [r for r in self.roadmaps if joueur not in r.joueurs_ayant_lu]
        if elts:
            joueur << "|vrc|La feuille de route a été mise à jour. " \
                    "Pour la consulter, utilisez\nla commande " \
                    "|cmd|roadmap|vrc|.|ff|"


    def entree_tip(self, personnage, cle):
        """Retourne True si le personnage a lue la tip, False sinon."""
        liste = self.tips.personnages.get(personnage, [])
        return cle in liste

    def noter_tip(self, personnage, cle):
        """Note la tip cle comme lue pour le personnage."""
        liste = self.tips.personnages.get(personnage, [])
        if cle not in liste:
            liste.append(cle)

        self.tips.personnages[personnage] = liste

    def get_reboot(self):
        """Création ou retour du reboot actuel."""
        if self.reboot:
            return self.reboot

        self.reboot = Reboot()
        return self.reboot

    def programmer_reboot(self, secondes):
        """Programme un reboot."""
        anciennes_versions = []
        if self.reboot:
            anciennes_versions = list(self.reboot.versions)
            self.reboot.actif = False

        self.reboot = Reboot()
        for version in anciennes_versions:
            self.reboot.versions.append(version)

        self.reboot.programmer(secondes)

    def surveiller_memoire(self):
        """Surveille la mémoire, programme un reboot si besoin."""
        if psutil:
            importeur.diffact.ajouter_action("ver_mem", 60, self.surveiller_memoire)
            mem = psutil.virtual_memory()
            pourcentage = mem.percent
            if pourcentage > 90:
                # Shutdown immédiat, sans appel
                self.programmer_reboot(180)
            elif pourcentage > 80 and self.reboot is None:
                self.programmer_reboot(2 * 60 * 60)

    def detruire(self):
        """Destruction du module."""
        BaseModule.detruire(self)
        if self.reboot:
            for version in self.reboot.versions:
                self.versions.append(version)
