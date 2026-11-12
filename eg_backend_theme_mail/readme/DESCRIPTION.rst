Styles the chatter of the **EG Backend Theme** with the theme tokens: messages
connected by a vertical line (timeline) with the body in a card, themed
composer, activities, followers and attachments, and field tracking changes
shown as a diff (old value with ``-``, new value with ``+``).

It only adds SCSS: no template or JavaScript is patched, so the native
behaviour of the chatter is unchanged (including its position: beside the form
from 1400 px, below it on narrower screens). It installs automatically when
``eg_backend_theme`` and ``mail`` are both installed, and uninstalling it
leaves the rest of the theme untouched. With the "Odoo original" preset the
styles are not applied.
