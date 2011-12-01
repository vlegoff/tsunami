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


"""Fichier contenant la classe Niveaux, détaillée plus bas."""

from math import sqrt

class Niveaux:
    
    """Classe contenant les mécanismes propres à la manipulation de niveaux.
    
    Elle se charge de calculer la grille d'expérience et les données
    variables d'un niveau à l'autre.
    
    Elle ne doit pas être instanciée pour manipuler ses données.
    En revanche, le module en charge (perso) doit lui donner
    les informations dont elle a besoin pour calculer certaines valeurs.
    
    """
    nb_niveaux = None
    xp_min = None
    xp_max = None
    grille_xp = []
    nb_points_quetes = None
    
    @classmethod
    def calculer_grille(cls):
        """Calcul la grille d'expérience.
        
        Le premier niveau est le 0. Il n'a besoin que de 0 xp.
        Le second niveau (1) a besoin de cls.xp_min XP pour se valider.
        Le dernier niveau cls.nb_niveaux a besoin de cls.xp_max pour
        se valider.
        Les niveaux intermédiaires sont calculés en fonction.
        Enfin, les points de quêtes sont répartis en fonction de
        leur nombre selon un calcul qui peut être ajusté ici.
        
        """
        grille = [
            (1, cls.xp_min),
        ]
        marge = sqrt(cls.xp_max - cls.xp_min)
        for etape in range(2, cls.nb_niveaux):
            coef = 2 - (1 - etape / cls.nb_niveaux) * 0.4
            xp = ((etape / cls.nb_niveaux) ** coef * marge) ** 2
            xp += cls.xp_min * (1 - etape / cls.nb_niveaux)
            grille.append((etape, xp))
        
        grille.append((cls.nb_niveaux, cls.xp_max))
        cls.grille_xp = grille