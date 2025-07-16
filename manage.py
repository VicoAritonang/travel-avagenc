#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_avagenc.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)

# Vercel handler
def handler(request, context):
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_avagenc.settings')
    application = get_wsgi_application()
    application = WhiteNoise(application, root=os.path.join(os.path.dirname(__file__), 'static'))
    return application(request, context)

if __name__ == '__main__':
    main()
