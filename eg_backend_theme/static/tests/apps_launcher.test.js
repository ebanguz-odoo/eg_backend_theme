// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { afterEach, beforeEach, expect, test } from "@odoo/hoot";
import { animationFrame } from "@odoo/hoot-mock";
import {
    contains,
    defineMenus,
    getService,
    mountWithCleanup,
    patchWithCleanup,
} from "@web/../tests/web_test_helpers";
import { NavBar } from "@web/webclient/navbar/navbar";
import { EgAppsLauncher } from "@eg_backend_theme/apps_launcher/apps_launcher";

const TOGGLE = ".o_navbar_apps_menu button";

beforeEach(() => {
    defineMenus([
        { id: 1, name: "Sales" },
        { id: 2, name: "Inventory" },
        { id: 3, name: "Accounting" },
    ]);
    document.body.classList.add("eg-theme");
});

afterEach(() => {
    document.body.classList.remove("eg-theme");
});

test("the launcher is registered statically on the NavBar", () => {
    expect(NavBar.components.EgAppsLauncher).toBe(EgAppsLauncher);
});

test.tags("desktop");
test("search filters the apps", async () => {
    await mountWithCleanup(NavBar);
    await contains(TOGGLE).click();
    expect(".o_eg_app").toHaveCount(3);
    await contains(".o_eg_launcher_input").edit("inv", { confirm: false });
    expect(".o_eg_app").toHaveCount(1);
    expect(".o_eg_app_name").toHaveText("Inventory");
    await contains(".o_eg_launcher_input").edit("zzz", { confirm: false });
    expect(".o_eg_launcher_empty").toHaveCount(1);
});

test.tags("desktop");
test("Enter opens the first match", async () => {
    await mountWithCleanup(NavBar);
    patchWithCleanup(getService("menu"), {
        selectMenu(menu) {
            expect.step(menu.name);
        },
    });
    await contains(TOGGLE).click();
    await contains(".o_eg_launcher_input").edit("a", { confirm: false });
    await contains(".o_eg_launcher_input").press("Enter");
    // "Sales" is the first app whose name contains an "a"
    expect.verifySteps(["Sales"]);
    expect(".o_eg_launcher").toHaveCount(0);
});

test.tags("desktop");
test("arrow keys move the focus between search and tiles, Escape closes", async () => {
    await mountWithCleanup(NavBar);
    await contains(TOGGLE).click();
    await contains(".o_eg_launcher_input").press("ArrowDown");
    await animationFrame();
    expect(".o_eg_app:first").toBeFocused();
    await contains(".o_eg_app:first").press("ArrowUp");
    expect(".o_eg_launcher_input").toBeFocused();
    await contains(".o_eg_launcher_input").press("Escape");
    expect(".o_eg_launcher").toHaveCount(0);
});

test.tags("desktop");
test("with the theme off the native list is shown", async () => {
    document.body.classList.remove("eg-theme");
    await mountWithCleanup(NavBar);
    await contains(TOGGLE).click();
    expect(".o_eg_launcher").toHaveCount(0);
    expect(".o-dropdown--menu .dropdown-item.o_app").toHaveCount(3);
});
