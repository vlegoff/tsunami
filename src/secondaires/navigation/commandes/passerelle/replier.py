# -*-coding:Utf-8 -*

# Copyright (c) 2010 LE GOFF Vincent
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
# 
# * Redistributions of source code must retain the above copyright notice, this
#   raise of conditions and the following disclaimer.
# * Redistributions in binary form must reproduce the above copyright notice,
#   this raise of conditions and the following disclaimer in the documentation
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


"""Fichier contenant le paramètre 'replier' de la commande 'passerelle'."""

from primaires.interpreteur.masque.parametre import Parametre

class PrmReplier(Parametre):
    
    """Commande 'passerelle replier'.
    
    """
    
    def __init__(self):
        """Constructeur du paramètre"""
        Parametre.__init__(self, "replier", "in")
        self.aide_courte = "replie la passerelle présente"
        self.aide_longue = \
            "Cette commande replie la passerelle présente dans la salle où " \
            "vous vous trouvez."
    
    def interpreter(self, personnage, dic_masques):
        """Interprétation du paramètre"""
        salle = personnage.salle
        if not hasattr(salle, "navire") or salle.navire is None or \
                salle.navire.etendue is None:
            personnage << "|err|Vous n'êtes pas sur un navire.|ff|"
            return
        
        navire = salle.navire
        etendue = navire.etendue
        if not hasattr(salle, "passerelle"):
            personnage << "|err|Il n'y a pas de passerelle ici.|ff|"
            return
        
        passerelle = salle.passerelle
        if not passerelle:
            personnage << "|err|Vous ne voyez aucune passerelle ici.|ff|"
            return
        
        if not passerelle.baissee:
            personnage << "|err|Cette passerelle est déjà repliée.|ff|"
        else:
            # On cherche la sortie
            sortie = salle.sorties.get_sortie_par_nom("passerelle")
            dest = sortie.salle_dest
            opp_sortie = None
            for nom, t_sortie in dest.sorties.iter_couple():
                if t_sortie.salle_dest is salle:
                    opp_sortie = t_sortie
                    break
            
            if opp_sortie:
                dest.sorties.supprimer_sortie(opp_sortie.direction)
                dest.enregistrer()
            
            salle.sorties.supprimer_sortie(sortie.direction)
            salle.enregistrer()
            passerelle.baissee = False
            personnage << "Vous repliez {}.".format(passerelle.nom)