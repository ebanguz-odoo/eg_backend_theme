# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import api, fields, models

from .eg_appearance_mixin import EG_AXES, EG_FIELDS, EG_PRESET_DEFAULTS


class ResUsers(models.Model):
    _name = "res.users"
    _inherit = ["res.users", "eg.appearance.mixin"]  # noqa: RUF012

    eg_follow_company = fields.Boolean(
        string="Use company appearance",
        default=True,
        help="Follow the appearance chosen for the current company.",
    )

    # Helpers for the preferences form, not part of the contract fields. Computed for the active company.
    eg_company_allow_user = fields.Boolean(
        compute="_compute_eg_company_allow_user", string="Company allows customizing"
    )
    eg_theme_available = fields.Boolean(compute="_compute_eg_theme_available")

    @api.depends_context("company")
    def _compute_eg_company_allow_user(self):
        allowed = self.env.company.sudo().eg_allow_user
        for user in self:
            user.eg_company_allow_user = allowed

    def _compute_eg_theme_available(self):
        available = "web_enterprise" not in self.env.registry._init_modules
        for user in self:
            user.eg_theme_available = available

    @property
    def SELF_READABLE_FIELDS(self):
        return super().SELF_READABLE_FIELDS + [
            "eg_follow_company",
            "eg_company_allow_user",
            "eg_theme_available",
            *EG_FIELDS,
        ]

    @property
    def SELF_WRITEABLE_FIELDS(self):
        return super().SELF_WRITEABLE_FIELDS + ["eg_follow_company", *EG_FIELDS]

    def _eg_appearance(self):
        """Resolved appearance of this user in the current company.

        :return: dict preset/accent/surface/scheme/density/navbar/labels, with no
            "preset" placeholder left.
        """
        self.ensure_one()
        user = self.sudo()
        company = self.env.company.sudo()
        source = company if not company.eg_allow_user or user.eg_follow_company else user
        values = {axis: source[f"eg_{axis}"] for axis in EG_AXES}
        defaults = EG_PRESET_DEFAULTS.get(values["preset"], EG_PRESET_DEFAULTS["aura"])
        for axis, default in defaults.items():
            if values[axis] == "preset":
                values[axis] = default
        return values
