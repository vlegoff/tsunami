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


"""Fichier contenant la classe PNJ, détaillée plus bas."""

import sys

from abstraits.obase import BaseObj
from primaires.perso.personnage import Personnage
from primaires.scripting.exceptions import InterrompreCommande

class PNJ(Personnage):

    """Classe représentant un PNJ, c'est-à-dire un personnage virtuel.

    Ce personnage est géré par l'univers et n'est pas connecté, à
    la différence d'un joueur.

    """

    enregistrer = True
    def __init__(self, prototype, salle=None):
        """Constructeur du PNJ"""
        Personnage.__init__(self)
        self._nom = ""
        self.prototype = prototype
        self.salle = salle
        self.salle_origine = salle
        self.controle_par = None
        self.instance_connexion = None
        if salle:
            salle.pop_pnj(self)

        if prototype:
            prototype.no += 1
            self.identifiant = prototype.cle + "_" + str(
                    prototype.no)
            prototype.pnj.append(self)

            # On copie les attributs propres à l'objet
            # Ils sont disponibles dans le prototype, dans la variable
            # _attributs
            # C'est un dictionnaire contenant en clé le nom de l'attribut
            # et en valeur le constructeur de l'objet
            for nom, val in prototype._attributs.items():
                setattr(self, nom, val.construire(self))

            # On force l'écriture de la race
            self.race = prototype.race
            for stat in prototype.stats:
                t_stat = getattr(self.stats, "_{}".format(stat.nom))
                t_stat.defaut = stat.defaut
                t_stat.courante = stat.defaut
            self.stats.restaurer()
            self.lier_equipement(prototype.squelette)
            self.genre = prototype.genre
            self.talents.update(prototype.talents)
            self.sorts.update(prototype.sorts)

            # Copie de l'équipement
            for membre, p_objet in prototype.equipement.items():
                if self.equipement.squelette.a_membre(membre):
                    objet = importeur.objet.creer_objet(p_objet)
                    self.equipement.equiper_objet(membre, objet)

            # On force l'écriture du niveau
            self.niveau = prototype.niveau

    def __getnewargs__(self):
        return (None, )

    def __getattr__(self, nom_attr):
        """Si le nom d'attribut n'est pas trouvé, le chercher
        dans le prototype

        """
        if nom_attr == "prototype":
            return object.__getattr__(self, nom_attr)
        else:
            try:
                return Personnage.__getattr__(self, nom_attr)
            except AttributeError:
                return getattr(self.prototype, nom_attr)

    def __repr__(self):
        return "<pnj {}>".format(self.identifiant)

    def _get_nom(self):
        """Retourne le nom singulier définit dans le prototype.

        Toutefois, si le nom est définit dans le PNJ lui-même
        (l'attribut _nom n'est pas vide), retourne celui-ci.

        """
        nom = self._nom
        if not nom:
            nom = self.prototype.nom_singulier

        return nom
    def _set_nom(self, nouveau_nom):
        """Ecrit le nom dans self._nom.

        Note contextuelle : si le nouveau nom est vide, le nom redeviendra
        le nom singulier du prototype.

        """
        self._nom = nouveau_nom
    nom = property(_get_nom, _set_nom)

    def _set_race(self, race):
        self._race = race
    race = property(Personnage._get_race, _set_race)

    def _get_contextes(self):
        return self.controle_par and self.controle_par.contextes or \
                None
    def _set_contextes(self, contextes):
        pass
    contextes = property(_get_contextes, _set_contextes)

    def _get_alias(self):
        alias = {}
        if self.controle_par:
            return self.controle_par.alias
        return alias
    def _set_alias(self, alias):
        pass
    alias = property(_get_alias, _set_alias)

    def _get_langue_cmd(self):
        if self.controle_par:
            return self.controle_par.langue_cmd
        else:
            return "francais"
    def _set_langue_cmd(self, langue):
        pass
    langue_cmd = property(_get_langue_cmd, _set_langue_cmd)

    def _get_distinction_audible(self):
        return self.get_distinction_audible()
    def _set_distinction_audible(self, distinction):
        pass
    distinction_audible = property(_get_distinction_audible,
            _set_distinction_audible)

    def envoyer(self, msg, *personnages, **kw_personnages):
        """Envoie un message"""
        if self.controle_par:
            self.controle_par.envoyer(msg, *personnages,
                    **kw_personnages)

    def get_nom_etat(self, personnage, nombre=1):
        """Retourne le nom et l'état (singulier ou pluriel)."""
        if nombre == 1:
            nom = self.get_nom_pour(personnage) + " "
            if self.etats:
                nom += Personnage.get_etat(self)
            else:
                nom += self.etat_singulier
            return nom
        else:
            return str(nombre) + " " + self.nom_pluriel + " " + \
                    self.etat_pluriel

    def get_nom_pour(self, personnage, retenu=True):
        """Retourne le nom pour le personnage passé en paramètre."""
        if retenu:
            noms = importeur.hook["pnj:nom"].executer(self, personnage)
            if any(noms):
                return noms[0]

        return self.nom_singulier

    def ajout_description_pour_imm(self):
        return " |vr|[{}]|ff|".format(self.identifiant)

    def est_connecte(self):
        return True

    def gagner_xp(self, niveau=None, xp=0, retour=True):
        """Fait gagner de l'XP au personnage."""
        ancien_niveau = self.niveau
        res = Personnage.gagner_xp(self, niveau, xp, retour)
        importeur.hook["pnj:gagner_xp"].executer(self, niveau, xp, retour)
        if self.niveau > ancien_niveau:
            importeur.hook["pnj:gagner_niveau"].executer(self, self.niveau)

        return res

    def mourir(self, adversaire=None, recompenser=True):
        """La mort d'un PNJ signifie sa destruction."""
        try:
            self.script["meurt"]["avant"].executer(pnj=self, salle=self.salle,
                    adversaire=adversaire)
        except InterrompreCommande:
            Personnage.mourir(self, adversaire=adversaire, recompenser=recompenser)
        else:
            Personnage.mourir(self, adversaire=adversaire, recompenser=recompenser)
            self.script["meurt"]["apres"].executer(pnj=self, salle=self.salle,
                    adversaire=adversaire)
            cadavre = importeur.objet.creer_objet(importeur.objet.prototypes[
                    "cadavre"])
            cadavre.pnj = self.prototype
            self.salle.objets_sol.ajouter(cadavre)

        importeur.hook["pnj:meurt"].executer(self, adversaire)

        # Gain d'XP
        if adversaire and self.gain_xp and recompenser:
            xp = importeur.perso.gen_niveaux.grille_xp[self.niveau][1]
            xp = xp * self.gain_xp / 100
            adversaire.gagner_xp("combat", xp)

        importeur.pnj.supprimer_PNJ(self.identifiant)

    @property
    def nom_unique(self):
        return self.identifiant

    @property
    def nom_etat_singulier(self):
        return self.get_nom_etat(None, 1)

    def get_distinction_audible(self):
        return self.nom_singulier

    def tick(self):
        """Méthode appelée à chaque tick."""
        Personnage.tick(self)
        try:
            self.script["tick"].executer(pnj=self)
        except Exception:
            pass

        importeur.hook["pnj:tick"].executer(self)

    def regarder(self, personnage):
        """personnage regarde self."""
        self.script["regarde"]["avant"].executer(personnage=personnage,
                pnj=self)
        Personnage.regarder(self, personnage)
        self.script["regarde"]["après"].executer(personnage=personnage,
                pnj=self)

    def detruire(self):
        """Destruction du PNJ."""
        self.decontroller()
        Personnage.detruire(self)
        if self in self.prototype.pnj:
            self.prototype.pnj.remove(self)

        if self.salle_origine:
            self.salle_origine.det_pnj(self)

    def decontroller(self):
        """Arrête de contrôler self."""
        if self.controle_par:
            try:
                contexte = \
                    self.controle_par.contextes.get_contexte_par_unom(
                    "ctrl_pnj(" + self.identifiant + ")")
            except KeyError:
                pass
            else:
                self.controle_par.contextes.retirer(contexte)
                self.controle_par = None
                self.instance_connexion = None

    def reagir_attaque(self, personnage):
        """Réagit à l'attaque."""
        if self.est_vivant():
            self.script["attaque"].executer(personnage=personnage, pnj=self)
            importeur.hook["pnj:attaque"].executer(self, personnage)

    def tuer(self, victime):
        """Le personnage self vient de tuer la victime."""
        self.script["tue"].executer(personnage=victime, pnj=self)

    def noyable(self):
        """Retourne True si le personnage est noyable, False sinon."""
        return False

    def essayer_nage(self, origine, destination):
        """Essaye de nager (un PNJ réussit toujours)."""
        return True

