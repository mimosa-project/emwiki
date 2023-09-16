import configparser
from distutils.util import strtobool
import os

from git import Repo

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-85qwk5p1@5d=b*+p3y6q3h+k+1*%dfr%m%(0wv=54(nn%')

# SECURITY WARNING: don't run with debug turned on in production!
if bool(int(os.environ.get('DEBUG', "1"))):
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = str(os.environ.get('DJANGO_ALLOWED_HOSTS', "localhost 127.0.0.1")).split(' ')

INSTALLED_APPS = [
    'article.apps.ArticleConfig',
    'symbol.apps.SymbolConfig',
    'home.apps.HomeConfig',
    'search.apps.SearchConfig',
    'accounts.apps.AccountsConfig',
    'graph.apps.GraphConfig',
    'explanation.apps.ExplanationConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'emwiki.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'mmlfiles', 'article', 'templates'),
            os.path.join(BASE_DIR, 'mmlfiles', 'symbol', 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'emwiki.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.environ.get("SQL_ENGINE", 'django.db.backends.postgresql'),
        "NAME": os.environ.get("SQL_DATABASE", 'postgres'),
        "USER": os.environ.get("SQL_USER", "postgres"),
        "PASSWORD": os.environ.get("SQL_PASSWORD", "postgres"),
        "HOST": os.environ.get("SQL_HOST", "localhost"),
        "PORT": os.environ.get("SQL_PORT", "5432"),
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Security settings
if not DEBUG:
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "SAMEORIGIN"

# Static files (CSS, JavaScript, Images)
STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'mmlfiles', 'graph', 'static'),
]
if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
MEDIA_URL = os.environ.get('MEDIA_URL', '/media/')
MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

# Account
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = os.environ.get('LOGIN_REDIRECT_URL', '/')
AUTH_USER_MODEL = 'accounts.User'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if DEBUG is True:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = os.environ.get("EMAIL_HOST")
    EMAIL_PORT = int(os.environ.get("EMAIL_PORT"))
    EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
    EMAIL_USE_TLS = strtobool(os.environ.get("EMAIL_USE_TLS"))

# Additional settings(Django framework doesn't refer these settings)

# Directory configurations
# mmlfiles
MMLFIELS_DIR = os.path.join(BASE_DIR, 'mmlfiles')
MML_ABSTR_DIR = os.path.join(MMLFIELS_DIR, 'abstr')
MML_FMBIBS_DIR = os.path.join(MMLFIELS_DIR, 'fmbibs')
MML_HTML_DIR = os.path.join(MMLFIELS_DIR, 'html')
MML_MML_DIR = os.path.join(MMLFIELS_DIR, 'mml')
MML_INI_PATH = os.path.join(MMLFIELS_DIR, 'mml.ini')
MML_LAR_PATH = os.path.join(MMLFIELS_DIR, 'mml.lar')
MML_VCT_PATH = os.path.join(MMLFIELS_DIR, 'mml.vct')
MML_ARTICLE_DIR = os.path.join(MMLFIELS_DIR, 'article')
MML_SYMBOL_DIR = os.path.join(MMLFIELS_DIR, 'symbol')
MML_SEARCH_DIR = os.path.join(MMLFIELS_DIR, 'search')
MML_GRAPH_DIR = os.path.join(MMLFIELS_DIR, 'graph')
# Article
PRODUCT_HTMLIZEDMML_DIR = os.path.join(
    MML_ARTICLE_DIR, 'templates', 'article', 'htmlized_mml')
# Symbol
PRODUCT_SYMBOLHTML_DIR = os.path.join(
    MML_SYMBOL_DIR, 'templates', 'symbol', 'symbol_html')
# Search
SEARCH_INDEX_DIR = os.path.join(MML_SEARCH_DIR, 'index')
# Graph
GRAPH_ELS_DIR = os.path.join(MML_GRAPH_DIR, 'static', 'graph')
# Tests
TEST_DATA_DIR = os.path.join(BASE_DIR, 'testdata')
TEST_OUTPUTS_DIR = os.path.join(TEST_DATA_DIR, 'outputs')
TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR = os.path.join(
    TEST_OUTPUTS_DIR, 'product_htmlized_mml')
TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR = os.path.join(
    TEST_OUTPUTS_DIR, 'product_symbol_html')
TEST_RAW_MML_MML_DIR = os.path.join(TEST_DATA_DIR, 'mml')
TEST_MML_MML_DIR = os.path.join(TEST_DATA_DIR, 'mml_commented')
TEST_EXPLANATION_DIR = os.path.join(TEST_DATA_DIR, 'explanation_edited')

TEST_MML_HTML_DIR = os.path.join(TEST_DATA_DIR, 'raw_htmlized_mml')
TEST_PRODUCT_HTMLIZEDMML_DIR = os.path.join(
    TEST_DATA_DIR, 'product_htmlized_mml')
TEST_PRODUCT_SYMBOLHTML_DIR = os.path.join(
    TEST_DATA_DIR, 'product_symbol_html')
TEST_DOWNLOAD_MML_DIR = os.path.join(TEST_OUTPUTS_DIR, 'mml_downloaded')
TEST_DOWNLOAD_HTML_DIR = os.path.join(TEST_OUTPUTS_DIR, 'html_downloaded')
TEST_SEARCH_INDEX_DIR = os.path.join(TEST_DATA_DIR, 'search_index')

# emwiki-contents
mml_config = configparser.ConfigParser()
mml_config.read(MML_INI_PATH)
MIZAR_VERSION = mml_config["MML"]["MMLVersion"]
EMWIKI_CONTENTS_REPO = Repo(os.path.join(BASE_DIR, 'emwiki-contents'))
EMWIKI_CONTENTS_REPO.git.checkout("mml_commented")
EMWIKI_CONTENTS_MML_DIR = os.path.join(BASE_DIR, 'emwiki-contents', 'mml')

EMWIKI_CONTENTS_EXPLANATION_REPO = Repo(os.path.join(BASE_DIR, 'emwiki-contents'))
EMWIKI_CONTENTS_EXPLANATION_REPO.git.checkout('explanation_edited')
EMWIKI_CONTENTS_EXPLANATON_DIR = os.path.join(BASE_DIR, 'emwiki-contents', 'explanation')