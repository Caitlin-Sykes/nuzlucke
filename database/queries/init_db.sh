#!/bin/sh
set -e

DB_USER="$POSTGRES_USER"
DB_NAME="$POSTGRES_DB"
INIT_DIR="/docker-entrypoint-initdb.d"
PYTHON_SCRIPT_PATH="/app/src/main.py"

cat << EOF
--- Starting Custom Schema & Data Initialization ---
This is necessary due to wanting to keep the
the nested folder structure inside the database/queries
---
EOF

# Wait for the PostgreSQL server to be fully ready
until pg_isready -U "$DB_USER"; do
  echo "Waiting for PostgreSQL..."
  sleep 2
done
echo "PostgreSQL is ready. Proceeding with SQL scripts."

# Execute ALL SQL files in alphabetical order (e.g., 00/ -> 01/ -> 02/)
# Finds files in subdirectories, sorts them, executes
find "$INIT_DIR" -type f -name "*.sql" | sort | while read -r file; do
    if [ -n "$file" ]; then
        echo "Executing SQL: $file"
        # -v ON_ERROR_STOP=1 halts execution on any error
        psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "$DB_NAME" -f "$file"
    fi
done

# Execute all ETL/Script files (e.g., Python scripts for dynamic data)
echo "Starting ETL/Script execution..."

if [ -f "$PYTHON_SCRIPT_PATH" ]; then
    echo "Executing Python script: $PYTHON_SCRIPT_PATH"
    python3 "$PYTHON_SCRIPT_PATH"
else
    echo "CRITICAL ERROR: Main Python script not found at $PYTHON_SCRIPT_PATH"
fi

echo "--- Initialization complete. ---"

