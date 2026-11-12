# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.exceptions import AccessError
from odoo.tests import Form, tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAppearance(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.company = cls.env.company
        cls.demo = cls.env.ref("base.user_demo")

    def test_defaults(self):
        user = self.env["res.users"].create({"name": "EG user", "login": "eg_user"})
        self.assertTrue(user.eg_follow_company)
        self.assertEqual(
            (
                user.eg_preset,
                user.eg_accent,
                user.eg_surface,
                user.eg_scheme,
                user.eg_density,
                user.eg_navbar,
                user.eg_labels,
            ),
            ("aura", "purple", "preset", "preset", "preset", "surface", "inline"),
        )
        self.assertTrue(self.company.eg_allow_user)

    def test_resolution_matrix(self):
        presets = {
            "aura": ("slate", "light", "comfy"),
            "graphite": ("zinc", "dark", "compact"),
            "mineral": ("sage", "light", "wide"),
        }
        self.company.eg_accent = "emerald"
        self.company.eg_navbar = "accent"
        self.company.eg_labels = "stacked"
        for preset, (surface, scheme, density) in presets.items():
            self.company.eg_preset = preset
            self.assertEqual(
                self.env.user._eg_appearance(),
                {
                    "preset": preset,
                    "accent": "emerald",
                    "surface": surface,
                    "scheme": scheme,
                    "density": density,
                    "navbar": "accent",
                    "labels": "stacked",
                },
            )

    def test_explicit_values_win_over_preset(self):
        self.company.write({"eg_preset": "graphite", "eg_surface": "stone", "eg_scheme": "system", "eg_density": "std"})
        result = self.env.user._eg_appearance()
        self.assertEqual((result["surface"], result["scheme"], result["density"]), ("stone", "system", "std"))

    def test_user_overrides_company(self):
        self.company.write({"eg_preset": "aura", "eg_allow_user": True})
        self.demo.write({"eg_follow_company": False, "eg_preset": "graphite", "eg_accent": "rose"})
        result = self.demo.with_user(self.demo)._eg_appearance()
        self.assertEqual((result["preset"], result["accent"], result["scheme"]), ("graphite", "rose", "dark"))
        self.demo.eg_follow_company = True
        self.assertEqual(self.demo._eg_appearance()["preset"], "aura")

    def test_company_lock(self):
        self.demo.write({"eg_follow_company": False, "eg_preset": "graphite"})
        self.company.write({"eg_preset": "mineral", "eg_allow_user": False})
        self.assertEqual(self.demo._eg_appearance()["preset"], "mineral")

    def test_user_can_write_own_fields(self):
        values = {"eg_follow_company": False, "eg_preset": "mineral", "eg_accent": "blue", "eg_scheme": "dark"}
        self.demo.with_user(self.demo).write(values)
        self.assertEqual(self.demo.eg_accent, "blue")
        readable = self.demo.with_user(self.demo).read(["eg_preset", "eg_density", "eg_follow_company"])
        self.assertEqual(readable[0]["eg_preset"], "mineral")

    def test_locked_company_neutralizes_user_write(self):
        self.company.write({"eg_preset": "mineral", "eg_allow_user": False})
        self.demo.with_user(self.demo).write({"eg_follow_company": False, "eg_preset": "graphite"})
        self.assertEqual(self.demo.eg_preset, "graphite")  # stored, but ignored while locked
        self.assertEqual(self.demo._eg_appearance()["preset"], "mineral")

    def test_active_company_drives_resolution(self):
        company2 = self.env["res.company"].create({"name": "EG second", "eg_preset": "mineral", "eg_allow_user": False})
        self.demo.company_ids |= company2
        self.company.write({"eg_preset": "aura", "eg_allow_user": True})
        demo = self.demo.with_user(self.demo)
        self.assertEqual(demo._eg_appearance()["preset"], "aura")
        in_company2 = demo.with_context(allowed_company_ids=[company2.id, self.company.id])
        self.assertEqual(in_company2._eg_appearance()["preset"], "mineral")
        self.assertTrue(demo.eg_company_allow_user)
        self.assertFalse(in_company2.eg_company_allow_user)

    def test_ir_http_skips_web_enterprise(self):
        self.env.registry._init_modules.add("web_enterprise")
        self.addCleanup(self.env.registry._init_modules.discard, "web_enterprise")
        self.assertEqual(self.env["ir.http"].with_user(self.demo)._eg_appearance(), {})
        self.assertFalse(self.demo.eg_theme_available)

    def test_ir_http_public_user_has_no_theme(self):
        public = self.env.ref("base.public_user")
        self.assertEqual(self.env["ir.http"].with_user(public)._eg_appearance(), {})

    def test_user_cannot_write_other_user(self):
        with self.assertRaises(AccessError):
            self.env.ref("base.user_admin").with_user(self.demo).write({"eg_preset": "odoo"})

    def test_settings_related_fields(self):
        with Form(self.env["res.config.settings"]) as form:
            form.eg_preset = "graphite"
            form.eg_accent = "amber"
            form.eg_allow_user = False
        settings = form.save()
        settings.execute()
        self.assertEqual(self.company.eg_preset, "graphite")
        self.assertEqual(self.company.eg_accent, "amber")
        self.assertFalse(self.company.eg_allow_user)
