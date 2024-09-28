#!/usr/bin/env bash

set -e

echo "Running make install..."
make install

echo "Running database migrations..."
psql -a -d $DATABASE_URL -f database.sql

echo "Build finished"