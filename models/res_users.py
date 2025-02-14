# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

#
class ResUsers(models.Model):
    _inherit = "res.users"

    type_groups = fields.Selection(
        [
            ("type1","Service commercial"),
            ("type2", "Le Contrôleur de Gestion"),
            ("type3", "La Direction Générale"),
            ("type4", "Direction Technique"),
            ("type11", "Direction financière"),
            ("type5", "Direction Commerciale"),
            ("type6", "Service ITC"),
            ("type7", "Service Achat"),
            ("type8", "Service Tresorerie"),
            ("type9", "Gestionnaire stock"),
            ("type10", "Gestionnaire caisse"),
            ("type12", "Service comptable"),
        ],string="Services"
    )
    user_mail = fields.Char("E-Mail")










