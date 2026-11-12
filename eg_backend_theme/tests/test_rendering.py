# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import HttpCase, tagged


@tagged("post_install", "-at_install")
class TestRendering(HttpCase):
    def setUp(self):
        super().setUp()
        self.company = self.env.company
        self.company.write({"eg_preset": "aura", "eg_accent": "blue", "eg_scheme": "light", "eg_allow_user": True})
        self.env.ref("base.user_demo").eg_follow_company = True
        self.authenticate("demo", "demo")

    def _page(self):
        return self.url_open("/odoo").text

    def test_body_classes(self):
        html = self._page()
        for cls in (
            "o_web_client",
            "eg-theme",
            "eg-preset-aura",
            "eg-accent-blue",
            "eg-surface-slate",
            "eg-scheme-light",
            "eg-density-comfy",
            "eg-navbar-surface",
            "eg-labels-inline",
        ):
            self.assertIn(cls, html)
        self.assertNotIn("eg_os_scheme", html)

    def test_odoo_preset_turns_theme_off(self):
        self.company.eg_preset = "odoo"
        html = self._page()
        self.assertIn("o_web_client", html)
        self.assertNotIn("eg-theme", html)

    def test_dark_scheme(self):
        self.company.eg_scheme = "dark"
        html = self._page()
        self.assertIn("eg-scheme-dark", html)
        self.assertIn("assets_web_dark", html)

    def test_system_scheme_uses_cookie(self):
        self.company.eg_scheme = "system"
        html = self._page()
        self.assertIn("eg-scheme-light", html)
        self.assertIn("eg_os_scheme", html)  # the inline script that stores the OS preference
        self.opener.cookies.set("eg_os_scheme", "dark")
        html = self._page()
        self.assertIn("eg-scheme-dark", html)
        self.assertIn("assets_web_dark", html)

    def test_color_scheme_method(self):
        self.company.eg_scheme = "dark"
        self.assertEqual(self.env["ir.http"].with_user(self.env.ref("base.user_demo")).color_scheme(), "dark")
        self.company.eg_preset = "odoo"
        self.assertEqual(self.env["ir.http"].with_user(self.env.ref("base.user_demo")).color_scheme(), "light")

    def test_active_company_cookie(self):
        company2 = self.env["res.company"].create({"name": "EG second", "eg_preset": "mineral", "eg_accent": "rose"})
        self.env.ref("base.user_demo").company_ids |= company2
        self.opener.cookies.set("cids", str(company2.id))
        html = self._page()
        self.assertIn("eg-preset-mineral", html)
        self.assertIn("eg-accent-rose", html)
        # a company the user cannot access is ignored
        outsider = self.env["res.company"].create({"name": "EG outsider", "eg_preset": "graphite"})
        self.opener.cookies.set("cids", str(outsider.id))
        self.assertIn("eg-preset-aura", self._page())

    def test_color_scheme_cookie(self):
        self.company.eg_scheme = "dark"
        self.assertEqual(self.url_open("/odoo").cookies.get("color_scheme"), "dark")
        self.company.eg_preset = "odoo"
        self.assertEqual(self.url_open("/odoo").cookies.get("color_scheme"), "light")

    def test_settings_appearance_renders(self):
        """Settings in a real browser with the theme on: widgets render, no JS error."""
        self.browser_js(
            "/odoo/settings",
            "console.log('test successful')",
            ready="!!document.querySelector('.o_field_eg_theme_picker .eg_theme_card')",
            login="admin",
        )
