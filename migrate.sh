#!/bin/bash
echo 'CREATING DATABASE TABLES'
psql postgres -c 'CREATE EXTENSION IF NOT EXISTS "uuid-ossp";'
psql postgres -c '\i create_tables.sql'
echo 'DATABASE TABLES CREATED'
echo 'MIGRATION STARTING'
python3 migrate-most-user-data.py
echo 'MIGRATION IS FINISHED'