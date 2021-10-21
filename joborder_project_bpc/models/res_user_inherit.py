from odoo import fields, models, api


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    web_url = fields.Char("Website Url")
    user_agent = fields.Char("Agent")

    @api.onchange('web_url')
    def _onchange(self):
        vals = {
            'name': 'BS Debug',
            'url': self.web_url,
            'view_id': 1,
        }
        record = self.env['website.page'].create(vals)
