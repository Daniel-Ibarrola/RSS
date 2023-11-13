#!/bin/bash

# Backup the postgres database. This script can be run as a cron job

DB_USER="rss"
DB_NAME="rss"

BACKUP_DIR="/pg_backup"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

BACKUP_FILENAME="backup_$TIMESTAMP.dump"
BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILENAME"

docker compose exec postgres pg_dump -U "$DB_USER" -F c -b -v -f "$BACKUP_FILE" "$DB_NAME"

if [ $? -eq 0 ]; then
    echo "Database backup completed successfully at $(date +'%Y-%m-%d %H:%M:%S')."

    BACKUP_FILE="../../../$BACKUP_DIR/$BACKUP_FILENAME"
    S3_BUCKET="cap-rss-pg-backups"
    /usr/local/bin/aws s3 cp "$BACKUP_FILE" "s3://$S3_BUCKET"

    if [ $? -eq 0 ]; then
        echo "Backup uploaded to S3 successfully."
    else
        echo "Failed to upload backup to S3."
    fi

    rm "$BACKUP_FILE"

else
    echo "Database backup failed at $(date +'%Y-%m-%d %H:%M:%S')."
fi