# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models

class CrmLead(models.Model):
    _inherit = "crm.lead"

    @api.model
    def create(self, vals):
        res = super(CrmLead, self).create(vals)
        return res

    def test(self):
        print("conde")

    @api.onchange("affecte_ids")
    def gotogo(self):
        if self.affecte_ids:
            # Si vous voulez afficher tous les IDs
            print(self.affecte_ids.ids)


    def nogo(self):
        # Vérifie qu'il y a un seul enregistrement
        self.ensure_one()

        # Chargement de l'enregistrement CRM
        crm = self.env["crm.lead"].browse(self.id)

        # Vérification et suppression
        if crm.exists():
            crm.unlink()

        # Retourne l'action pour afficher la vue `tree` de crm.lead
        return {
            'type': 'ir.actions.act_window',
            'name': 'Opportunités',
            'view_mode': 'tree,form',
            'res_model': 'crm.lead',
            'target': 'current',  # Affiche dans la même fenêtre
            'context': {},  # Ajoutez un contexte personnalisé si nécessaire
        }

    def action_submit(self):
        self.update({"state": "submit"})
        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Création d'une opportunité",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Une nouvelle opportunité à été crée : <strong>{self.name} par {self.create_uid} </strong>,Veuillez valider svp</p>",
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
                'subject': "Annulation de la creation de l'opportunité",
                'body_html': f"<p>Bonjour M.{user.name},</p><p>L' {self.name} n'a pas été validé </strong>.</p>",
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
                'subject': "Validation de l'opportunité",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>l'opportunité {self.name} a été validé </strong>.</p>",
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
                'subject': "Création d'une opportunité",
                'body_html': f"<p>Bonjour M. {user.name},</p><p>Un nouveau propers a été crée </p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    partner_id = fields.Many2one("res.partner", domain="[('state', '=', 'valider')]")
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
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("submit", "Soumis"),
            ("valider", "Valider"),
            ("cancel", "Annuler"),
            ("affecte", "Affecter")
        ], default="draft"
    )

    affecte_ids = fields.Many2many(
        "res.users",
        domain=lambda self: [
            ('groups_id', 'in', self.env.ref('ouverture_dossier.itc_id').id)
        ],
        readonly=True,
        string="Utilisateurs :"
    )

    @api.onchange("pv_reunion1", "pv_reunion2", "pv_reunion3", "pv_reunion4", "pv_reunion5", "pv_reunion6")
    def notification(self):
        if self.user_id:  # Vérifier si l'utilisateur est bien défini
            mail_values = {
                'subject': "PV de la réunion ajouté à l'opportunité",
                'body_html': f"<p>Bonjour M. {self.user_id.name},</p>"
                             f"<p>Un PV a été ajouté à l'opportunité <strong>{self.name}</strong>.</p>",
                'email_to': self.user_id.user_mail,  # Correction de 'user_mail' en 'email'
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    pv_reunion1 = fields.Binary("PV 1")
    pv_reunion2 = fields.Binary("PV 2")
    pv_reunion3 = fields.Binary("PV 3")
    pv_reunion4 = fields.Binary("PV 4")
    pv_reunion5 = fields.Binary("PV 5")
    pv_reunion6 = fields.Binary("PV 6")








