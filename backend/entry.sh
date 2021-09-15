#!/bin/sh
echo "executing entry..."

# while ! mysqladmin ping -h db --silent; do
#     echo "Waiting for MySQL"
#     sleep 1
# done

echo "starting migrations..."
alembic upgrade head
# init database

echo "seeding user data..."
python3 -m app.initial_data

echo "starting the api server..."
# start web server
/usr/bin/supervisord
