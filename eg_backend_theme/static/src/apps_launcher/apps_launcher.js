// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { Component, useRef, useState } from "@odoo/owl";
import { Dropdown } from "@web/core/dropdown/dropdown";
import { DropdownItem } from "@web/core/dropdown/dropdown_item";
import { useDropdownState } from "@web/core/dropdown/dropdown_hooks";
import { _t } from "@web/core/l10n/translation";
import { useService } from "@web/core/utils/hooks";
import { NavBar } from "@web/webclient/navbar/navbar";

export class EgAppsLauncher extends Component {
    static template = "eg_backend_theme.AppsLauncher";
    static components = { Dropdown, DropdownItem };
    // label: text under the icon (mobile tab bar); the launcher then opens upwards
    static props = { apps: Array, label: { type: String, optional: true } };

    setup() {
        this.menuService = useService("menu");
        this.state = useState({ query: "" });
        this.dropdown = useDropdownState({
            onClose: () => (this.state.query = ""),
        });
        // The input lives in the Dropdown popover, so useAutofocus never sees it mount.
        this.searchRef = useRef("search");
        this.placeholder = _t("Search applications");
    }

    // With the theme off (preset "Odoo original") the menu falls back to the native list.
    get isThemed() {
        return document.body.classList.contains("eg-theme");
    }

    onOpened() {
        // On phones the keyboard would cover the grid
        if (!this.env.isSmall) {
            this.searchRef.el?.focus();
        }
    }

    get filteredApps() {
        const query = this.state.query.trim().toLowerCase();
        return this.props.apps.filter(
            (app) => !query || app.name.toLowerCase().includes(query),
        );
    }

    get currentApp() {
        return this.menuService.getCurrentApp();
    }

    getHref(app) {
        return `/odoo/${app.actionPath || "action-" + app.actionID}`;
    }

    getInitial(app) {
        return (app.name || "?").trim().charAt(0).toUpperCase();
    }

    openApp(app) {
        this.dropdown.close();
        this.menuService.selectMenu(app);
    }

    onClickApp(ev, app) {
        // keep the native behaviour for ctrl/cmd/middle clicks (open in a new tab)
        if (ev.ctrlKey || ev.metaKey || ev.shiftKey || ev.button === 1) {
            return;
        }
        ev.preventDefault();
        this.openApp(app);
    }

    onKeydownSearch(ev) {
        if (ev.key === "Enter") {
            ev.preventDefault();
            ev.stopPropagation(); // keep the Dropdown navigator from also acting on the key
            const [first] = this.filteredApps;
            if (first) {
                this.openApp(first);
            }
        } else if (ev.key === "ArrowDown") {
            ev.preventDefault();
            ev.stopPropagation();
            this.focusApp(0);
        }
    }

    onKeydownGrid(ev) {
        const items = [...ev.currentTarget.querySelectorAll(".o_eg_app")];
        const index = items.indexOf(ev.target);
        if (index < 0) {
            return;
        }
        const columns = getComputedStyle(
            ev.currentTarget,
        ).gridTemplateColumns.split(" ").length;
        const delta = {
            ArrowRight: 1,
            ArrowLeft: -1,
            ArrowDown: columns,
            ArrowUp: -columns,
        }[ev.key];
        if (!delta) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation(); // 2D movement replaces the Dropdown's linear arrow navigation
        const target = index + delta;
        if (target < 0) {
            // leaving the grid by the top goes back to the search box
            this.searchRef.el?.focus();
        } else {
            this.focusApp(Math.min(items.length - 1, target), items);
        }
    }

    focusApp(index, items) {
        const list =
            items || document.querySelectorAll(".o_eg_launcher .o_eg_app");
        list[index]?.focus();
    }
}

NavBar.components = { ...NavBar.components, EgAppsLauncher };
