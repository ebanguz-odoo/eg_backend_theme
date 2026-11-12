==========================
EG Backend Theme - Chatter
==========================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :alt: License: LGPL-3

|badge1| |badge2|

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

Usage
=====

#. Choose any preset other than *Odoo original* in *Settings > General Settings > Backend appearance*
   or in your user preferences.
#. Open a record with a chatter (for example a quotation) and change a tracked
   field, such as the customer: the log shows the old value on a ``-`` line and the
   new value on a ``+`` line.

Credits
=======

Authors
-------

* Esteban Guzman

Contributors
------------

* Esteban Guzman <ebanguz>

Maintainers
-----------

This module is maintained by Esteban Guzman (``ebanguz``).
