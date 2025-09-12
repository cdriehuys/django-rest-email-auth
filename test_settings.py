DATABASES = {
    "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}
}

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_email_auth",
]

SECRET_KEY = "secret"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": []},
    }
]


ROOT_URLCONF = "test_urls"

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Basic settings required for the app
REST_EMAIL_AUTH = {
    "EMAIL_VERIFICATION_URL": "https://example.com/verify/{key}",
    "PASSWORD_RESET_URL": "https://example.com/reset/{key}",
}
