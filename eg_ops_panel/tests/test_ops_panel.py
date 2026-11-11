# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import HttpCase, TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestOpsPanel(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({"name": "Ops Customer"})
        cls.env["sale.order"].create({"partner_id": cls.partner.id})
        confirmed = cls.env["sale.order"].create({"partner_id": cls.partner.id})
        product = cls.env["product.product"].create({"name": "Ops Item", "list_price": 10})
        confirmed.order_line = [(0, 0, {"product_id": product.id, "product_uom_qty": 2})]
        confirmed.action_confirm()

    def _check(self, user):
        env = self.env(user=user)
        for period in ("month", "prev", "all"):
            data = env["eg.ops.panel"].get_dashboard_data(period)
            self.assertTrue(data["kpis"])
            kpis = list(data["kpis"])
            kpis += [k["secondary"] for k in data["kpis"] if k.get("secondary")]
            for kpi in kpis:
                action = kpi["action"]
                self.assertEqual(
                    kpi["count"],
                    env[action["res_model"]].search_count(action["domain"]),
                    f"{kpi['key']} ({period}) for {user.login}",
                )
            self.assertEqual(len(data["weekly"]["weeks"]), 6)

    def test_weekly_includes_order_confirmed_today(self):
        """The order confirmed in setUpClass (dated now) lands in the current week's bar."""
        weeks = self.env["eg.ops.panel"].get_dashboard_data("month")["weekly"]["weeks"]
        self.assertGreaterEqual(weeks[-1]["amount"], 20.0)

    def test_kpi_counts_admin(self):
        self._check(self.env.ref("base.user_admin"))

    def test_kpi_counts_demo(self):
        demo = self.env.ref("base.user_demo", raise_if_not_found=False)
        if not demo:
            self.skipTest("demo data not loaded")
        demo.group_ids |= self.env.ref("sales_team.group_sale_salesman")
        self._check(demo)

    def test_invalid_period_falls_back(self):
        data = self.env["eg.ops.panel"].get_dashboard_data("bogus")
        self.assertEqual(data["period"], "month")


@tagged("post_install", "-at_install")
class TestOpsPanelUi(HttpCase):
    def test_dashboard_renders(self):
        """Opens the client action in a real browser: any OWL/JS error fails the test."""
        self.browser_js(
            "/odoo/action-eg_ops_panel.action_dashboard",
            "console.log('test successful')",
            ready="!!document.querySelector('.eg_ops_kpi')",
            login="admin",
        )
