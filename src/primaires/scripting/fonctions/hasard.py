# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
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


"""Fichier contenant la fonction hasard."""

from random import random, choice

from primaires.scripting.fonction import Fonction
from primaires.scripting.instruction import ErreurExecution

class ClasseFonction(Fonction):

    """Retourne vrai ou faux aléatoirement.

    Cette fonction peut être utilisée associée à une condition."""

    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.hasard, "Fraction")
        cls.ajouter_types(cls.choix_chaine, "str")

    @staticmethod
    def hasard(probabilite):
        """Retourne vrai ou faux en fonction de la probabilité.

        La probabilité entrée doit être un entier entre 1 et 100.
        Un test avec une probabilité de 100 sera toujours vrai.
        Un test avec une probabilité de 50 aura 1/2 chances d'être vrai.
        Un test avec une probabilité de 0 sera toujours faux.

        """
        probabilite /= 100
        probabilite = float(probabilite)
        chance = random()
        return chance < probabilite

    @staticmethod
    def choix_chaine(chaine):
        """Choisit un des éléments de la chaîne séparé par |.

        La chaîne est sous la forme de plusieurs éléments séparés
        par |. Par exemple:

            cle = choisir("branche|tronc|racine|tige")

        Dans la variable 'cle' se trouvera soit "branche", soit
        "tronc", soit "racine", soit "tige".

        """
        if not chaine:
            raise ErreurExecution("la chaîne précisée est vide")

        chaines = chaine.split("_b_")
        return choice(chaines)
