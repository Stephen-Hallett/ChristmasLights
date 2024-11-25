#!/bin/bash
# Check if the database file already exists
if [ ! -f /data/app.db ]; then
  echo "Initializing database..."
  sqlite3 /data/app.db < /data/schema.sql
fi