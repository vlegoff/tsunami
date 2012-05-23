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


"""Ce fichier contient la classe Periode, détaillée plus bas."""

from abstraits.obase import BaseObj
from .element import Element

class Periode(BaseObj):
    
    """Classe décrivant une période de temps (cycle pour une plante).
    
    Une période possède :
    nom -- le nom de la période
    nom_singulier, nom_pluriel, etat_singulier, etat_pluriel
        Noms et états du végétal pour la période
    plante -- le prototype de plante définissant la période
    fin -- un tuple (jour, mois) représentant la fin du cycle
    variation -- un nombre de jours représentant la variation aléatoire [1]
    elements -- une liste représentant les éléments récoltables
                à cette période [2]
    
    [1] La première période présente dans la liste d'un prototype est
        toujours choisie au début de l'année. Si plus d'une période
        est définie, la première étape laisse la place à la suivante
        au jour précisé plus ou moins la variation optionnelle.
        Cela permet d'introduire une donnée aléatoire faisant
        qu'un plan de maïs pourra être récoltable dans des dates
        approximatives. Notez qu'après la dernière étape définie,
        la plante revient en étape 0 (la première).
    
    [2] La liste des éléments est constituée d'objets Element (voir
        la classe définie dans .element.py).
    
    """
    
    def __init__(self, nom, cycle):
        """Constructeur de la période."""
        BaseObj.__init__(self)
        self.nom = nom
        self.cycle = cycle
        self.nom_singulier = "une plante"
        self.nom_pluriel = "plantes"
        self.etat_singulier = "fleurit ici"
        self.etat_pluriel = "fleurient ici"
        self.fin = (0, 0)
        self.variation = 0
        self.elements = []
    
    def __getnewargs__(self):
        return ("", None)
    
    def __repr__(self):
        return "<période {} ({}-{} variation={})>".format(self.nom,
                self.fin[0] + 1, self.fin[1] + 1, self.variation)
    
    def __str__(self):
        return self.nom
    
    @property
    def date_fin(self):
        """Retourne la date de fin grâce aux informations du module temps."""
        return "{} du {}".format(importeur.temps.cfg.noms_jours[ \
                self.fin[0]], importeur.temps.cfg.mois[self.fin[1]][0])
    
    @property
    def plante(self):
        return self.cycle and self.cycle.plante or None
    
    def ajouter_element(self, objet, quantite):
        """Ajout d'un élément.
        
        Si on cherche à ajouter un élément existant (l'objet est défini
        dans un autre élément), une exception ValueError est levée.
        
        """
        for elt in self.elements:
            if elt.objet is objet:
                raise ValueError("l'élément {} existe déjà".format(elt))
        
        elt = Element(self.plante, self, objet, quantite)
        self.elements.append(elt)
        return elt
    
    def get_element(self, cle):
        """Retourne l'élément dont l'objet a la clé indiquée."""
        for elt in self.elements:
            if elt.objet.cle == cle:
                return elt
        
        raise ValueError("la clé d'élément {} est introuvable".format(cle))
    
    def supprimer_element(self, cle):
        """Supprime l'élément."""
        for elt in list(self.elements):
            if elt.objet.cle == cle:
                self.elements.remove(elt)
                elt.detruire()
                return
        
        raise ValueError("aucun élément ne porte la clé {}".format(cle))
    
    def detruire(self):
        """Destruction de la période."""
        for elt in self.elements:
            elt.detruire()
        
        BaseObj.detruire(self)
