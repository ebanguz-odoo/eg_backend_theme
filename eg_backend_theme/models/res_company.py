# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResCompany(models.Model):
    _name = "res.company"
    _inherit = ["res.company", "eg.appearance.mixin"]  # noqa: RUF012

    eg_allow_user = fields.Boolean(
        string="Allow users to customize",
        default=True,
        help="When disabled, every user of the company sees the company appearance.",
    )
