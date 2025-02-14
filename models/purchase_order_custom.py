# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models
from odoo.exceptions import UserError



class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def plan_paiement_valider(self):
        self.update({"etap_state": "plan_paiement"})
        users = self.env["res.users"].search([('type_groups', '=', 'type8')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Validation du plan de paiement",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le plan paiement à été validé</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def plan_paiement_refuse(self):
        self.update({"etap_state": "ser_tresorie"})
        users = self.env["res.users"].search([('type_groups', '=', 'type8')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Refus du plan de paiement",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le plan paiement à été refusé</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def facture_proformat(self):
        self.update({"etap_state": "facture_profomat"})

    def trans_dg_daf(self):
        self.update({"etap_state": "dg_daf"})
        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Transmission du plan de paiement",
                'body_html': f"<p>Bonjour {user.name},</p><p> vous trouverez le plan de paiement dans bon de commande </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def trans_tresorerie(self):
        self.update({"etap_state": "ser_tresorie"})
        users = self.env["res.users"].search([('type_groups', '=', 'type8')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Transmission de bon de commande signé",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le bon de commande a été signe </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def lance_commande(self):
        self.update({"etap_state": "lance_commande"})

    def service_achat(self):
        self.update({"etap_state": "service_achat"})
        users = self.env["res.users"].search([('type_groups', '=', 'type7')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Transmission de bon de commande signé",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le bon de commande à été signe </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def action_annuler(self):
        self.update({"etap_state": "draft"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type1')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Annulation du bon de commande",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le bon de commande {self.name} a été annuler </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def verification_offre(self):
        self.update({"etap_state": "envoye_dg"})

        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Soumission de la facture proforma",
                'body_html': f"<p>Bonjour {user.name},</p><p>Veuillez valider cette facture proforma {self.name}  </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def soumission_dg(self):
        self.update({"etap_state": "envoye_dg"})

    def validate_dg(self):
        self.update({"etap_state": "validate","state":"purchase"})
        if self.offre_physique:  # Vérifie que l'offre physique est activée
            # Récupérer le type de picking (opération de sortie) pour l'entrepôt
            picking_type = self.env['stock.picking.type'].search([('code', '=', 'incoming')], limit=1)
            if not picking_type:
                raise ValueError("Aucun type d'opération 'Sortie' trouvé. Vérifiez la configuration de l'entrepôt.")

            # Créer le picking
            self.env['stock.picking'].create({
                'origin': self.name,
                'partner_id': self.partner_id.id,
                'location_id': picking_type.default_location_src_id.id,  # Emplacement source
                'location_dest_id': self.partner_id.property_stock_customer.id,  # Emplacement client
                'purchase_id': self.id,
                'picking_type_id': picking_type.id,  # Type d'opération
                'offre_physique': self.offre_physique,
                "location_id" :1
            })

        users = self.env["res.users"].search([('type_groups', '=', 'type2')])
        users_gestionnaire = self.env["res.users"].search([('type_groups', '=', 'type9')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Validation de la facture proforma",
                'body_html': f"<p>Bonjour {user.name},</p><p>cette facture proforma {self.name} à été </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

        for user in users_gestionnaire:
            mail_values = {
                'subject': "Entrée en stock",
                'body_html': f"<p>Bonjour {user.name},</p><p>Bientôt, vous aurez des entrées en stock</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  #


    def send_document_controleur(self):

        self.update({"etap_state": "envoye_controleur"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type2')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                 'subject': "Soumission de la facture proforma",
                'body_html': f"<p>Bonjour {user.name},</p><p>Veuillez verifier cette facture proforma {self.name}  </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

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
                'name': 'Demande.pdf',
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
                       <p>Veuillez trouver ci-joint le document lié à la demande <strong>{record.name}</strong>.</p>
                       <p>Cordialement,</p>
                   """,
                'email_from': self.env.user.email ,
                'email_to': email_to,  # E-mail du client
                'attachment_ids': [(4, attachment.id)],  # Associer l'attachement
                'auto_delete': False,  # Ne pas supprimer l'e-mail automatiquement
            }

            # Créer et envoyer l'e-mail
            mail = self.env['mail.mail'].create(mail_values)
            mail.send()


    def action_rfq_send(self):
        # Appel à la méthode originale pour conserver son comportement par défaut
        res = super(PurchaseOrder, self).action_rfq_send()
        self.update({"etap_state": "envoye_fournisseu","state":"sent"})

        # Appel de la méthode `send_document_by_email` pour envoyer le document
        for record in self:
            if record.offre_physique:
                # Vérifier si le client a un e-mail
                if not record.partner_id or not record.partner_id.email:
                    raise UserError(f"Le client de la commande {record.name} n'a pas d'adresse e-mail.")

                # Appeler la méthode pour envoyer l'e-mail avec le document
                record.send_document_by_email()

        return res


    etap_commande = fields.Selection(
        [
            ("traite","Traité"),
            ("non_traite", "Non Traité"),
        ],default ="non_traite"
    )
    offre_physique = fields.Binary("Offre physique")
    rapport_select = fields.Binary("Rapport de sélection fournisseur")
    etap_state = fields.Selection(
        [
            ("draft","Brouillon"),
            ("envoye_fournisseu", "Envoyer au fournisseur"),
            ("facture_profomat", "Facture proforma"),
            ("envoye_controleur", "Envoyer au Controleur"),
            ("envoye_dg", "Envoyer au DG"),
            ("validate", "Validation DG"),
            ("service_achat", "SERVICE ACHAT"),
            ("lance_commande", "LANCÉ COMMANDE"),
            ("ser_tresorie", "TRESORERIE"),
            ("dg_daf", "DG/DAF"),
            ("plan_paiement", "Plan paiement"),

        ] , default="draft"
    )
    plan_paiement =fields.Binary("plan de paiement")












