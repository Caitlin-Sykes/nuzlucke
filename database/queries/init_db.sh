#!/bin/sh
set -e

SCHEMA_DIR="/schema_files"

echo "--- Starting Ordered SQL Initialization ---"

# -V (version sort) handles numbers like a human would (1, 2, 10)
# -type f ensures we don't try to "execute" a directory
find "$SCHEMA_DIR" -type f -name "*.sql" | sort -V | while read -r file; do
    echo "Applying migration: $file"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$file"
done

echo "--- All SQL migrations applied successfully ---"