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


"""Fichier contenant la classe ModeleNavire, détaillée plus bas."""

from abstraits.id import ObjetID
from bases.collections.dict_valeurs_id import DictValeursID
from bases.collections.liste_id import ListeID

class ModeleNavire(ObjetID):
    
    """Classe représentant un modèle de navire ou une embarcation.
    
    Les modèles définissent des informations communes à plusieurs navires
    (une barque, par exemple, sera construite sur un seul modèle mais
    plusieurs navires seront formés sur ce modèle).
    
    """
    
    groupe = "modele_navire"
    sous_rep = "navires/modeles"
    def __init__(self, cle):
        """Constructeur du modèle."""
        ObjetID.__init__(self)
        self.cle = cle
        self.vehicules = ListeID(self)
        self.salles = DictValeursID(self)
    
    def __getnewargs__(self):
        return ("", )
    
    def detruire(self):
        """Se détruit, ainsi que les véhicules créés sur ce modèle."""
        for vehicule in list(self.vehicules):
            vehicule.detruire()
        
        ObjetID.detruire(self)


ObjetID.ajouter_groupe(ModeleNavire)
