"""
WSGI config for Config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from dotenv import load_dotenv

from django.core.wsgi import get_wsgi_application

# Carrega variáveis de ambiente antes de iniciar a aplicação
load_dotenv()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Config.settings')

application = get_wsgi_application()
