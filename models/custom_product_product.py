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












