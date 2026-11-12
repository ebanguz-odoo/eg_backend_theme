# Copyright 2026 Esteban Guzman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from datetime import datetime, timedelta

import pytz

from odoo import api, fields, models

FEED_LIMIT = 8
WEEKS = 6
PICKING_OPEN = ["assigned", "confirmed", "waiting"]


class EgOpsPanel(models.AbstractModel):
    _name = "eg.ops.panel"
    _description = "Operations Panel"

    # ------------------------------------------------------------------ helpers

    @api.model
    def _available(self, model):
        """Optional models: installed and readable by the current user."""
        return model in self.env and self.env[model].has_access("read")

    @api.model
    def _local_tz(self):
        try:
            return pytz.timezone(self.env.context.get("tz") or self.env.user.tz or "UTC")
        except pytz.UnknownTimeZoneError:
            return pytz.utc

    @api.model
    def _month_start(self, tz, months_back=0):
        """UTC naive datetime of the 1st of a month at local midnight."""
        now = datetime.now(pytz.utc).astimezone(tz)
        index = now.year * 12 + now.month - 1 - months_back
        local = tz.localize(datetime(index // 12, index % 12 + 1, 1))
        return local.astimezone(pytz.utc).replace(tzinfo=None)

    @api.model
    def _action(self, name, model, domain):
        return {
            "type": "ir.actions.act_window",
            "name": name,
            "res_model": model,
            "views": [[False, "list"], [False, "form"]],
            "domain": domain,
            "target": "current",
        }

    @api.model
    def _amounts(self, model, domain, field):
        """Count and per-currency totals (no conversion between currencies)."""
        company_cur = self.env.company.currency_id
        rows = self.env[model]._read_group(domain, ["currency_id"], ["__count", f"{field}:sum"])
        amounts = [
            {
                "id": cur.id,
                "code": cur.name,
                "symbol": cur.symbol,
                "total": total or 0.0,
                "main": cur == company_cur,
            }
            for cur, _count, total in rows
        ]
        amounts.sort(key=lambda a: not a["main"])
        return sum(count for _cur, count, _total in rows), amounts

    @api.model
    def _kpi(self, key, label, model, domain, amount_field=None):
        if amount_field:
            count, amounts = self._amounts(model, domain, amount_field)
        else:
            count, amounts = self.env[model].search_count(domain), []
        return {
            "key": key,
            "label": label,
            "count": count,
            "amounts": amounts,
            "action": self._action(label, model, domain),
        }

    # ------------------------------------------------------------------ KPIs

    @api.model
    def _sale_kpis(self, period):
        tz = self._local_tz()
        start_cur, start_prev = (
            self._month_start(tz, 0),
            self._month_start(tz, 1),
        )
        if period == "prev":
            start, end = start_prev, start_cur
            prev_start, prev_end = self._month_start(tz, 2), start_prev
        elif period == "month":
            start, end = start_cur, self._month_start(tz, -1)
            prev_start, prev_end = start_prev, start_cur
        else:
            start = end = prev_start = prev_end = None

        def confirmed(low, high):
            domain = [("state", "=", "sale")]
            if low:
                domain += [
                    ("date_order", ">=", fields.Datetime.to_string(low)),
                    ("date_order", "<", fields.Datetime.to_string(high)),
                ]
            return domain

        quotations = self._kpi(
            "quotations",
            self.env._("Open quotations"),
            "sale.order",
            [("state", "in", ["draft", "sent"])],
            "amount_total",
        )
        orders = self._kpi(
            "orders",
            self.env._("Confirmed orders"),
            "sale.order",
            confirmed(start, end),
            "amount_total",
        )
        if prev_start:
            count, amounts = self._amounts("sale.order", confirmed(prev_start, prev_end), "amount_total")
            orders["previous"] = {"count": count, "amounts": amounts}
        return [quotations, orders]

    @api.model
    def _delivery_kpi(self):
        domain = [
            ("picking_type_code", "=", "outgoing"),
            ("state", "in", PICKING_OPEN),
        ]
        kpi = self._kpi("deliveries", self.env._("Deliveries to do"), "stock.picking", domain)
        late = domain + [("scheduled_date", "<", fields.Datetime.now())]
        kpi["secondary"] = self._kpi("late", self.env._("Late deliveries"), "stock.picking", late)
        return kpi

    @api.model
    def _activity_kpi(self):
        today = fields.Date.context_today(self)
        base = [("user_id", "=", self.env.uid)]
        kpi = self._kpi(
            "activities",
            self.env._("Overdue activities"),
            "mail.activity",
            base + [("date_deadline", "<", today)],
        )
        kpi["secondary"] = self._kpi(
            "activities_today",
            self.env._("Activities due today"),
            "mail.activity",
            base + [("date_deadline", "=", today)],
        )
        return kpi

    @api.model
    def _lead_kpi(self):
        domain = [("type", "=", "opportunity"), ("won_status", "=", "pending")]
        # company_currency is not stored, so group by company and map to its currency.
        rows = self.env["crm.lead"]._read_group(domain, ["company_id"], ["__count", "expected_revenue:sum"])
        main = self.env.company.currency_id
        totals = {}
        for company, _count, total in rows:
            cur = company.currency_id or main
            totals[cur] = totals.get(cur, 0.0) + (total or 0.0)
        amounts = [
            {"id": c.id, "code": c.name, "symbol": c.symbol, "total": t, "main": c == main} for c, t in totals.items()
        ]
        amounts.sort(key=lambda a: not a["main"])
        label = self.env._("Open opportunities")
        return {
            "key": "opportunities",
            "label": label,
            "count": sum(count for _company, count, _total in rows),
            "amounts": amounts,
            "action": self._action(label, "crm.lead", domain),
        }

    # ------------------------------------------------------------------ chart + feed

    @api.model
    def _weekly(self):
        """Confirmed amount per ISO week (Monday) for the last WEEKS weeks."""
        tz = self._local_tz()
        today = datetime.now(pytz.utc).astimezone(tz).date()
        monday = today - timedelta(days=today.weekday())
        weeks = [monday - timedelta(weeks=i) for i in range(WEEKS - 1, -1, -1)]
        currency = self.env.company.currency_id
        low = tz.localize(datetime.combine(weeks[0], datetime.min.time()))
        domain = [
            ("state", "=", "sale"),
            ("currency_id", "=", currency.id),
            (
                "date_order",
                ">=",
                fields.Datetime.to_string(low.astimezone(pytz.utc)),
            ),
        ]
        # Group by day and bucket to Monday here: the ":week" granularity starts on the
        # language's first weekday (Sunday for en_US), which would not match `weeks`.
        orders = self.env["sale.order"].with_context(tz=tz.zone)
        rows = orders._read_group(domain, ["date_order:day"], ["amount_total:sum"])
        totals = {}
        for day, total in rows:
            day = day.date() if isinstance(day, datetime) else day
            key = str(day - timedelta(days=day.weekday()))
            totals[key] = totals.get(key, 0.0) + (total or 0.0)
        return {
            "code": currency.name,
            "id": currency.id,
            "symbol": currency.symbol,
            "weeks": [{"start": str(w), "amount": totals.get(str(w), 0.0)} for w in weeks],
        }

    @api.model
    def _feed(self):
        sources = [
            ("sale.order", self.env._("Sale order")),
            ("stock.picking", self.env._("Transfer")),
            ("crm.lead", self.env._("Opportunity")),
        ]
        items = []
        for model, kind in sources:
            if not self._available(model):
                continue
            recs = self.env[model].search([], order="write_date desc", limit=FEED_LIMIT)
            for rec in recs:
                items.append(
                    {
                        "model": model,
                        "id": rec.id,
                        "kind": kind,
                        "name": rec.display_name,
                        "date": fields.Datetime.to_string(rec.write_date),
                    }
                )
        items.sort(key=lambda item: item["date"], reverse=True)
        return items[:FEED_LIMIT]

    # ------------------------------------------------------------------ entry point

    @api.model
    def get_dashboard_data(self, period="month"):
        if period not in ("month", "prev", "all"):
            period = "month"
        kpis = []
        if self._available("sale.order"):
            kpis += self._sale_kpis(period)
        if self._available("stock.picking"):
            kpis.append(self._delivery_kpi())
        if self._available("mail.activity"):
            kpis.append(self._activity_kpi())
        if self._available("crm.lead"):
            kpis.append(self._lead_kpi())
        return {
            "period": period,
            "kpis": kpis,
            "weekly": self._weekly() if self._available("sale.order") else None,
            "feed": self._feed(),
        }
