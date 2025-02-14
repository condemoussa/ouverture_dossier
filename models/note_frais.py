# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

#
class NoteFrais(models.Model):
    _inherit = "hr.expense.sheet"
    _description = "Gestion des depenses pour l'entreprise cogitech"




    def action_submit(self):
        self.update({"state": "submit","state_up": "submit"})
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Nouvelle demande de decaissement",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Une nouvelle de decaissement à été crée : <strong>{self.name} par {self.create_uid} </strong></p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_verification(self):
        self.update({"state_up": "transfert"})
        users = self.env["res.users"].search([('type_groups', '=', 'type11')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Transmission d'une demande de decaissement",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Une nouvelle de decaissement vous etes transmis: <strong>{self.name}  </strong></p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_valider(self):
        self.update({"state_up": "accord","state":"approve"})
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Validation de la  demande de decaissement",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>La demande à été validée  <strong>{self.name}  </strong></p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_annuler(self):
        self.update({"state_up": "reset","state":"cancel"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Annulation de la demande",
                'body_html': f"<p>Bonjour {user.name},</p><p>La demande  {self.name} à été annuler </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def transfer_justifs(self):
        self.update({"state_up": "justif"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Transmission des justificatifs",
                'body_html': f"<p>Bonjour {user.name},</p><p> Nous avons les justififs en main </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def action_directeur_general(self):
        self.update({"state_up": "accord"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Validation de la demande par le directeur general",
                'body_html': f"<p>Bonjour {user.name},</p><p>La demande à été validée</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def validation_justifs(self):
        self.update({"state_up": "validate"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])

    def rejet_justifs(self):
        self.update({"state_up": "rejet"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type10')])


    piece_caisse = fields.Binary("Pièce de caisse")
    visa_demandeur = fields.Binary("Visa du demandeur")
    visa_direct_fin = fields.Binary("Visa du Directeur Financier")

    state_up = fields.Selection(
        [
            ("draft","Brouillon"),
            ("submit", "Soumis"),
            ("transfert", "Transferer"),
            ("accord", "Accord"),
            ("justif", "Transmission des justificatifs"),
            ("reset", "Annuler"),
            ("validate", "Valider"),
            ("rejet", "Rejetter"),

        ],default="draft"
    )












