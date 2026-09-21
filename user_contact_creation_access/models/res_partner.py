from odoo import _, api, models
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model_create_multi
    def create(self, vals_list):
        if (
            not self.env.is_superuser()
            and not self.env.user.has_group("base.group_system")
            and not self.env.user.has_group(
                "user_contact_creation_access.group_contact_creation"
            )
        ):
            raise AccessError(
                _(
                    "You are not allowed to create contacts. "
                    "Please contact your administrator."
                )
            )
        return super().create(vals_list)
