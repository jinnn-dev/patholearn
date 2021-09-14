#!/bin/sh
mkdir -p "/data/slide"
while ! mysqladmin ping -h db --silent; do
    echo "Waiting for MySQL"
    sleep 1
done
# init database
python3 -m app.initial_data
# start web server
/usr/bin/supervisord