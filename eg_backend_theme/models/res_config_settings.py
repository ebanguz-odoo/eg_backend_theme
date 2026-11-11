# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    eg_preset = fields.Selection(related="company_id.eg_preset", readonly=False)
    eg_accent = fields.Selection(related="company_id.eg_accent", readonly=False)
    eg_surface = fields.Selection(related="company_id.eg_surface", readonly=False)
    eg_scheme = fields.Selection(related="company_id.eg_scheme", readonly=False)
    eg_density = fields.Selection(related="company_id.eg_density", readonly=False)
    eg_navbar = fields.Selection(related="company_id.eg_navbar", readonly=False)
    eg_allow_user = fields.Boolean(related="company_id.eg_allow_user", readonly=False)
