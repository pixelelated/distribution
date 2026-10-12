# Retained cloud configuration diagnosis — #569

The reported save-action availability is consistent with an existing configured
backend and preserved legacy paths. Local sign-in completion and a recent
connection-check success were found. Neither a configuration file nor its
modification time alone proves authentication or who entered the account.

The exact accepted ES source c8dc72cf9e builds these action rows using the
uncached existence of rclone.conf (GuiMenu.cpp:6118, 6127–6144; the shared
row helper at6280). This gate does not contact a provider. The connection
selector preserves a legacy first remote when active-connection is absent
(cloud_connections.py:active). D-CLOUD-175/178/179 intentionally preserve
existing folder choices. The update does not change them to current defaults.

The October9 and October12 accepted update preservation receipts independently
show existing configuration retained. No evidence here establishes firmware
seeded that sign-in. Credential values, private folder selections and original
incident text remain in the restricted incident packet; this public record is
value-free. No provider request, mutation, screenshot or input was performed.
No product repair or VM execution is claimed for this diagnostic read.

If the owner elects to align folders, inspect the intended destination first and
obtain named settings-change authority. Linking, checking and selecting folders
are distinct; none authorizes a bulk move. #565 owns the broader firmware gate.
