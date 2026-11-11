# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install")
class TestAssets(TransactionCase):
    def test_backend_bundle_compiles_with_chatter_styles(self):
        """The backend bundle must compile (SCSS included) and carry the chatter rules."""
        bundle = self.env["ir.qweb"]._get_asset_bundle("web.assets_backend", css=True, js=False)
        attachment = bundle.css()
        self.assertFalse(bundle.css_errors)
        self.assertIn("o-mail-Message-trackingOld", attachment.raw.decode())
