# -*-coding:Utf-8 -*

# Copyright (c) 2010-2017 LE GOFF Vincent
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


"""Ce module contient la classe Neige, détaillée plus bas."""

from primaires.affection.salle import AffectionSalle

class Neige(AffectionSalle):

    """Affection définissant la neige dans une salle."""

    def __init__(self):
        AffectionSalle.__init__(self, "neige")
        self.resume = "les flocons de neige dans une salle"
        self.force_max = 60
        self.duree_max = 120
        self.visible = True
        self.tick_actif = False

    def __getnewargs__(self):
        return ()

    def dec_duree(self, affection, duree=1):
        """Manipule l'affection concrète quand la durée se décrémente.

        Cette fonction est appelée pour modifier une affection concrète
        (avec durée, force et s'appliquant à un affecté) quand la
        durée est censée se décrémenter. Ici, la neige fond au fur
        et à mesure que la durée diminue.

        """
        if affection.duree == 0:
            return

        if affection.affecte.zone.temperature < 1:
            return

        fact_dec = (affection.duree - duree) / affection.duree
        duree = affection.duree - duree
        force = affection.force * fact_dec
        force = self.equilibrer_force(force)
        duree = self.equilibrer_duree(duree)
        affection.force = force
        affection.duree = duree
        self.verifier_validite(affection)
        if affection.force <= 0:
            affection.detruire()

    def message(self, affection):
        """Retourne le message de la salle affectée par la neige."""
        messages = (
            (2, "Un fin tapis de neige recouvre le sol."),
            (5, "Une fine couche de neige recouvre le sol."),
            (10, "Une couche de neige d'un bon pied recouvre le sol."),
            (20, "Une épaisse couche de neige recouvre le sol."),
            (40, "La couche de neige épaisse est parsemée de hautes congères."),
        )

        for t_force, message in messages:
            if affection.force <= t_force:
                return message

        return messages[-1][1]

    def moduler(self, affection, duree, force):
        """Module, c'est-à-dire ici ajoute simplement les forces et durées."""
        force = self.equilibrer_force(affection.force + force)
        duree = self.equilibrer_duree(affection.duree + duree)
        affection.duree = duree
        affection.force = force
        self.verifier_validite(affection)

    def verifier_validite(self, affection):
        """Vérifie la validité de l'affection.

        Si la salle est passée en intérieur ou en un terrain inapproprié,
        par exemple, l'affection doit se détruire.

        """
        if not affection.affecte.peut_affecter("neige"):
            affection.force = 0
            affection.duree = 0

    def message_detruire(self, affection):
        """Destruction de l'affection de salle."""
        return "La neige fond, ne laissant que quelques flaques au sol."

    def programmer_destruction(self, affection):
        """Programme la destruction de la neige.

        D'etruit les bonhommes de neige de la salle.

        """
        AffectionSalle.programmer_destruction(self, affection)
        affection.affecte.supprimer_bonhommes_neige()
