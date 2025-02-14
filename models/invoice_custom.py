from odoo import models, fields, api
from datetime import date


class AccountMove(models.Model):
    _inherit = 'account.move'

    def send_due_invoice_reminders(self):
        # Récupérer les factures client en statut ouvert (non payé) et à échéance dépassée
        invoices = self.search([
            ('move_type', '=', 'out_invoice'),  # Factures client
            ('state', '=', 'posted'),  # Factures validées
            ('payment_state', 'not in', ['paid', 'in_payment']),  # Non payé
            ('invoice_date_due', '<', date.today())  # Échéance dépassée
        ])

        for invoice in invoices:
            # Préparer l'objet mail
            mail_values = {
                'subject': f"Rappel : Facture {invoice.name} arrivée à échéance",
                'body_html': f"""
                    <p>Bonjour {invoice.partner_id.name},</p>
                    <p>Nous vous rappelons que la facture <b>{invoice.name}</b>, d'un montant de 
                    <b>{invoice.amount_total} {invoice.currency_id.symbol}</b>, arrivée à échéance le 
                    <b>{invoice.invoice_date_due}</b>, est toujours en attente de paiement.</p>
                    <p>Nous vous remercions de bien vouloir régulariser la situation dans les plus brefs délais.</p>
                    <p>Cordialement,</p>
                    <p>Votre équipe.</p>
                """,
                'email_to': invoice.partner_id.email,
                'email_from': self.env.user.email
            }

            # Créer l'e-mail
            mail = self.env['mail.mail'].create(mail_values)

            # Envoyer l'e-mail
            mail.send()

        return True
