from itertools import product
from odoo import models, fields, api
from datetime import date

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_soumis(self):
        self.update({"state_p": "submitted","state":"waiting"})
        users = self.env["res.users"].search([('type_groups', '=', 'type4')])
        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                "subject": "Nouvelle demande de sortie",
                "body_html": f"""
                               <p>Bonjour M. {user.name},</p>
                               <p>Une nouvelle demande à été crée :</p>
                               <p><strong>{self.name}</strong> par <strong>{self.create_uid.name}</strong>.</p>
                               <p>Veuillez la transférer au gestionnaire SVP.</p>
                           """,
                "email_to": user.user_mail,
                "email_from": self.env.user.email,  # L'expéditeur est l'utilisateur actuel
                "author_id": self.env.user.partner_id.id,
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def action_transfere(self):

        self.update({"state_p": "approved","state":"confirmed"})
        users = self.env["res.users"].search([('type_groups', '=', 'type9')])
        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                "subject": "Transmission au Gestionnaire de Stock",
                "body_html": f"""
                          <p>Bonjour M. {user.name},</p>
                          <p>Une nouvelle demande vous a été transférée :</p>
                          <p><strong>{self.name}</strong></p>
                      """,
                "email_to": user.user_mail,
                "email_from": self.env.user.email,  # L'expéditeur est l'utilisateur actuel
                "author_id": self.env.user.partner_id.id,
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def sortir_physique(self):
        self.update({"state_p": "sortir_physique"})
        self.button_validate()

        users = self.env["res.users"].search([('type_groups', '=', 'type9')])
        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                "subject": "Transmission au Gestionnaire de Stock",
                "body_html": f"""
                                <p>Bonjour M. {user.name},</p>
                                <p>Une nouvelle demande vous a été transférée :</p>
                                <p><strong>{self.name}</strong></p>
                            """,
                "email_to": user.user_mail,
                "email_from": self.env.user.email,  # L'expéditeur est l'utilisateur actuel
                "author_id": self.env.user.partner_id.id,
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def livraison_client(self):
        self.update({"state_p": "livraison_client"})

        users = self.env["res.users"].search([('type_groups', '=', 'type4')])
        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                "subject": "Livraison au client",
                "body_html": f"""
                                     <p>Bonjour M. {user.name},</p>
                                     <p>La livraison été effectué au client :</p>
                                 """,
                "email_to": user.user_mail,
                "email_from": self.env.user.email,  # L'expéditeur est l'utilisateur actuel
                "author_id": self.env.user.partner_id.id,
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email


    def action_rejeter(self):
        self.update({"state_p": "rejected"})
        users = self.env["res.users"].search([('type_groups', '=', 'type4')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                "subject": "Rejet de la sortie du matériel",
                "body_html": f"""
                                  <p>Bonjour M. {user.name},</p>
                                  <p>La demande <strong>{self.name}</strong> a été rejetée.</p>
                                  <p>Veuillez consulter la plateforme pour plus de détails.</p>
                              """,
                "email_to": user.email,
                "email_from": self.env.user.email,
                "author_id": self.env.user.partner_id.id,
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email




    offre_physique =fields.Binary("Offre physique")
    demandeur = fields.Many2one("res.users", string="Demandeur")
    state_p= fields.Selection(
        [
            ("draft", "Brouillon"),
            ("submitted", "Directeur technique"),
            ("approved", "Gestionnaire de Stock"),
            ("sortir_physique", "Sortie physique"),
            ("livraison_client", "Livraison client"),
            ("rejected", "Rejetée"),
        ],
        string="État",
        default="draft",
    )


