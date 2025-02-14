from datetime import datetime

from odoo import api, fields, models

class AtOuvertureDossier(models.Model):
    _name = "atm.ouverture.dossier"
    _description = "Ouverture de dossier"
    _rec_name = "name"



    @api.model
    def create(self, vals):
        record = super(AtOuvertureDossier, self).create(vals)
        if record:
            # Récupération des utilisateurs de type 'type1'
            users = self.env["res.users"].search([('type_groups', '=', 'type2')])

            # Création de l'e-mail pour chaque utilisateur
            for user in users:
                mail_values = {
                    'subject': "Création d'un nouveau OT",
                    'body_html': f"<p>Bonjour {user.name},</p><p>Un nouveau OT a été créé : <strong>{record.user_id.name}</strong>.</p>",
                    'email_to': user.user_mail,
                    'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
                }
                self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

        return record

    def create_projet(self):

        project_model = self.env['project.project']  # Modèle de projet
        users = self.env["res.users"].search([('type_groups', '=', 'type4')])
        for record in self:
            projet = project_model.create({
                'name': record.name,
                'atm_ouverture_dossier_id': record.id,
                'partner_id': record.sale_order_id.partner_id.id
            })

            if projet:
                for user in users:
                    mail_values = {
                        'subject': "Creation de nouveau projet",
                        'body_html': f"<p>Bonjour {user.name},</p><p>un nouveau proejet {self.name} a été créer </strong>.</p>",
                        'email_to': user.user_mail,
                        'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
                    }
                    self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email
                # Mise à jour de l'état de la commande de vente
                if record.sale_order_id:
                    record.sale_order_id.write({"etap_commande": "traite"})

                # Mise à jour de l'état de la commande d'achat
                if record.purchase_order_ids:
                    record.purchase_order_ids.write({"etap_commande": "traite"})

            # Mise à jour de l'état du dossier
            record.write({"state": "projet"})

        return True

    def action_submit(self):
        self.update({"state": "ouvert_dossier"})
        users = self.env["res.users"].search([('type_groups', '=', 'type2')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Création d'un nouveau OT",
                'body_html': f"<p>Bonjour {user.name},</p><p>Un nouveau OT a été créé : <strong>{self.user_id.name}</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

    def test(self):
        return 'cone'

    def verify(self):
        self.update({"state": "validate"})
        self.generate_number()
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type4')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Analyse de OT",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le nouveau OT {self.name} a été validé par : <strong>{self.user_id.name}</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

        # Génération du nom du dossier

    def generate_number(self):
        for record in self:
            # Récupération de la date d'ouverture
            date_ouverture = record.dat_ouverture or fields.Date.today()
            formatted_date = datetime.strptime(str(date_ouverture), '%Y-%m-%d')

            # Format personnalisé : JJMM-AAAA
            day = formatted_date.strftime('%d')  # Jour sur 2 chiffres
            month = formatted_date.strftime('%m')  # Mois sur 2 chiffres
            year = formatted_date.strftime('%Y')  # Année sur 4 chiffres

            # Construction du numéro
            custom_number = f"{day}{month}{year}VTE" + str(self.id)

            # Mise à jour du champ 'name'
            record.update({"name": custom_number})

    def annule(self):

        self.update({"state": "draft"})

    def analyse(self):
        self.update({"state": "analyse"})
        # Récupération des utilisateurs de type 'type1'
        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Analyse de OT",
                'body_html': f"<p>Bonjour {user.name},</p><p>Le nouveau OT {self.name} a été analysé par : <strong>{self.user_id.name}</strong>.</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

        # Génération du nom du dossier







    name = fields.Char("N°dossier" ,readonly=True)
    sale_order_id = fields.Many2one(
        "sale.order", 
        "Commande client",
        domain="[('expres_command', '!=', False),('etap_commande', '!=', 'traite'),('expres_command', '!=', 'express4'),('state', '=', 'sale')]",
        required =True,

    )
    expre_commande = fields.Selection(
        related="sale_order_id.expres_command",
        string="Expression de la commande",
        readonly=True,
        store=True
    )
    fiche_affaire = fields.Binary("Fiche affaire")
    purchase_order_ids = fields.Many2many("purchase.order",
                                         string="Offre fournisseurs",
                                          domain="[('etap_commande', '!=', 'traite')]"
                                         )
    dat_ouverture = fields.Date("Date d'ouverture", default=fields.Date.today)
    state = fields.Selection(
        [
            ("draft", "Brouillon"),
            ("ouvert_dossier","Ouverture de dossier"),
            ("analyse", "Analyse"),
            ("validate", "Validation"),
            ("projet", "Projet")
        ],default="draft"
    )
    rapport_selec_f = fields.Binary("Rapport de sélection fournisseur")
    user_id = fields.Many2one(
        "res.users",
        string="Agent",
        default=lambda self: self.env.user.id , readonly=True
    )

class Project(models.Model):
    _inherit = "project.project"

    atm_ouverture_dossier_id = fields.Many2one("atm.ouverture.dossier", string="Dossier associé")


