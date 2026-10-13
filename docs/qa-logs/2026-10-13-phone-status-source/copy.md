# Exact copy and EN/FR review needs

Source uses the existing handheld-inherited `signin_language()` selection, not
the phone's browser language. Unknown locales keep the existing English fallback.
`phone_page()` sets the HTML language and status dictionary together. Service
names are retained, HTML-escaped, never translated, and available in full in the
heading title/accessibility tree even when the visible line ellipsizes.

The accessible button name and live announcement combine the state label, a
period, and its detail. The details panel contains the detail alone. “Checking
connection” is initial markup before the first response.

| Context | English | French |
| --- | --- | --- |
| Document title, heading, heading title | Keyboard for {service} | Clavier pour {service} |
| Initial button name/title and detail | Checking connection | Vérification de la connexion |
| Connected label | Connected | Connecté |
| Disconnected label | Disconnected | Déconnecté |
| Warning label | Warning | Attention |
| Hide details | Hide status | Masquer l’état |
| Field ready | The keyboard is ready. | Le clavier est prêt. |
| Loading with control window present | Opening on your handheld. You can keep typing here; it goes across once a box on that page is ready. | La page s’ouvre sur votre console. Vous pouvez continuer à saisir ici ; le texte sera envoyé dès qu’un champ de la page sera prêt. |
| No control window observed yet | Not open yet. Choose CONTINUE on your handheld. You can type or paste here meanwhile; it goes across when the page opens. | La page n’est pas encore ouverte. Choisissez CONTINUER sur votre console. Vous pouvez saisir ou coller du texte ici ; il sera envoyé à l’ouverture de la page. |
| Control window no longer present | The sign-in page is closed. Start sign-in again on your handheld if you still need it. | La page de connexion est fermée. Relancez la connexion sur votre console si nécessaire. |
| Probe failure, before threshold | Checking the connection to your handheld again. | Nouvelle vérification de la connexion à votre console. |
| Five failed probes | Your phone can't reach your handheld. Both need to be on the same Wi-Fi, and a VPN on your phone can get in the way. If sign-in has ended, you can close this phone page. | Votre téléphone ne peut pas joindre votre console. Les deux doivent être sur le même réseau Wi-Fi. Un VPN sur votre téléphone peut bloquer la connexion. Si la connexion au service est terminée, vous pouvez fermer cette page sur votre téléphone. |
| Script failure, followed by browser-supplied error text | This page stopped working. Reload it; if it happens again, report it to the pixelelated project: {error} | Cette page ne fonctionne plus. Rechargez-la ; si le problème persiste, signalez-le au projet pixelelated : {error} |

Review needs **UNRUN**: narrow/wide EN/FR heading clipping, glyph legibility and
name/description announcement; reveal/Hide/Escape keyboard order; all failure
details readable without outer-page movement; screen-reader live announcements
not repeated per poll. Confirm the existing native CONTINUE / CONTINUER labels
against the coordinator's exact ES pin during flow review. No ES source changed.

Preserved copy: Close page / Fermer la page, Keep / Garder ouverte, Close / Fermer,
and the existing Close question. Input labels, pointer explanation, network-trust
warning, and unsupported-character feedback retain their previous locale behavior
(several remain English in the existing French companion page). This packet
translates the new status/header surface; it is not a claim of full French-page
localization. Frames must show that boundary rather than disguise it.
