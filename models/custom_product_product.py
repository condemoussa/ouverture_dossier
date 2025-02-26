# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

#
class ProductTemplate(models.Model):
    _inherit = "product.template"

    localisation = fields.Selection(
        [
            ("interne", "Interne"),
            ("externe", "Externe"),
        ], default="externe",string="Destination"
    )
    sect_activity = fields.Selection(
        [
            ("secteur1", "Solutions Informatiques, Réseaux, Cybersécurité"),
            ("secteur2", "Solutions Énergétiques et Technologies du Bâtiment"),
            ("secteur3", "Solutions de Télécommunication et DATA"),
            ("secteur4", "Solutions Monétiques, Intégrées et Moyens de Paiement"),
            ("secteur5", "Technologies de Défense et Sécurité"),
            ("secteur6", "BTP et Services"),
        ],
        string="Secteur d'activité"
    )












