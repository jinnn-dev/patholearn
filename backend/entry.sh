#!/bin/sh
while ! mysql --host=lern_db --port=3306 -u root -p"$MYSQL_ROOT_PASSWORD" -e "show databases;" > /dev/null 2>&1; do
    echo "Waiting for MySQL..."
    sleep 1
done

echo "Running migrations..."
alembic upgrade head
# init database

echo "Creating initial data..."
python3 -m app.initial_data

echo "Starting the api server..."
# start web server
/usr/bin/supervisord
