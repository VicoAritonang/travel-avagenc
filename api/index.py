import sys
import os

# Pastikan path project Django dikenali
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "travel_avagenc.settings")

from django.core.wsgi import get_wsgi_application

# Vercel expects 'app' or 'handler'
app = get_wsgi_application() 