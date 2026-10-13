# Exact companion-keyboard copy additions

English visible text is preserved. New English accessible names are identified
below. Status/header and Close/Keep strings retain the accepted phone-status
packet's translations. Service names and browser-supplied diagnostic text are data.

| Control/context | English | French |
| --- | --- | --- |
| Input placeholder | Type here | Saisissez ici |
| Input accessible name (new) | Text to type on your handheld | Texte à saisir sur votre console |
| Backspace button | Back | ⌫ |
| Backspace accessible name (new) | Backspace | Effacer un caractère |
| Tab button | Tab | Tab |
| Tab accessible name | Tab (button text) | Tabulation |
| Enter button | Enter | ↵ |
| Enter accessible name (explicit) | Enter | Entrée |
| Clear local field | Clear | Vider |
| Reveal local field | Show | Voir |
| Mask local field | Hide | Cacher |
| Left arrow accessible name (new) | Left arrow | Flèche gauche |
| Up arrow accessible name (new) | Up arrow | Flèche haut |
| Down arrow accessible name (new) | Down arrow | Flèche bas |
| Right arrow accessible name (new) | Right arrow | Flèche droite |
| Scroll up button | Page up | Monter |
| Scroll up accessible name | Page up (button text) | Faire défiler vers le haut |
| Scroll down button | Page down | Descendre |
| Scroll down accessible name | Page down (button text) | Faire défiler vers le bas |
| Pointer heading | Pointer | Pointeur |
| Pointer instruction | drag to move · tap to click | glissez pour déplacer · touchez pour cliquer |

English note (unchanged; source newlines collapse into spaces):

> The sign-in page is on your handheld’s screen, not here. This types for it, so you can more easily retrieve and type your login info. What you type crosses your network unencrypted, so use this on a network you trust.

French note:

> La page de connexion est sur l’écran de votre console, pas ici. Ce clavier vous permet d’y saisir vos identifiants plus facilement. Le texte saisi traverse votre réseau sans chiffrement. Utilisez un réseau de confiance.

| Warning | English | French |
| --- | --- | --- |
| Masked, one dropped unit | The handheld can't type one of the characters you entered, so it was left out. | La console ne peut pas saisir un des caractères entrés. Il a été ignoré. |
| Masked, multiple dropped units | The handheld can't type {count} of the characters you entered, so they were left out. | La console ne peut pas saisir {count} des caractères entrés. Ils ont été ignorés. |
| Revealed, one dropped unit | The handheld can't type {characters}, so it was left out. | La console ne peut pas saisir {characters}. Ce caractère a été ignoré. |
| Revealed, multiple dropped units | The handheld can't type {characters}, so they were left out. | La console ne peut pas saisir {characters}. Ces caractères ont été ignorés. |

`{count}` is the existing dropped-array length. `{characters}` is the existing
space-joined dropped array and is substituted **only in the revealed branch**.
Neither placeholder is visible literally in a normal warning. Zero dropped units
hide the warning. Messages keep the existing UTF-16 counting/filtering semantics.

The French first row stays at the existing 16 px font size. Symbols shorten its
Backspace and Enter controls without abbreviating their accessible names; only
French flex sizing changes to make room for Vider and Cacher. Rendering, text-size
zoom, symbol availability, screen-reader speech, and 320 px fit are **UNRUN**.
