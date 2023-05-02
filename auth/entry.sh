#!/bin/bash
echo "Creating auth user"
curl --location --request POST 'http://supertokens:3567/recipe/dashboard/user' -H 'rid: dashboard' -H 'Content-Type: application/json' -d @- <<EOF
{ "email": "$DASHBOARD_EMAIL", "password": "$DASHBOARD_PASSWORD"}
EOF
echo "Starting the auth server..."
/usr/bin/supervisord -c /etc/supervisor/conf.d/supervisord.conf