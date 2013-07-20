# -*-coding:Utf-8 -*

# Copyright (c) 2013 LE GOFF Vincent
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


"""Fichier contenant l'ordre LongDeplacer."""

from secondaires.navigation.equipage.ordres.deplacer import Deplacer
from ..ordre import *

class LongDeplacer(Ordre):

    """Ordre combinant plusieurs ordres de déplacement."""

    cle = "long_deplacer"
    def __init__(self, matelot, navire, *directions):
        Ordre.__init__(self, matelot, navire)
        self.directions = directions

    def choisir_matelot(self, matelots):
        """Un matelot de substitution ne peut pas être trouvé pour cet ordre."""
        raise OrdreSansSubstitution

    def calculer_empechement(self):
        """Retourne une estimation de l'empêchement du matelot."""
        if self.matelot.cle_etat:
            return 100
        else:
            return 0

    def executer(self):
        """Exécute l'ordre : déplace le matelot."""
        for i, direction in enumerate(self.directions):
            deplacement = Deplacer(self.matelot, self.navire, direction)
            deplacement.executer()
            if i < len(self.directions) - 1:
                yield 0.2
