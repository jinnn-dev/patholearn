import os


class Config:
    CLEARML_API = os.environ.get("CLEARML_API", "")
    CLEARML_API_ACCESS_KEY = os.environ.get("CLEARML_API_ACCESS_KEY", "")
    CLEARML_API_SECRET_KEY = os.environ.get("CLEARML_API_SECRET_KEY", "")

    SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
    SENTRY_ENVIRONMENT = os.environ.get("SENTRY_ENVIRONMENT", "")
