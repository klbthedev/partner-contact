from odoo import api, fields, models


class HREmployee(models.Model):
    _inherit = "hr.employee"

    employee_number = fields.Char(string="Employee ID", readonly=True, copy=False)

    def _assign_employee_number(self):
        """Assign a unique sequence to the employee if missing."""
        for rec in self:
            if not rec.employee_number:
                rec.employee_number = self.env["ir.sequence"].next_by_code(
                    "hr.employee.custom"
                )

    @api.model_create_multi
    def create(self, vals_list):
        employees = super().create(vals_list)
        employees._assign_employee_number()
        return employees
