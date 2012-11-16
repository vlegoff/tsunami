# -*-coding:Utf-8 -*

# Copyright (c) 2012 LE GOFF Vincent
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


"""Fichier contenant la fonction duree."""

from primaires.scripting.fonction import Fonction

class ClasseFonction(Fonction):
    
    """Retourne la durée de l'affection du personnage."""
    
    @classmethod
    def init_types(cls):
        cls.ajouter_types(cls.duree_personnage, "Personnage", "str")
        cls.ajouter_types(cls.duree_salle, "Salle", "str")
    
    @staticmethod
    def duree_personnage(personnage, affection):
        """Retourne la durée de l'affection du personnage.
        
        Si le personnage n'est pas affecté par l'affection précisée, cette
        fonction retourne 0.
        
        """
        cle = affection.lower()
        affection = personnage.affections.get(cle)
        if affection is None:
            return 0
        
        return affection.duree
    
    @staticmethod
    def duree_salle(salle, affection):
        """Retourne la durée de l'affection de la salle.
        
        Si la salle n'est pas affectée par l'affection précisée, cette
        fonction retourne 0.
        
        """
        cle = affection.lower()
        affection = salle.affections.get(cle)
        if affection is None:
            return 0
        
        return affection.duree
