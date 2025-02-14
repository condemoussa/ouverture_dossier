from odoo import models, fields, api


class CrmAssignWizard(models.TransientModel):
    _name = 'crm.assign.wizard'
    _description = 'Affecter une opportunité à plusieurs utilisateurs'



    def affectation_opportunite(self):
        self.ensure_one()  # S'assure qu'il n'y a qu'un seul enregistrement
        self.crm_id.update({"state":"affecte"})
        if self.crm_id and self.user_ids:
            self.crm_id.affecte_ids = [(6, 0, self.user_ids.ids)]

            users = self.user_ids
            # envoyer de mail
            for line in users :
                self.env['mail.mail'].sudo().create([
                    {
                        'subject': "Nouvelle opportunité assignée",
                        'body_html': f"""
                                              <p>Bonjour {line.name},</p>
                                              <p>Vous avez été affecté(e) à l'opportunité <strong>{self.crm_id.name}</strong>.</p>
                                              <p>Merci de prendre les actions nécessaires.</p>
                                          """,
                        'email_to': line.user_mail,
                        'author_id': self.env.user.partner_id.id,  # Auteur de l'email (utilisateur actuel)
                    } for user in self.user_ids
                ]).send()

            return True
        return False


    crm_id = fields.Many2one(
        "crm.lead",
        string="Opportunité",
        default=lambda self: self.env.context.get('active_id'),
        readonly=True,
    )
    user_ids = fields.Many2many(
        'res.users',
        string="Utilisateurs",
        help="Sélectionnez les utilisateurs à assigner à cette opportunité.",
    domain = lambda self: [('groups_id', 'in', self.env.ref('ouverture_dossier.itc_id').id)],
    )



