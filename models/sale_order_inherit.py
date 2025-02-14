# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import UserError
# produit
class SaleOrder(models.Model):
    _inherit = "sale.order"

    def action_confirm(self):

        res = super(SaleOrder, self).action_confirm()
        for order in self:
            if order.offre_physique:  # Vérifie que l'offre physique est activée
                # Récupérer le type de picking (opération de sortie) pour l'entrepôt
                picking_type = self.env['stock.picking.type'].search([('code', '=', 'outgoing')], limit=1)
                if not picking_type:
                    raise ValueError("Aucun type d'opération 'Sortie' trouvé. Vérifiez la configuration de l'entrepôt.")

                # Créer le picking
                self.env['stock.picking'].create({
                    'origin': order.name,
                    'partner_id': order.partner_id.id,
                    'location_id': picking_type.default_location_src_id.id,  # Emplacement source
                    'location_dest_id': order.partner_id.property_stock_customer.id,  # Emplacement client
                    'sale_id': self.id,
                    'picking_type_id': picking_type.id , # Type d'opération
                    'offre_physique' :self.offre_physique
                })
        return res



    #creation de l'ouverture de dossier'
    def create_ouverture_dossier(self):
        self.update({"expres_command": "express5"})
        for order in self:
            if order.type_commd !='comand1':
                self.env['atm.ouverture.dossier'].create({
                    'name': False,  # Numéro de commande
                    'sale_order_id': order.id,  # Référence à la commande de vente
                    'dat_ouverture': fields.Date.today(),  # Date actuelle
                })
            else:
                self.env['atm.ouverture.contrat'].create({
                    'name': False,  # Numéro de commande
                    'sale_order_id': order.id,  # Référence à la commande de vente
                    'dat_ouverture': fields.Date.today(),  # Date actuelle
                })

    def bon_accord(self):
        self.action_confirm()
        self.update({"expres_command":"express2"})

    def bon_commande(self):
        self.action_confirm()
        self.update({"state": "sale","expres_command":"express1"})

    def lettre_attribution(self):
        self.action_confirm()
        self.update({"state": "sale","expres_command":"express3"})

    def contra_travail(self):
        self.action_confirm()
        self.update({"state": "sale", "expres_command": "express4"})

    def send_document_by_email(self):
        for record in self:
            # Vérifier si un document est attaché
            if not record.offre_physique:
                raise UserError("Aucun document n'est attaché à cette commande.")

            # Vérifier si un client est lié et possède une adresse e-mail
            if not record.partner_id or not record.partner_id.email:
                raise UserError("Le client associé n'a pas d'adresse e-mail.")

            # Récupérer l'adresse e-mail du client
            email_to = record.partner_id.email

            # Créer l'attachement
            attachment = self.env['ir.attachment'].create({
                'name': 'Devis.pdf',
                'type': 'binary',
                'datas': record.offre_physique,
                'res_model': self._name,
                'res_id': record.id,
                'mimetype': 'application/pdf',  # Changez si nécessaire
            })

            # Préparer l'e-mail
            mail_values = {
                'subject': f"Document lié à la commande {record.name}",
                'body_html': f"""
                    <p>Bonjour {record.partner_id.name},</p>
                    <p>Veuillez trouver ci-joint le document lié à la commande <strong>{record.name}</strong>.</p>
                    <p>Cordialement,</p>
                """,
                'email_from': self.env.user.email or "noreply@example.com",
                'email_to': email_to,  # E-mail du client
                'attachment_ids': [(4, attachment.id)],  # Associer l'attachement
                'auto_delete': False,  # Ne pas supprimer l'e-mail automatiquement
            }

            # Créer et envoyer l'e-mail
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()

    def action_quotation_send(self):
        # Appel à la méthode originale pour conserver son comportement par défaut
        res = super(SaleOrder, self).action_quotation_send()

        # Appel de la méthode `send_document_by_email` pour envoyer le document
        for record in self:
            if record.offre_physique:
                # Vérifier si le client a un e-mail
                if not record.partner_id or not record.partner_id.email:
                    raise UserError(f"Le client de la commande {record.name} n'a pas d'adresse e-mail.")

                # Appeler la méthode pour envoyer l'e-mail avec le document
                record.send_document_by_email()

        return res


    type_commd = fields.Selection([
        ("comand1","Les contrats d’assistance et de maintenance"),
        ("comand2", "Les commandes de matériel et équipement"),
        ("comand3", "Les travaux et services"),
    ],string="Type de l'offre ",required=True)

    expres_command = fields.Selection(
        [
            ("express1", "Un bon de commande"),
            ("express2", "Un bon pour accord"),
            ("express3", "Une lettre d’attribution de marché."),
            ("express4","contrat de maintenance"),
            ("express5", "Ouverture de dossier")
        ],string="Expression de la commande"
    )
    etap_commande = fields.Selection(
        [
            ("traite","Traité"),
            ("non_traite", "Non Traité"),
        ],default ="non_traite"
    )
    offre_physique=fields.Binary("Offre physique")



class StockPicking(models.Model):
    _inherit = "stock.picking"

    rapport_control = fields.Binary("Rapport de contrôle")
    rapport2 = fields.Binary("Rapport de suivi projet")
    rapport3 = fields.Binary("Bon ou PV de livraison- attestation de bonne exécution")
    rapport4 = fields.Binary("Pv de fin")

class ResUsers(models.Model):
    _inherit = "res.users"

    type_groups = fields.Selection(
        [
            ("type1","Service commercial"),
            ("type2", "Le Contrôleur de Gestion"),
            ("type3", "La Direction Général"),
            ("type4", "Direction Technique"),
        ]
    )
    user_mail = fields.Char("E-Mail")










