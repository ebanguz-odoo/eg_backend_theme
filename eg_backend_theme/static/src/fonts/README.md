# Bundled fonts

Served from this folder only; nothing is loaded from a CDN at runtime.

| Family                         | Package                      | Version | Files                                                                            | License                              |
| ------------------------------ | ---------------------------- | ------- | -------------------------------------------------------------------------------- | ------------------------------------ |
| Inter (variable, wght 100-900) | `@fontsource-variable/inter` | 5.3.0   | `inter-latin-wght-normal.woff2`, `inter-latin-ext-wght-normal.woff2`             | SIL OFL 1.1, `OFL-Inter.txt`         |
| JetBrains Mono (400, 500)      | `@fontsource/jetbrains-mono` | 5.3.0   | `jetbrains-mono-latin-400-normal.woff2`, `jetbrains-mono-latin-500-normal.woff2` | SIL OFL 1.1, `OFL-JetBrainsMono.txt` |

Fetched once from `https://cdn.jsdelivr.net/npm/<package>@5.3.0/files/<file>` (licenses from `<package>@5.3.0/LICENSE`).
The `@font-face` rules live in `../scss/fonts.scss`. To update, download the new files, change the versions above and
keep the `unicode-range` values in sync with the package CSS.
