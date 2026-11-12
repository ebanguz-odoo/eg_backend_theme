import { Component, onWillStart, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";
import { formatCurrency } from "@web/core/currency";
import { deserializeDateTime, formatDateTime } from "@web/core/l10n/dates";
import { useService } from "@web/core/utils/hooks";

const CHART_W = 300;
const CHART_H = 110;

export class EgOpsPanel extends Component {
    static template = "eg_ops_panel.Dashboard";
    static props = ["*"];

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ period: "month", data: null, loading: true });
        this.periods = [
            { key: "month", label: _t("This month") },
            { key: "prev", label: _t("Last month") },
            { key: "all", label: _t("All time") },
        ];
        onWillStart(() => this.load());
    }

    async load(period = this.state.period) {
        this.state.loading = true;
        const data = await this.orm.call("eg.ops.panel", "get_dashboard_data", [
            period,
        ]);
        this.state.period = period;
        this.state.data = data;
        this.state.loading = false;
    }

    /** Server sends UTC strings; show them in the user's timezone and format. */
    formatDate(value) {
        return formatDateTime(deserializeDateTime(value));
    }

    formatCount(count) {
        return count.toLocaleString(user.lang?.replace("_", "-"));
    }

    formatAmount(amount) {
        // Odoo's own formatter: symbol position and separators follow the currency and language
        return formatCurrency(amount.total, amount.id, { digits: [16, 0] });
    }

    /** Amounts of other currencies are listed apart, never converted. */
    mainAmount(kpi) {
        return kpi.amounts.find((a) => a.main);
    }

    otherAmounts(kpi) {
        return kpi.amounts.filter((a) => !a.main);
    }

    /** Percent change vs the previous period, or null when there is no base. */
    deltaPct(kpi) {
        const prev = kpi.previous?.count;
        if (!prev) {
            return null;
        }
        return Math.round(((kpi.count - prev) / prev) * 100);
    }

    // role="button" cards: Enter and Space activate, like a native button
    onKpiKeydown(ev, kpi) {
        if (ev.key === "Enter" || ev.key === " ") {
            ev.preventDefault();
            this.openKpi(kpi);
        }
    }

    openKpi(kpi) {
        this.action.doAction(kpi.action);
    }

    openRecord(item) {
        this.action.doAction({
            type: "ir.actions.act_window",
            res_model: item.model,
            res_id: item.id,
            views: [[false, "form"]],
        });
    }

    get bars() {
        const weekly = this.state.data?.weekly;
        if (!weekly) {
            return [];
        }
        const max = Math.max(...weekly.weeks.map((w) => w.amount), 1);
        const slot = CHART_W / weekly.weeks.length;
        return weekly.weeks.map((week, i) => {
            const height = Math.round((week.amount / max) * (CHART_H - 20));
            return {
                x: i * slot + slot * 0.2,
                width: slot * 0.6,
                y: CHART_H - height,
                height,
                label: week.start.slice(5),
                title: `${week.start}: ${this.formatAmount({
                    total: week.amount,
                    id: weekly.id,
                })}`,
            };
        });
    }

    get chartBox() {
        return `0 0 ${CHART_W} ${CHART_H + 16}`;
    }
}

registry.category("actions").add("eg_ops_panel.dashboard", EgOpsPanel);
