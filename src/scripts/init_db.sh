#!/bin/bash
set -e

#!/bin/bash

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" < /scripts/create_tables.sql

