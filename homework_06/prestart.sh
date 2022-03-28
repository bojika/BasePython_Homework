#!/usr/bin/env bash

set -e
echo "Apply migrations"
#flask db init
flask db migrate -m "Create Edge Model"
flask db upgrade
echo "migrations ok"
exec "$@"


