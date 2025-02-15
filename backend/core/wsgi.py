import os
from django.core.wsgi import get_wsgi_application

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

# Create the WSGI application object
application = get_wsgi_application()
app = application