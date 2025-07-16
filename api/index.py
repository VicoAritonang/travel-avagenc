import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'travel_avagenc.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

# Create WSGI application
application = get_wsgi_application()
application = WhiteNoise(application, root=os.path.join(project_root, 'static'))

# Vercel handler
def handler(request, context):
    return application(request, context) 