// Copyright 2026 Esteban Guzman
// License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";

function egAppearanceItem(env) {
    return {
        type: "item",
        id: "eg_appearance",
        description: _t("Appearance"),
        callback: async () => {
            const action = await env.services.orm.call(
                "res.users",
                "action_get",
            );
            action.res_id = user.userId;
            env.services.action.doAction(action);
        },
        sequence: 55,
    };
}

registry.category("user_menuitems").add("eg_appearance", egAppearanceItem);
