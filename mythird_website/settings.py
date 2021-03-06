"""
Django settings for mythird_website project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')ed=uz^l4=cy+7ymax2ho!l7o-^n=bkft*0c=7f9^!l$_s_48f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = 'users.UserProfile'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'DjangoUeditor',
    'users.apps.UsersConfig',
    'goods.apps.GoodsConfig',
    'trade.apps.TradeConfig',
    'user_operation.apps.UserOperationConfig',
    'crispy_forms',
    'xadmin',
    'rest_framework',
    'django_filters',
    'corsheaders',  # 跨域
    'rest_framework.authtoken',  # token
    'social_django',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域问题 notes:此拦截器 似乎可以代理csrf。所以前端不需要传csrf。具体百度
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True  # 跨域问题

ROOT_URLCONF = 'mythird_website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # 以下两个感觉暂时没必要加，并未采用template
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

WSGI_APPLICATION = 'mythird_website.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
import pymysql
pymysql.install_as_MySQLdb()
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'third',
        'USER': 'test',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        # 设置数据库引擎，用于第三方软件对数据库的操作，此处无需
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;'}
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 数据库存储使用时间，True时间会被存为UTC的时间
USE_TZ = False

AUTHENTICATION_BACKENDS = (
    'social_core.backends.weibo.WeiboOAuth2',
    'social_core.backends.qq.QQOAuth2',
    'social_core.backends.weixin.WeixinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    # 以上为第三方登录到的配置。具体需要查看源码
    'users.views.CustomBackend',
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',  # jwt token 最好放到view里面，防止某些token出错时公共页面无法访问
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
    # 限速策略配置，也可以在类内配置
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',  # 未登录请求，通过ip判断
        'rest_framework.throttling.UserRateThrottle'  # 登录用户请求
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}

import datetime
JWT_AUTH = {
    # 配置详情参见官方文档：https://github.com/GetBlimp/django-rest-framework-jwt/blob/master/docs/index.md
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',  # token的名字 此处需要和前端联调，所以为token 否则无法正确登录
}

# 手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

# 云片apikey
YUNPIAN_API_KEY = "042cdd2e94d8649d2e61d2350da61cc1"

# 支付宝相关配置
private_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/app_private_key.pem')
ali_pub_key_path = os.path.join(BASE_DIR, 'apps/trade/keys/alipay_public_key.pem')

# rest_framework_extensions相关配置
REST_FRAMEWORK_EXTENSIONS = {
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60,  # 过期时间
}

# 配置redis缓存
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 设置第三方登录参数
SOCIAL_AUTH_WEIBO_KEY = '2473478422'
SOCIAL_AUTH_WEIBO_SECRET = 'b1380a5ad6afcdfda02a35adc880ca20'

SOCIAL_AUTH_QQ_KEY = ''
SOCIAL_AUTH_QQ_SECRET = ''

SOCIAL_AUTH_WEIXIN_KEY = ''
SOCIAL_AUTH_WEIXIN_SECRET = ''

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/index'  # 登录成功后跳转页面
