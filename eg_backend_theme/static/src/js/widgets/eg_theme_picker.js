// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";
import { applyPreview, useRestorePreview } from "./eg_preview";

// Mini preview colors per preset. nav, canvas, surface, accent, radius (px)
const PREVIEWS = {
    odoo: {
        nav: "#71639e",
        canvas: "#f9fafb",
        surface: "#ffffff",
        accent: "#71639e",
        radius: 2,
    },
    aura: {
        nav: "#ffffff",
        canvas: "#f8fafc",
        surface: "#ffffff",
        accent: "#71639e",
        radius: 6,
    },
    graphite: {
        nav: "#18181b",
        canvas: "#09090b",
        surface: "#18181b",
        accent: "#b4a9e6",
        radius: 4,
    },
    mineral: {
        nav: "#fcfefd",
        canvas: "#f3f7f5",
        surface: "#fcfefd",
        accent: "#047857",
        radius: 10,
    },
};

export class EgThemePicker extends Component {
    static template = "eg_backend_theme.ThemePicker";
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

    preview(key) {
        const { nav, canvas, surface, accent, radius } =
            PREVIEWS[key] || PREVIEWS.aura;
        return {
            frame: `background:${canvas};border-radius:${radius}px;height:64px;width:120px;`,
            nav: `background:${nav};height:12px;`,
            card: `background:${surface};border-radius:${radius}px;`,
            accent: `background:${accent};border-radius:${radius}px;`,
        };
    }

    onSelect(key) {
        this.props.record.update({ [this.props.name]: key });
        applyPreview(this.props.record, { [this.props.name]: key });
    }
}

registry.category("fields").add("eg_theme_picker", {
    component: EgThemePicker,
    supportedTypes: ["selection"],
});
