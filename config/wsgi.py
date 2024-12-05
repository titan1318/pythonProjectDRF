"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
<<<<<<< HEAD
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

load_dotenv()
=======
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
>>>>>>> 9ff2f24294ef21ce0325f374f0cc082d46302804

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
