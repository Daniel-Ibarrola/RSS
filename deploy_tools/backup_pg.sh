#!/bin/bash

DB_USER="your_db_user"
DB_NAME="your_db_name"
DB_HOST="localhost"
DB_PORT="5432"

BACKUP_DIR="/path/to/backup/directory"
TIMESTAMP=$(date +"%Y%m%d%H%M%S")

BACKUP_FILENAME="backup_$TIMESTAMP.sql"
BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILENAME"

S3_BUCKET="my-bucket"
AWS_S3_CMD="/usr/local/bin/aws s3"

pg_dump -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -F c -b -v -f "$BACKUP_FILE" "$DB_NAME"

# Check the exit status of pg_dump
if [ $? -eq 0 ]; then
    echo "Database backup completed successfully at $(date +'%Y-%m-%d %H:%M:%S')."

    # Upload the backup to S3
    $AWS_S3_CMD cp "$BACKUP_FILE" "s3://$S3_BUCKET"

    # Check the exit status of the AWS S3 command
    if [ $? -eq 0 ]; then
        echo "Backup uploaded to S3 successfully."
    else
        echo "Failed to upload backup to S3."
    fi

    # Remove the local backup file to save space
     rm "$BACKUP_FILE"

else
    echo "Database backup failed at $(date +'%Y-%m-%d %H:%M:%S')."
fi
