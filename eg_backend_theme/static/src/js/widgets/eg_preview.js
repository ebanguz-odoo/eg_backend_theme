// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { onWillUnmount } from "@odoo/owl";
import { session } from "@web/session";

// Mirrors EG_PRESET_DEFAULTS of models/eg_appearance_mixin.py, without the scheme (see applyPreview).
const PRESET_DEFAULTS = {
    aura: { surface: "slate", density: "comfy" },
    graphite: { surface: "zinc", density: "compact" },
    mineral: { surface: "sage", density: "wide" },
};
const AXES = ["accent", "surface", "density", "navbar"];

let original = null;

/**
 * Put the body classes back as the server rendered them. Called when a widget
 * goes away (discard, navigation, tab change) so a preview never outlives the form.
 */
export function restorePreview() {
    if (original !== null) {
        document.body.className = original;
        original = null;
    }
}

/** Restore the body classes when the calling widget is destroyed. */
export function useRestorePreview() {
    onWillUnmount(restorePreview);
}

/**
 * Swap the eg-* body classes to match the record being edited, so the choice is
 * visible before saving. The scheme class is never touched: the scheme bundle is
 * rendered by the server, so a scheme change only applies after a reload.
 *
 * @param {Object} record form record holding the eg_* fields
 * @param {Object} [changes] values not yet written to the record
 */
export function applyPreview(record, changes = {}) {
    if (!session.eg_theme_available) {
        return;
    }
    const data = { ...record.data, ...changes };
    const body = document.body;
    original ??= body.className;
    const scheme = [...body.classList].find((cls) =>
        cls.startsWith("eg-scheme-"),
    );
    body.classList.remove(
        ...[...body.classList].filter((cls) => cls.startsWith("eg-")),
    );
    const preset = data.eg_preset || "aura";
    if (preset === "odoo") {
        return;
    }
    const values = { preset, ...PRESET_DEFAULTS[preset] };
    for (const axis of AXES) {
        const value = data[`eg_${axis}`];
        if (value && value !== "preset") {
            values[axis] = value;
        }
    }
    values.accent ||= "purple";
    values.navbar ||= "surface";
    body.classList.add("eg-theme", scheme || "eg-scheme-light");
    for (const [axis, value] of Object.entries(values)) {
        body.classList.add(`eg-${axis}-${value}`);
    }
}
