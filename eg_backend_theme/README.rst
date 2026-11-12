================
EG Backend Theme
================

.. |badge1| image:: https://img.shields.io/badge/maturity-Beta-yellow.png
    :alt: Beta
.. |badge2| image:: https://img.shields.io/badge/licence-LGPL--3-blue.png
    :alt: License: LGPL-3

|badge1| |badge2|

A modern look for the Odoo Community backend, built on design tokens instead of
patched templates. Pick a style (*Aura*, *Graphite*, *Mineral* or the original
Odoo look), an accent color, a surface tint, a light, dark or system color
scheme, a row density, the navigation bar tone and whether form labels sit
beside their fields (as in Odoo) or above them.

The administrator sets the company appearance and decides whether users may
customize it. Users can follow the company or choose their own look from their
preferences, with a live preview while choosing. A light/dark toggle sits in
the systray, and the apps menu becomes a searchable launcher with keyboard
navigation.

On phones the backend behaves like a native app: a bottom tab bar with the apps
launcher and the menus of the current app (extra menus in a bottom sheet), card
lists, edge-to-edge forms and 16px inputs so iOS does not zoom while typing.

The theme is applied from the server through body classes, so there is no flash
of unstyled content. With the *Odoo original* style the theme is fully off. The
login page, portal, website and reports are not touched. If ``web_enterprise``
is installed the module does nothing.

Usage
=====

**Company appearance**

#. Go to *Settings > General Settings > Backend appearance*.
#. Choose the style, accent color, surface tint, color scheme, density and
   navigation bar. Choose *Odoo original* to turn the theme off.
#. Untick *Allow users to customize* to lock the appearance for everyone.

**Personal appearance**

#. Open the user menu and click *Appearance* (or *Preferences > Appearance*).
#. Switch off *Use company appearance* and pick your own options. The page
   previews each choice; the color scheme applies after the page reloads.
#. Use the moon/sun button in the top bar to switch between light and dark.

**Apps launcher**

#. Click the apps icon (or press ``h``), type to filter, use the arrow keys and
   press Enter to open the first match.

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
