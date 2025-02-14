from datetime import datetime

from odoo import api, fields, models

class AtOuvertureContrat(models.Model):
    _name = "atm.ouverture.contrat"
    _description = "Ouverture de dossier"
    _rec_name = "name"


    @api.model
    def create(self, vals):
        record = super(AtOuvertureContrat, self).create(vals)
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

    def test(self):
        return 'cone'

    def annule(self):
        self.update({"state": "draft"})

    def action_submit(self):
        self.update({"state": "ouvert_dossier"})

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

    def execute(self):
        self.update({"state": "execution"})
        users = self.env["res.users"].search([('type_groups', '=', 'type3')])

        # Création de l'e-mail pour chaque utilisateur
        for user in users:
            mail_values = {
                'subject': "Exécution du projet",
                'body_html': f"<p>Bonjour {user.name},</p><p> le projet a été executé avec success .</p>",
                'email_to': user.user_mail,
                'author_id': self.env.user.partner_id.id,  # Auteur de l'email (l'utilisateur actuel)
            }
            self.env['mail.mail'].create(mail_values).send()  # Création et envoi de l'email

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






    name = fields.Char("N°dossier" ,readonly=True)
    sale_order_id = fields.Many2one(
        "sale.order",
        "Expression de la commande",
        domain="[('expres_command', '=', 'express4'),('etap_commande', '!=', 'traite'),('state', '!=', 'sale')]"
    )
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
            ("execution", "Exécution")
        ],default="draft"
    )
    rapport_exe = fields.Binary("Rapport d’intervention signé par le client")
    user_id = fields.Many2one(
        "res.users",
        string="Agent",
        default=lambda self: self.env.user.id , readonly=True
    )




