#!/usr/bin/env bash

set -e

echo "Running database migrations..."
psql -a -d $DATABASE_URL -f database.sql

echo "Migration finished"