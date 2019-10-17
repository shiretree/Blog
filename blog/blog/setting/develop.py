from .base import *   #NOQA
                        #NOQA这个注释的作用是，告诉PEP8规范检测工具，这个地方不需要检测。或者在文件的第一行添加# flake8: NOQA


DEBUG = True

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3')
    }
}