# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

{
    "name": "EG Backend Theme",
    "summary": "Modern backend look for Odoo Community: presets, accent, light/dark, density and an app launcher",
    "version": "19.0.1.0.0",
    "category": "Themes/Backend",
    "website": "https://github.com/ebanguz-odoo/eg_backend_theme",
    "images": ["static/description/icon.png"],
    "support": "estebanguzman9301@gmail.com",
    "author": "Esteban Guzman",
    "maintainers": ["ebanguz"],
    "license": "LGPL-3",
    "depends": ["web", "base_setup"],
    "data": [
        "views/webclient_templates.xml",
        "views/res_users_views.xml",
        "views/res_config_settings_views.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "eg_backend_theme/static/src/scss/fonts.scss",
            "eg_backend_theme/static/src/scss/tokens/*.scss",
            "eg_backend_theme/static/src/scss/components/*.scss",
            "eg_backend_theme/static/src/apps_launcher/*",
            "eg_backend_theme/static/src/mobile_tabbar/*",
            "eg_backend_theme/static/src/js/**/*",
            "eg_backend_theme/static/src/xml/**/*",
        ],
        "web.assets_unit_tests": [
            "eg_backend_theme/static/tests/**/*",
        ],
    },
    "installable": True,
    "application": False,
}
