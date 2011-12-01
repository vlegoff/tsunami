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


"""Ce fichier contient la classe Objet, détaillée plus bas."""

from abstraits.id import ObjetID

class Objet(ObjetID):
    
    """Cette classe contient un Objet issu d'un prototype.
    Pour rappel, un prototype définit une suite d'action propre au type de
    l'objet, ainsi que des attributs génériques. Les administrateurs en
    charge de l'univers créent des prototypes et sur ce prototype (qui est
    une sorte de modèle), des objets sont créés.
    L'objet peut avoir des attributs se distinguant du prototype mais
    conserve une référence vers son prototype.
    
    Petite subtilité : la méthode __getattr__ a été redéfinie pour qu'il
    ne soit pas nécessaire de faire :
    >>> self.prototype.nom
    pour accéder au nom de l'objet.
    >>> self.nom
    suffit. La méthode va automatiquement chercher l'attribut dans
    'self.prototype' si l'attribut n'existe pas. Cela veut dire que si
    vous faites :
    >>> self.nom = "un autre nom"
    vous modifiez le nom de l'objet, sans modifier le prototype
    (le prototype ne doit pas être modifié depuis l'objet). Le nom de
    l'objet changera donc et sera différent de celui du prototype, le
    temps de la durée de vie de l'objet. Pour que :
    >>> self.nom
    fasse de nouveau référence au nom du prototype, il est conseillé de
    supprimer le nom de l'objet :
    >>> del self.nom
    Ce mécanisme permet une assez grande flexibilité. Si par exemple vous
    modifiez la description du prototype, tous les objets créés sur ce
    prototype, (ceux créés comme ceux prochainement créés), seront affectés
    par ce changement, sauf si ils définissent une description propre.
    
    """
    
    groupe = "objets"
    sous_rep = "objets/objets"
    def __init__(self, prototype):
        """Constructeur de l'objet"""
        ObjetID.__init__(self)
        self.prototype = prototype
        if prototype:
            self.identifiant = prototype.cle + "_" + str(
                    prototype.no)
            prototype.no += 1
            prototype.objets.append(self)
            
            # On copie les attributs propres à l'objet
            # Ils sont disponibles dans le prototype, dans la variable
            # _attributs
            # C'est un dictionnaire contenant en clé le nom de l'attribut
            # et en valeur le constructeur de l'objet
            for nom, val in prototype._attributs.items():
                setattr(self, nom, val.construire(self))
    
    def __getnewargs__(self):
        return (None, )
    
    def __getattr__(self, nom_attr):
        """Si le nom d'attribut n'est pas trouvé, le chercher
        dans le prototype
        
        """
        return getattr(self.prototype, nom_attr)
    
    def __str__(self):
        return self.nom_singulier
    
    def detruire(self):
        """Destruction de l'objet"""
        if self in self.prototype.objets:
            self.prototype.objets.remove(self)
        ObjetID.detruire(self)

ObjetID.ajouter_groupe(Objet)