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


"""Ce fichier définit le cherchable des prototypes de PNJ."""

from primaires.format.fonctions import supprimer_accents
from primaires.recherche.cherchables.cherchable import Cherchable

class CherchablePrototypePNJ(Cherchable):

    """Classe cherchable pour les prototypes d'objet de l'univers.

    """

    nom_cherchable = "prpnj"
    recherche_par_defaut = "nom"

    def init(self):
        """Méthode d'initialisation.

        C'est ici que l'on ajoute réellement les filtres, avec la méthode
        dédiée.

        """
        self.ajouter_filtre("n", "nom", "nom_singulier", "regex")
        self.ajouter_filtre("l", "cle", "cle", "regex")
        self.ajouter_filtre("r", "race", "nom_race", "regex")
        self.ajouter_filtre("g", "genre", "genre", "chaine")
        self.ajouter_filtre("v", "niveau", "niveau", "nombre")
        self.ajouter_filtre("e", "entrainement", self.entraine_stat, "chaine")

    @property
    def items(self):
        """Renvoie la liste des objets traités"""
        return list(importeur.pnj.prototypes.values())

    @property
    def attributs_tri(self):
        """Renvoie la liste des attributs par lesquels on peut trier"""
        return ["cle", "nom", "race", "niveau"]

    @property
    def colonnes(self):
        """Retourne un dictionnaire des valeurs que l'on peut disposer en
        colonne à l'affichage final, de la forme :
        >>> {nom: attribut/méthode}
        (une colonne peut être remplie par une méthode du cherchable).

        """
        return {
            "nom": "nom_singulier",
            "cle": "cle",
            "race": "nom_race",
            "genre": "genre",
            "niveau": "niveau",
        }

    def entraine_stat(self, prototype, valeur):
        """Permet une recherche sur le type de l'objet.

        Le type spécifié doit être un type valide et existant ;
        si l'objet est de ce type ou d'un de ses fils, il sera
        retourné à la recherche (cette option n'accepte pas les regex).

        """
        valeur = supprimer_accents(valeur).lower()
        for nom_stat in prototype.entraine_stats:
            if supprimer_accents(nom_stat).lower() == valeur:
                return True

        return False

    def colonnes_par_defaut(self):
        """Retourne les colonnes d'affichage par défaut.

        Si une ou plusieurs colonnes sont spécifiés lors de la recherche,
        les colonnes par défaut ne sont pas utilisées.

        Cette méthode doit retourner une liste de nom de colonnes.

        """
        return ("cle", "nom")

    def tri_par_defaut(self):
        """Sur quelle colonne se base-t-on pour trier par défaut ?"""
        return "cle"
