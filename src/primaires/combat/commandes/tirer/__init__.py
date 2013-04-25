# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Package contenant la commande 'tirer'.

"""

from corps.aleatoire import varier
from corps.fonctions import lisser
from primaires.interpreteur.commande.commande import Commande

class CmdTirer(Commande):

    """Commande 'tirer'.

    """

    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "tirer", "shoot")
        self.nom_categorie = "combat"
        self.schema = "(<personnage_present>)"
        self.aide_courte = "décharge une arme de jet"
        self.aide_longue = \
            "Cette commande permet de décharger une arme de jet " \
            "que vous tenez sur une cible, présente ou non dans la " \
            "salle. Si vous précisez un argument à la commande, c'est " \
            "un nom de personnage ou créature présente dans la salle " \
            "où vous vous trouvez. Si vous ne précisez rien, la " \
            "cible que vous avez auparavant sélectionné avec les " \
            "commandes %scruter% et %viser% sera sélectionnée. Dans " \
            "ce dernier cas, vous devrez disposer d'un angle de " \
            "tir correct : le projectile qui traversera plusieurs " \
            "salles doit être droit."

    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        arme_de_jet = None
        for objet in personnage.equipement.equipes:
            if objet.est_de_type("arme de jet"):
                arme_de_jet = objet

        if arme_de_jet is None:
            personnage << "|err|Vous n'équipez aucune arme de jet.|ff|"
            return

        if arme_de_jet.projectile is None:
            personnage << "|err|Cette arme n'est pas chargée.|ff|"
            return

        # Sélection de la cible
        if dic_masques["personnage_present"]:
            cible = dic_masques["personnage_present"].personnage
        else:
            cible = importeur.combat.cible.get(personnage)
            if cible is None or (hasattr(cible, "connecte") and not cible.connecte):
                personnage << "|err|Vous ne visez personne actuellement.|ff|"
                return

        chemin = None
        if personnage.salle is not cible.salle:
            chemin = personnage.salle.trouver_chemin(cible.salle)
            if chemin is None or not chemin.droit:
                personnage << "|err|Vous ne disposez pas d'un bon angle de tir.|ff|"
                return

        # 1. On fait partir le projectile
        projectile = arme_de_jet.projectile
        personnage << lisser("Vous libérez la tension de {}.".format(
                arme_de_jet.get_nom()))
        personnage.salle.envoyer(lisser("{{}} libère la tension de {}.".format(
                arme_de_jet.get_nom())), personnage)
        arme_de_jet.projectile = None

        # 2. On parcourt les salles adjacentes, si il y en a
        if chemin:
            for sortie in chemin:
                origine = sortie.parent
                destination = sortie.salle_dest
                direction = sortie.nom_complet
                if origine is personnage.salle:
                    origine.envoyer("{} part en sifflant vers {}.".format(
                            projectile.get_nom(), direction))
                else:
                    origine.envoyer("{} passe en sifflant vers {}.".format(
                            projectile.get_nom(), direction))

                if destination is cible.salle:
                    destination.envoyer("{} arrive en sifflant dans les " \
                            "airs.".format(projectile.get_nom()))
        else:
            # personnage et  ible sont dans la même salle
            personnage.salle.envoyer("{} part en sifflant dans l'air.".format(
                projectile.get_nom()))

        # 3. On voit si on atteint on manque la cible
        fact_p = varier(personnage.stats.agilite, 20) / 150
        fact_p += (1 - personnage.poids / personnage.poids_max) / 3
        fact_c = varier(cible.stats.agilite, 20) / 150
        fact_c += (1 - cible.poids / cible.poids_max) / 3
        if fact_p > fact_c:
            personnage << "Touché !"
            importeur.objet.supprimer_objet(projectile.identifiant)
        else:
            personnage << "Pas touché"
            personnage.salle.objets_sol.ajouter(projectile)