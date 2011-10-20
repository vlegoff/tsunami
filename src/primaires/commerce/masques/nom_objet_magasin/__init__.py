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


"""Fichier contenant le masque <id_objet_magasin>."""

from primaires.interpreteur.masque.masque import Masque
from primaires.interpreteur.masque.fonctions import *
from primaires.interpreteur.masque.exceptions.erreur_validation \
        import ErreurValidation
from primaires.format.fonctions import contient

class NomObjetMagasin(Masque):
    
    """Masque <nom_objet_magasin>.
    On attend le nom d'un objet en vente dans la salle où se trouve le joueur.
    
    """
    
    nom = "nom_objet_magasin"
    nom_complet = "nom d'un objet en vente"
    
    def init(self):
        """Initialisation des attributs du masque"""
        self.objet = None
    
    def repartir(self, personnage, masques, commande):
        """Répartition du masque."""
        nom_objet = liste_vers_chaine(commande)
        if not nom_objet:
            raise ErreurValidation( \
                "Vous devez préciser le nom d'un objet.", False)
        
        self.a_interpreter = nom_objet
        commande[:] = []
        masques.append(self)
        return True
    
    def valider(self, personnage, dic_masques):
        """Validation du masque"""
        Masque.valider(self, personnage, dic_masques)
        nom_objet = self.a_interpreter
        magasin = personnage.salle.magasin
        objet = None
        for o in magasin.liste_objets:
            if contient(o.nom_singulier, nom_objet):
                objet = o
                break
        for p in magasin.liste_pnjs:
            if contient(p.nom_singulier, nom_objet):
                objet = p
                break
        if objet is None:
            raise ErreurValidation( \
                "|err|L'objet demandé n'est pas en vente.|ff|")
        else:
            self.objet = objet
            return True
