# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "EG Backend Theme - Chatter",
    "summary": "Chatter as a timeline, tracking changes as a diff, themed composer and activities",
    "version": "19.0.1.0.0",
    "category": "Themes/Backend",
    "website": "https://github.com/ebanguz-odoo/eg_backend_theme",
    "images": ["static/description/icon.png"],
    "support": "estebanguzman9301@gmail.com",
    "author": "Esteban Guzman",
    "maintainers": ["ebanguz"],
    "license": "LGPL-3",
    "depends": ["eg_backend_theme", "mail"],
    "assets": {
        "web.assets_backend": [
            "eg_backend_theme_mail/static/src/scss/*.scss",
        ],
    },
    "auto_install": True,
    "installable": True,
    "application": False,
}
