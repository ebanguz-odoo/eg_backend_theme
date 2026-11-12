# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "EG Ops Panel",
    "summary": "Operations dashboard: quotations, orders, deliveries, activities and opportunities at a glance",
    "version": "19.0.1.0.0",
    "category": "Productivity",
    "website": "https://github.com/ebanguz-odoo/eg_backend_theme",
    "author": "Esteban Guzman",
    "maintainers": ["ebanguz"],
    "support": "estebanguzman9301@gmail.com",
    "license": "LGPL-3",
    "images": ["static/description/icon.png"],
    "depends": ["eg_backend_theme", "sale_management"],
    "data": ["views/eg_ops_panel_views.xml"],
    "assets": {
        "web.assets_backend": [
            "eg_ops_panel/static/src/scss/ops_panel.scss",
            "eg_ops_panel/static/src/js/ops_panel.js",
            "eg_ops_panel/static/src/xml/ops_panel.xml",
        ],
    },
    "installable": True,
    "application": True,
}
