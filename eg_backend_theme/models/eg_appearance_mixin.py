# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import fields, models

EG_PRESETS = [("odoo", "Odoo original"), ("aura", "Aura"), ("graphite", "Graphite"), ("mineral", "Mineral")]
EG_ACCENTS = [
    ("purple", "Purple"),
    ("blue", "Blue"),
    ("emerald", "Emerald"),
    ("amber", "Amber"),
    ("rose", "Rose"),
    ("contrast", "Contrast"),
]
EG_SURFACES = [
    ("preset", "Preset default"),
    ("slate", "Slate"),
    ("zinc", "Zinc"),
    ("stone", "Stone"),
    ("sage", "Sage"),
]
EG_SCHEMES = [("preset", "Preset default"), ("light", "Light"), ("dark", "Dark"), ("system", "Follow the system")]
EG_DENSITIES = [
    ("preset", "Preset default"),
    ("compact", "Compact"),
    ("std", "Standard"),
    ("comfy", "Comfortable"),
    ("wide", "Wide"),
]
EG_NAVBARS = [("surface", "Surface"), ("accent", "Accent")]
EG_LABELS = [("inline", "Beside the field"), ("stacked", "Above the field")]
EG_AXES = ("preset", "accent", "surface", "scheme", "density", "navbar", "labels")
EG_FIELDS = tuple(f"eg_{axis}" for axis in EG_AXES)
# Values used when an axis is set to "preset", by preset.
EG_PRESET_DEFAULTS = {
    "aura": {"surface": "slate", "scheme": "light", "density": "comfy"},
    "graphite": {"surface": "zinc", "scheme": "dark", "density": "compact"},
    "mineral": {"surface": "sage", "scheme": "light", "density": "wide"},
}


class EgAppearanceMixin(models.AbstractModel):
    _name = "eg.appearance.mixin"
    _description = "Backend appearance fields"

    eg_preset = fields.Selection(EG_PRESETS, string="Style", required=True, default="aura")
    eg_accent = fields.Selection(EG_ACCENTS, string="Accent color", required=True, default="purple")
    eg_surface = fields.Selection(EG_SURFACES, string="Surface tint", required=True, default="preset")
    eg_scheme = fields.Selection(EG_SCHEMES, string="Color scheme", required=True, default="preset")
    eg_density = fields.Selection(EG_DENSITIES, string="Density", required=True, default="preset")
    eg_navbar = fields.Selection(EG_NAVBARS, string="Navigation bar", required=True, default="surface")
    eg_labels = fields.Selection(EG_LABELS, string="Form labels", required=True, default="inline")
