# Database Backup Standard Operating Procedure (SOP)

## Overview
This SOP outlines the process for backing up databases at Northwind Systems to ensure data integrity and availability. The procedure covers the use of the AcmeDB backup tool, which is hosted on our internal server and managed by the IT Operations Team.

## Prerequisites
- **AcmeDB Tool**: Ensure that the latest version of AcmeDB is installed and configured.
- **Backup Credentials**: Obtain the necessary database credentials from the Database Administration (DBA) team.
- **Disk Space**: Verify sufficient disk space on the backup destination to accommodate new backups.
- **Network Connectivity**: Confirm network connectivity between the server running AcmeDB and the backup storage location.

## Step-by-Step Instructions

### 1. Preparation
1. **Log in to the Server**:
   - SSH into the AcmeDB server using your credentials: `ssh dbbackup@acmedb-server.northwindsystems.com`
   
2. **Check Disk Space**:
   ```bash
   df -h /path/to/backup/directory
   ```
   Ensure that there is enough free space for a new backup.

### 2. Acquiring Backup Credentials
1. Contact the Database Administration (DBA) team at `dba@northwindsystems.com` to obtain:
   - **Database Username**: `northwind_user`
   - **Database Password**: `password123!`
   - **Database Name**: `northwind_db`

### 3. Initializing AcmeDB
1. Navigate to the AcmeDB directory:
   ```bash
   cd /opt/acmedb
   ```
   
2. Initialize a backup session with the required parameters:
   ```bash
   ./acmedb-backup.sh --db-name northwind_db --user northwind_user --password password123! --destination /path/to/backup/directory
   ```

### 4. Monitoring Backup Progress
- The AcmeDB tool provides real-time logs and progress updates in the terminal.
- For more detailed monitoring, use:
   ```bash
   tail -f acmedb-backup.log
   ```

### 5. Verifying Backup Integrity
1. Once the backup is complete, verify its integrity by running a checksum on the latest backup file:
   ```bash
   sha256sum /path/to/backup/directory/latest_backup_file.sql.gz > /path/to/backup/checksum.txt
   ```
   
2. Store the checksum in a secure location for future reference.

### 6. Archiving Old Backups
- Archive old backups to offsite storage to free up local disk space.
- Use `rsync` or similar tools to transfer archives:
   ```bash
   rsync -avz /path/to/backup/directory/archives/ remote_user@offsite-storage.northwindsystems.com:/remote/path/
   ```

### 7. Documentation and Reporting
1. Document the backup process in the internal wiki under `/wiki/db-backups`.
2. Notify the IT Operations Team via email at `itops@northwindsystems.com` once the backup is complete.

## Troubleshooting

### Issue: Backup Failed with Error Message
- **Symptom**: The AcmeDB tool fails to start or encounters errors during execution.
- **Solution**:
  - Check the logs for specific error messages (`cat acmedb-backup.log`).
  - Verify network connectivity and credentials (contact DBA team if needed).
  - If issues persist, contact the IT Operations Team at `itops@northwindsystems.com`.

### Issue: Insufficient Disk Space
- **Symptom**: The backup process fails due to insufficient disk space.
- **Solution**:
  - Free up additional space on the local storage or archive old backups.
  - Increase the size of the backup directory if necessary.

### Issue: Backup Integrity Check Fails
- **Symptom**: The checksum does not match expected values.
- **Solution**:
  - Re-run the backup process to ensure data integrity.
  - If issues continue, investigate potential corruption in the database or tool configuration.

## Conclusion
Following this SOP ensures that Northwind Systems maintains a robust and reliable database backup strategy. Regularly reviewing and updating this procedure will help maintain system integrity and availability.

---

For any questions or concerns, please contact the IT Operations Team at `itops@northwindsystems.com`.