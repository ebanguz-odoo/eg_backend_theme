# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from odoo import models
from odoo.http import request


class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    def _eg_theme_available(self):
        # The theme targets Community: leave web_enterprise alone.
        return "web_enterprise" not in self.env.registry._init_modules

    def _eg_appearance(self):
        """Resolved appearance of the current user, or {} when the theme is off."""
        user = self.env.user
        if not self._eg_theme_available() or user._is_public():
            return {}
        # The /odoo request carries no allowed_company_ids: the active company lives in the "cids" cookie.
        cids = request.httprequest.cookies.get("cids", "") if request else ""
        allowed = set(user._get_company_ids())
        company_ids = [int(cid) for cid in cids.split("-") if cid.isdigit() and int(cid) in allowed]
        if company_ids:
            user = user.with_context(allowed_company_ids=company_ids)
        appearance = user._eg_appearance()
        return {} if appearance["preset"] == "odoo" else appearance

    def color_scheme(self):
        scheme = self._eg_appearance().get("scheme")
        if not scheme:
            return super().color_scheme()
        if scheme == "system":
            cookies = request.httprequest.cookies if request else {}
            scheme = "dark" if cookies.get("eg_os_scheme") == "dark" else "light"
        return scheme

    def session_info(self):
        info = super().session_info()
        info["eg_theme_available"] = self._eg_theme_available()
        return info

    def webclient_rendering_context(self):
        context = super().webclient_rendering_context()
        appearance = self._eg_appearance()
        classes = ""
        if appearance:
            classes = (
                f"eg-theme eg-preset-{appearance['preset']} eg-accent-{appearance['accent']}"
                f" eg-surface-{appearance['surface']} eg-scheme-{context['color_scheme']}"
                f" eg-density-{appearance['density']} eg-navbar-{appearance['navbar']}"
            )
        if request and self._eg_theme_available():
            # Core JS (graph, ace, color picker, mail) reads the scheme from this cookie.
            request.future_response.set_cookie("color_scheme", context["color_scheme"], max_age=31536000)
        context["eg_body_classes"] = classes
        context["eg_scheme_mode"] = appearance.get("scheme", "light")
        return context
