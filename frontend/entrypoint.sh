#!/bin/sh
JSON_STRING='window.configs = { \
  "SLIDE_API_URL":"'"${SLIDE_API_URL}"'", \
  "BASE_API_URL":"'"${BASE_API_URL}"'", \
  "SLIDE_IMAGE_URL":"'"${SLIDE_IMAGE_URL}"'" \
}'
sed -i "s@// CONFIGURATIONS_PLACEHOLDER@${JSON_STRING}@" /usr/share/nginx/html/index.html
exec "$@"