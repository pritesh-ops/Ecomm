from pathlib import Path
import os
import mimetypes
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================
# SECURITY CONFIGURATION
# ======================
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-8j#t+633ubijv4=^e51aj#po^f!rmfiz5&$8(0d5$%c4(i#hv(')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Hosts/URLs Configuration
ALLOWED_HOSTS = ['localhost']
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# Security Headers
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# =================
# APPLICATION CONFIG
# =================
INSTALLED_APPS = [
    # Django Core Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    
    # Third Party Apps
    "whitenoise.runserver_nostatic",
    
    # Local Apps
    "shops.apps.ShopsConfig",
    "products.apps.ProductsConfig",
    "orders.apps.OrdersConfig",
    "users.apps.UsersConfig",
    "home.apps.HomeConfig",
    "seller_dashboard.apps.SellerDashboardConfig",
]

# Debug Toolbar (Development Only)
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    INTERNAL_IPS = ["127.0.0.1"]
    mimetypes.add_type("application/javascript", ".js", True)

MIDDLEWARE = [
    # Security Middleware
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    
    # Django Core Middleware
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Debug Toolbar Middleware
if DEBUG:
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG
    }

ROOT_URLCONF = "ecomm.urls"
WSGI_APPLICATION = "ecomm.wsgi.application"

# =============
# DATABASE CONFIG
# =============
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        conn_max_age=600
    )
}

# ===================
# AUTHENTICATION CONFIG
# ===================
AUTH_USER_MODEL = "users.User"
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# =============
# INTERNATIONALIZATION
# =============
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# =============
# STATIC FILES
# =============
STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media Files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# =============
# TEMPLATES
# =============
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "users.context_processors.cart_count",
            ],
            'libraries': {
                'multipy': 'orders.templatetags.multiply',
            }
        },
    },
]

# =============
# OTHER SETTINGS
# =============
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Stripe Configuration
STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY', 'pk_test_**********')
STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY', 'sk_test_***********')