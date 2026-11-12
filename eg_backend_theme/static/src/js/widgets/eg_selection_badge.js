// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import {
    badgeSelectionField,
    BadgeSelectionField,
} from "@web/views/fields/badge_selection/badge_selection_field";
import { applyPreview, useRestorePreview } from "./eg_preview";

export class EgSelectionBadge extends BadgeSelectionField {
    static template = "eg_backend_theme.SelectionBadge";

    setup() {
        super.setup();
        useRestorePreview();
        this.state = useState({ hint: false });
    }

    onChange(value) {
        super.onChange(value);
        applyPreview(this.props.record, { [this.props.name]: value });
        this.state.hint = this.props.name === "eg_scheme";
    }
}

registry.category("fields").add("eg_selection_badge", {
    ...badgeSelectionField,
    component: EgSelectionBadge,
});
