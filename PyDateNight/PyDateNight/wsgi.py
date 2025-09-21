"""
WSGI config for PyDateNight project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

path = r'/home/thebaze/PythonWeb/PyDateNight'
if path not in sys.path:
        sys.path.insert(0, path)

# Set environment variables for production
os.environ.setdefault('YELP_API_KEY', 'CPRMZCArl_l0ArDq0IQnPieOsO1IFbxnCIn_OkNf2nJb4nneIYjw4MJyNBwFpapXFTtEkh4LbqNzMWF3eZYwJDfoWHeZDDfCDVV0CCqT-SVgz0URom3R-r7XSILQaHYx')
os.environ.setdefault('DEBUG', 'False')
os.environ.setdefault('SECRET_KEY', 'j7f+(ejwzy(33zxwoxq_ruy6u@^5f=)(1=8(=usm8mwro$!8+^')

os.environ['DJANGO_SETTINGS_MODULE'] = 'PyDateNight.settings'

application = get_wsgi_application()
