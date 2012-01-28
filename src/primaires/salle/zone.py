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


"""Fichier contenant la classe Zone, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.liste_id import ListeID

class Zone(ObjetID):
    
    """Classe représentant une zone.
    
    Une zone est un ensemble de salle. Certaines informations génériques
    sont conservés dans la zone plutôt que dans chaque salle.
    
    """
    
    groupe = "zones"
    sous_rep = "zones"
    
    def __init__(self, cle):
        """Constructeur de la zone."""
        ObjetID.__init__(self)
        self.cle = cle
        self.salles = ListeID(self)
        self.ouverte = True
    
    def __getnewargs__(self):
        return ("", )
    
    def __repr__(self):
        return "zone {}".format(repr(self.cle))
    
    def __str__(self):
        return self.cle
    
    @property
    def fermee(self):
        return not self.ouverte
    
    def ajouter(self, salle):
        """Ajoute une salle à la zone."""
        if salle not in self.salles:
            self.salles.append(salle)
    
    def retirer(self, salle):
        """Retire la salle de la zone."""
        if salle in self.salles:
            self.salles.remove(salle)


ObjetID.ajouter_groupe(Zone)