import os

SECRET_KEY = 'django-insecure-)&)%sskcxrvh7hpcmx5)=&ncjzo1cp_-ind$348-xs(oemrpmq'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'get_a_pic_db',
        'USER': 'postgres',
        'PASSWORD': 'coderslab',
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5433'),
    }
}
