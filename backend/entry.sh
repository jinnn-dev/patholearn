#!/bin/sh

echo "HOST: $MYSQL_HOST"
echo "PASSWORD: $MYSQL_ROOT_PASSWORD"
echo "DATABASE: $MYSQL_DATABASE"

while ! mysql --host=$MYSQL_HOST --port=3306 -u root -p"$MYSQL_ROOT_PASSWORD" -e "show databases;" > /dev/null 2>&1; do
    echo "Waiting for MySQL..."
    sleep 1
done

echo "Initializing databases..."
mysql --host=$MYSQL_HOST --port=3306 -u root -p"$MYSQL_ROOT_PASSWORD" -e "create database if not exists ${MYSQL_DATABASE};"

echo "Running migrations..."
alembic upgrade head

echo "Creating initial data..."
python3 -m app.initial_data

echo "Starting the api server..."
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf
