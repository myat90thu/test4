from odoo import api, models

class DeliveryReport(models.AbstractModel):
    _name = 'report.delivery_reports.delivery_reports.report_delivery_reports_pdf'

    @api.model
    def _get_report_values(self, docids, data=None):
        pass

