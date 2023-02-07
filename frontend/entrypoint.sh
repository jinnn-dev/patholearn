#!/bin/sh
JSON_STRING='window.configs = { \
  "SLIDE_API_URL":"'"${SLIDE_API_URL}"'", \
  "BASE_API_URL":"'"${BASE_API_URL}"'", \
  "APP_TITLE":"'"${APP_TITLE}"'", \
  "APP_LOGO_URL":"'"${APP_LOGO_URL}"'", \
  "APP_FAVICON_URL":"'"${APP_FAVICON_URL}"'", \
  "SLIDE_IMAGE_URL":"'"${SLIDE_IMAGE_URL}"'", \
  "FRONTEND_VERSION":"'"${FRONTEND_VERSION}"'", \
  "VITE_SENTRY_DSN":"'"${VITE_SENTRY_DSN}"'" \
  "VITE_SENTRY_ENVIRONMENT":"'"${VITE_SENTRY_ENVIRONMENT}"'" \
}'
sed -i "s@// CONFIGURATIONS_PLACEHOLDER@${JSON_STRING}@" /usr/share/nginx/html/index.html
exec "$@"