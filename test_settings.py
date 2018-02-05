DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'rest_email_auth',
]

SECRET_KEY = 'secret'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [],
        },
    },
]


ROOT_URLCONF = 'test_urls'


# Basic settings required for the app
REST_EMAIL_AUTH = {
    'EMAIL_VERIFICATION_URL': 'https://example.com/verify/{key}',
    'PASSWORD_RESET_URL': 'https://example.com/reset/{key}',
}
