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


"""Package contenant la commande 'where'.

"""

from primaires.interpreteur.commande.commande import Commande

class CmdWhere(Commande):
    
    """Commande 'where'.
    
    """
    
    def __init__(self):
        """Constructeur de la commande"""
        Commande.__init__(self, "where", "where")
        self.groupe = "administrateur"
        self.schema = ""
        self.aide_courte = "affiche la position des joueurs"
        self.aide_longue = \
            "Cette commande permet d'afficher la liste des joueurs connectés " \
            "avec leur position dans l'univers, sous la forme zone:mnemonic."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation de la commande"""
        joueurs = type(self).importeur.connex.joueurs_connectes
        liste_affichee = []
        if not joueurs:
            personnage.envoyer("Aucun joueur ne semble être présent, mais " \
                    "qui es-tu alors ?")
        else:
            res = "+" + "-" * 22 + "+" + "-" * 17 + "+\n"
            res += "|" + "|tit|Joueurs|ff| ".rjust(31) + "|"
            res += " |tit|Positions|ff|".ljust(26) + "|\n"
            res += "+" + "-" * 22 + "+" + "-" * 17 + "+\n"
            for joueur in joueurs:
                ident = "|rgc|" + joueur.salle.zone + "|ff|:|vrc|" 
                ident += joueur.salle.mnemonic + "|ff|"
                ident = ident.ljust(33)
                nom = joueur.nom.rjust(20)
                res += "| " + nom + " | " + ident + " |\n"
            res += "+" + "-" * 22 + "+" + "-" * 17 + "+"
            personnage << res
