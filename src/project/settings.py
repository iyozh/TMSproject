"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 3.0.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from itertools import chain
from pathlib import Path

import dj_database_url
import sentry_sdk
from django.urls import reverse_lazy
from dynaconf import settings as _ds
from sentry_sdk.integrations.django import DjangoIntegration

BASE_DIR = Path(__file__).parent.parent
PROJECT_DIR = BASE_DIR / "project"
REPO_DIR = BASE_DIR.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _ds.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _ds.DEBUG

sentry_sdk.init(
    dsn=_ds.SENTRY_DSN,
    integrations=[DjangoIntegration()],
    traces_sample_rate=1.0,
    send_default_pii=True,
)

INTERNAL_IPS = ["127.0.0.1"]
INTERNAL_HOSTS = ["localhost"]
ALLOWED_HOSTS = list(chain(_ds.ALLOWED_HOSTS or [], INTERNAL_IPS, INTERNAL_HOSTS))

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "applications.goodbye.apps.GoodbyeConfig",
    "applications.resume.apps.ResumeConfig",
    "applications.projects.apps.ProjectsConfig",
    "applications.main_page.apps.MainPageConfig",
    "applications.hello.apps.HelloConfig",
    "applications.stats.apps.StatsConfig",
    "applications.education.apps.EducationConfig",
    "applications.test_projects.apps.TestProjectsConfig",
    "applications.blog.apps.BlogConfig",
    "applications.onboarding.apps.OnboardingConfig",
    "applications.api.apps.ApiConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [PROJECT_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "utils.theme_utils.theme_ctx_processor",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
development_database_url = _ds.DATABASE_URL
database_url = os.getenv("DATABASE_URL", development_database_url)
database_params = dj_database_url.parse(database_url)

DATABASES = {
    "default": database_params,
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


LOGIN_URL = reverse_lazy("onboarding:sign-in")

LOGIN_REDIRECT_URL = reverse_lazy("main_page:main")

STATIC_URL = "/s/"
STATICFILES_DIRS = [
    PROJECT_DIR / "static",
]
STATIC_ROOT = REPO_DIR / ".static"
if not DEBUG:
    STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

AWS_ACCESS_KEY_ID = _ds.AWS_ACCESS_KEY_ID
AWS_S3_OBJECT_PARAMETERS = {"ACL": "public-read"}
AWS_QUERYSTRING_AUTH = False
AWS_S3_AVATARS_LOCATION = _ds.AWS_S3_AVATARS_LOCATION
AWS_S3_ADDRESSING_STYLE = "path"
AWS_S3_REGION_NAME = _ds.AWS_S3_REGION_NAME
AWS_SECRET_ACCESS_KEY = _ds.AWS_SECRET_ACCESS_KEY
AWS_STORAGE_BUCKET_NAME = _ds.AWS_STORAGE_BUCKET_NAME

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication"
    ]
}
