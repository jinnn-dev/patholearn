#!/bin/sh
while ! mysqladmin ping -h db --silent; do
    echo "Waiting for MySQL"
    sleep 1
done
uvicorn  app.app:app --reload --host 0.0.0.0 --port 8000
