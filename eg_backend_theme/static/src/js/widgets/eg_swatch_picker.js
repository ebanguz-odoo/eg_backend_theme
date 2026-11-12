// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { applyPreview, useRestorePreview } from "./eg_preview";

// Light-mode colors, only to draw the swatches. [fill, ring]
const SWATCHES = {
    purple: ["#71639e"],
    blue: ["#2563eb"],
    emerald: ["#047857"],
    amber: ["#b45309"],
    rose: ["#be185d"],
    contrast: ["#18181b"],
    preset: ["#f8fafc", "#cbd5e1"],
    slate: ["#f1f5f9", "#cbd5e1"],
    zinc: ["#f4f4f5", "#d4d4d8"],
    stone: ["#f5f5f4", "#d6d3d1"],
    sage: ["#e7efeb", "#b7c8bf"],
};

export class EgSwatchPicker extends Component {
    static template = "eg_backend_theme.SwatchPicker";
    static props = { ...standardFieldProps };

    setup() {
        useRestorePreview();
    }

    get options() {
        return this.props.record.fields[this.props.name].selection;
    }

    get value() {
        return this.props.record.data[this.props.name];
    }

    isSurface() {
        return this.props.name === "eg_surface";
    }

    swatchStyle(key) {
        const [fill, ring = fill] = SWATCHES[key] || SWATCHES.preset;
        return `background:${fill};border:2px solid ${ring};`;
    }

    onSelect(key) {
        this.props.record.update({ [this.props.name]: key });
        applyPreview(this.props.record, { [this.props.name]: key });
    }
}

registry.category("fields").add("eg_swatch_picker", {
    component: EgSwatchPicker,
    supportedTypes: ["selection"],
});
