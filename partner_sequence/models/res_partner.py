from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    customer_number = fields.Char(string="Customer ID", readonly=True, copy=False)
    vendor_number = fields.Char(string="Vendor ID", readonly=True, copy=False)
    is_customer = fields.Boolean(
        default=False,
        help="This will assign sequence number for Customer",
    )
    is_vendor = fields.Boolean(
        default=False,
        help="This will assign sequence number for Vendor",
    )
    has_tin = fields.Boolean(string="Has TIN No.", default=True)
    is_employee = fields.Boolean(required=False)
    employee_number = fields.Char(string="Employee ID", readonly=True, copy=False)

    @api.constrains("vat")
    def _check_unique_vat(self):
        for rec in self:
            if rec.vat:
                existing = self.search(
                    [("vat", "=", rec.vat), ("id", "!=", rec.id)], limit=1
                )
                if existing:
                    raise ValidationError(
                        _(
                            "The Tax ID must be unique! \n"
                            "There is a record already registered with this TIN number!"
                        )
                    )

    def _assign_partner_sequences(self):
        """Assign unique sequences based on partner type flags."""
        for rec in self:
            if rec.is_customer and not rec.customer_number:
                rec.customer_number = self.env["ir.sequence"].next_by_code(
                    "res.partner.customer"
                )
            if rec.is_vendor and not rec.vendor_number:
                rec.vendor_number = self.env["ir.sequence"].next_by_code(
                    "res.partner.vendor"
                )
            if rec.is_employee and not rec.employee_number:
                rec.employee_number = self.env["ir.sequence"].next_by_code(
                    "hr.employee.custom"
                )

    @api.model_create_multi
    def create(self, vals_list):
        partners = super().create(vals_list)
        partners._assign_partner_sequences()
        return partners

    def write(self, vals):
        result = super().write(vals)
        self._assign_partner_sequences()
        return result
