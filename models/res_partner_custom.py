# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class ResPartner(models.Model):
    _inherit = "res.partner"



    def action_submit(self):
        self.update({"state": "submit"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type3')])
        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Création d'un nouveau prospect",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Un nouveau prospect a été créé : <strong>{self.name}</strong>,Veuillez valider svp</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def valide(self):
        self.update({"state": "valider"})
        # # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type1')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Validation du prospect",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Le prospect {self.name} a été validé </strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email



    def annule(self):
        self.update({"state": "cancel"})
        # # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type1')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Annulation de la validation du prospect",
                'body_html': f"<p>Bonjour M.{user.name},</p><p>Le nouveau {self.name} n'a pas été validé par : <strong>{self.user_id.name}</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email




    def remettre_draft(self):
        self.update({"state": "draft"})
        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Création d'un nouveau prospect",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Un nouveau prospect a été crée </p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email






    state =fields.Selection(
        [
            ("draft", "Brouillon"),
            ("submit", "Soumis"),
            ("valider","Valider"),
            ("cancel", "Annuler")
        ],default="draft"
    )

    type_fournisseur = fields.Selection(
        [
            ("locaux","locaux"),
            ("etrangers", "étrangers"),

        ]
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
    doc_def = fields.Binary("DFE")
    doc_registre = fields.Binary("Registre de commerce")
    doc_rib = fields.Char("RIB")
    doc_arf = fields.Binary("ARF")
    doc_attes = fields.Binary("Attestation de mise a jours CNPS")
    doc_attes_regime = fields.Binary("Attestation de régime")








