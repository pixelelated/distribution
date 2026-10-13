# #566 provider-supported developer identity

Checked October13,2026 against ScreenScraper's [official API documentation](https://www.screenscraper.fr/webapi2.php), “Qui peut utiliser l’API ?”. The provider directs developers to its forum to introduce their application and obtain a developer identity. Developer credentials and the player's account credentials are separate API parameters.

This establishes the supported application-registration route, not approval for pixelelated to reuse another project's pair. D-QA-005/006 still describe the existing runtime fallback. #566 explicitly revisits release provisioning. No provider message was sent and no credentials were embedded or copied.

A clarification is pending: does the owner already have an approved pixelelated developer identity? No credential values are requested in chat. If not, prepare an owner-reviewable registration request describing pixelelated, its free distribution/source, inherited EmulationStation integration and intended firmware provisioning. Obtain provider-supported use/distribution details before selecting a pair. Then exercise compiled-pair precedence, ordinary-player account separation, fallback/error paths and backup exclusion using synthetic credentials first. Other M7 code and VM work need not wait for provider response.
