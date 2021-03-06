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


"""Fichier contenant la fonction recette."""

from primaires.format.fonctions import supprimer_accents
from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne la recette si trouvée."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.recette, "Personnage", "str", "list")
        cls.ajouter_types(cls.recette, "Personnage", "str", "list", "str")

    @staticmethod
    def recette(personnage, cle_guilde, ingredients, nom=""):
        """Cherche et fabrique la recette si trouvée.

        Si la recette n'est pas trouvée dans la guilde, retourne
        une liste vide. Sinon, retourne la liste des objets nouvellement
        créés.

        Paramètres à préciser :

          * personnage : le personnage voulant fabriquer la recette
          * cle_guilde : la clé de la guilde (une chaîne)
          * ingredients : la liste des ingrédients (liste d'objets)
          * nom (optionnel) : le nom de la recette

        Le dernier paramètre est utile si la guilde créé comporte
        potentiellement plusieurs recettes utilisant les mêmes
        ingrédients.

        Exemple d'utilisation :

          resultats = recette(personnage, "forgerons", ingredients)
          si resultats:
              # 'resultats' est une liste non vide d'objets
              pour chaque objet dans resultats:
                  poser salle objet

        """
        nom = supprimer_accents(nom).lower()
        cle_guilde = cle_guilde.lower()
        if cle_guilde not in importeur.crafting.guildes:
            raise ErreurExecution("La guilde {} n'existe pas".format(
                    repr(cle_guilde)))

        guilde = importeur.crafting.guildes[cle_guilde]

        if personnage not in guilde.membres:
            return []

        # On ne cherche que les rangs parents
        rangs_parents = guilde.membres[personnage].rang.rangs_parents

        for rang in guilde.rangs:
            if rang not in rangs_parents:
                continue

            for recette in rang.recettes:
                if nom == "" or nom == supprimer_accents(
                        recette.nom).lower():
                    if recette.peut_faire(personnage, ingredients):
                        return recette.creer_resultat(personnage, ingredients)

        return []
