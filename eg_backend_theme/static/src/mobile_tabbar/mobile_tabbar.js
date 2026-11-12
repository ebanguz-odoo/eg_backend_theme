// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { Component, onMounted, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { useBus, useService } from "@web/core/utils/hooks";
import { EgAppsLauncher } from "../apps_launcher/apps_launcher";

// Font Awesome icon of a menu section, guessed from its xmlid and name: first match wins.
const SECTION_ICONS = [
    [/overview|dashboard|home/, "fa-th-large"],
    [/report|analys|statistic/, "fa-bar-chart"],
    [/config|setting/, "fa-cog"],
    [/product|catalog/, "fa-cube"],
    [/invoice|bill|payment|account/, "fa-file-text-o"],
    [/customer|contact|partner|vendor|employee|applicant|people/, "fa-users"],
    [/calendar|planning|time.?off|leave|attendance/, "fa-calendar"],
    [/task|project|todo/, "fa-check-square-o"],
    [/order|sale|purchase|quotation|pipeline|lead/, "fa-shopping-bag"],
    [
        /operation|transfer|inventory|stock|manufactur|repair|maintenance/,
        "fa-truck",
    ],
];
// Sections shown as tabs; the rest go to "More" (4 sections still fit without it).
const MAX_TABS = 3;

/**
 * Bottom tab bar on small screens: Apps, then the top menus of the current app, like a
 * native mobile app. Rendered in the main components container, a flex child of the
 * body after the action manager, so it takes its own space instead of covering views.
 */
export class EgMobileTabbar extends Component {
    static template = "eg_backend_theme.MobileTabbar";
    static components = { EgAppsLauncher };
    static props = {};

    setup() {
        this.menu = useService("menu");
        this.ui = useState(useService("ui"));
        this.state = useState({ sheet: null, active: null });
        useBus(this.env.bus, "MENUS:APP-CHANGED", () => {
            this.state.sheet = null;
            this.state.active = null;
            this.render(); // the sections come from the menu service, which is not reactive
        });
        this.labels = {
            apps: _t("Apps"),
            more: _t("More"),
            close: _t("Close"),
        };
        // Browser chrome (Android address bar, installed web app) takes the navbar color
        onMounted(() => {
            const meta = document.querySelector('meta[name="theme-color"]');
            const color = getComputedStyle(document.body)
                .getPropertyValue("--eg-nav-bg")
                .trim();
            if (meta && color && document.body.classList.contains("eg-theme")) {
                meta.content = color;
            }
        });
    }

    get visible() {
        return this.ui.isSmall && document.body.classList.contains("eg-theme");
    }

    get apps() {
        return this.menu.getApps();
    }

    get sections() {
        const app = this.menu.getCurrentApp();
        return app ? this.menu.getMenuAsTree(app.id).childrenTree : [];
    }

    get tabs() {
        const sections = this.sections;
        return sections.length > MAX_TABS + 1
            ? sections.slice(0, MAX_TABS)
            : sections;
    }

    get overflow() {
        const sections = this.sections;
        return sections.length > MAX_TABS + 1 ? sections.slice(MAX_TABS) : [];
    }

    icon(section) {
        const key = `${section.xmlid || ""} ${section.name}`.toLowerCase();
        const match = SECTION_ICONS.find(([re]) => re.test(key));
        return match ? match[1] : "fa-circle-o";
    }

    onTab(section) {
        this.state.active = section.id;
        if (section.childrenTree.length) {
            this.state.sheet =
                this.state.sheet?.id === section.id ? null : section;
        } else {
            this.open(section);
        }
    }

    onMore() {
        this.state.active = "more";
        this.state.sheet =
            this.state.sheet?.id === "more"
                ? null
                : {
                      id: "more",
                      name: this.labels.more,
                      childrenTree: this.overflow,
                  };
    }

    closeSheet() {
        this.state.sheet = null;
    }

    open(menu) {
        this.state.sheet = null;
        this.menu.selectMenu(menu);
    }
}

registry.category("main_components").add("eg_backend_theme.MobileTabbar", {
    Component: EgMobileTabbar,
});
