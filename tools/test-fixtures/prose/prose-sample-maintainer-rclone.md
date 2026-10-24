## Cloud Sync with rclone

This guide provides instructions on configuring and using `rclone` for syncing game saves, states, screenshots, and system backups to the cloud.

### Step 1: Enable Network and SSH Access

Before configuring `rclone`, ensure your device is connected to the network and SSH access is enabled:

1. **Enable Networking**:
   - Press `START` on your device to open the Main Menu.
   - Navigate to `Network Settings`.
   - Set `Enable Network` to `ON`.
   - Select your `WIFI SSID` and enter your `WIFI Key`.
   - Exit the menu to apply settings.

2. **Enable SSH**:
   - In `Network Settings`, set `Enable SSH` to `ON`.
   - Retrieve the `root` password from the `System Settings` menu under `Security`.

3. **Access via SSH**:
   - Use an SSH client (e.g., PowerShell on Windows, Terminal on macOS/Linux) to connect:
     ```bash
     ssh root@<device_ip_address>
     ```
   - Enter the `root` password when prompted.

### Step 2: Configure rclone

With SSH access established, configure `rclone` to connect to your cloud storage provider:

1. **Start rclone Configuration**:
   ```bash
   rclone config
   ```
   - Follow the interactive prompts to set up a new remote.
   - Refer to the [rclone provider documentation](https://rclone.org/remote_setup/) and [headless configuration guide](https://rclone.org/remote_setup/#configuring-by-copying-the-config-file) for detailed instructions.

### Step 3: Understanding `cloud_sync.conf`

The `cloud_sync.conf` file contains essential settings for configuring your backup and restore operations:

- **`BACKUPPATH`**: Local directory containing game saves and screenshots.
- **`RESTOREPATH`**: Local directory where restored data will be placed.
- **`SYNCPATH`**: Remote cloud directory for syncing.
- **`BACKUPFOLDER`**: Local directory for system backup files.
- **`SYNCPATH_BACKUP`**: Remote directory for system backup files.

Additional options:

- **`RCLONEOPTS`**: Options for logging, filters, and verbosity during sync operations.
- **`BACKUPMETHOD`**: "sync" mirrors local files exactly; "copy" updates remote without deleting.
- **`BACKUPFILE_BACKUP_OPTION`**: Include ("yes") or exclude ("no") system backup files.
- **`RESTOREMETHOD`**: "copy" preserves existing local files; "sync" overwrites them.
- **`BACKUPFILE_RESTORE_OPTION`**: Include ("yes") or exclude ("no") system backup files during restore.
- **`RSYNCRMDIR`**: Automatically remove empty remote directories ("yes" to enable).

### Step 4: Using Cloud Backup and Restore

ROCKNIX provides built-in tools for cloud backup and restore operations:

1. **Access Tools**:
   - Navigate to the `Tools` menu in the user interface.
   - Select `Cloud Backup` to back up your save games and states (and system backup if enabled).
   - Select `Cloud Restore` to restore data from the cloud, per your `.conf` file settings.

2. **Configuration Files**:
   - These tools are configurable by editing `/storage/.config/cloud_sync.conf` and `/storage/.config/cloud_sync-rules.txt`. Be careful when modifying the rules. Changes ma have unintended consequences. If you do make chages, you may want to try a dry run first.

#### Step 5: Logs and Troubleshooting

Monitor sync logs for troubleshooting and/or more insight into rclone's activity:

```bash
tail -f /var/log/cloud_sync.log
```

If you run into any issues, please share details in the appropriate channel in Discord.

