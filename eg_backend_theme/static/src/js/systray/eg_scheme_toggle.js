// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { Component, onWillStart, useState } from "@odoo/owl";
import { browser } from "@web/core/browser/browser";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";
import { useService } from "@web/core/utils/hooks";

const COMPANY_FIELDS = [
    "eg_preset",
    "eg_accent",
    "eg_surface",
    "eg_scheme",
    "eg_density",
    "eg_navbar",
    "eg_labels",
];

export class EgSchemeToggle extends Component {
    static template = "eg_backend_theme.SchemeToggle";
    static props = {};

    setup() {
        this.orm = useService("orm");
        this.state = useState({ allowed: false });
        onWillStart(async () => {
            const [company] = await this.orm.read(
                "res.company",
                [user.activeCompanies[0].id],
                ["eg_allow_user"],
            );
            this.state.allowed = company.eg_allow_user;
        });
    }

    get isDark() {
        return document.body.classList.contains("eg-scheme-dark");
    }

    get title() {
        return this.isDark
            ? _t("Switch to light mode")
            : _t("Switch to dark mode");
    }

    async toggle() {
        const [me] = await this.orm.read(
            "res.users",
            [user.userId],
            ["eg_follow_company"],
        );
        const values = {
            eg_scheme: this.isDark ? "light" : "dark",
            eg_follow_company: false,
        };
        if (me.eg_follow_company) {
            // Start from what the user sees now: the company appearance.
            const [company] = await this.orm.read(
                "res.company",
                [user.activeCompanies[0].id],
                COMPANY_FIELDS,
            );
            const { id, ...appearance } = company;
            Object.assign(values, appearance, { eg_scheme: values.eg_scheme });
        }
        await this.orm.write("res.users", [user.userId], values);
        browser.location.reload();
    }
}

registry.category("systray").add(
    "eg_backend_theme.SchemeToggle",
    {
        Component: EgSchemeToggle,
        isDisplayed: () => document.body.classList.contains("eg-theme"),
    },
    { sequence: 5 },
);
