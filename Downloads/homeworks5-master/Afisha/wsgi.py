import os
import dotenv

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Afisha.settings')
dotenv.read_dotenv(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')) # указывает путь до файла

application = get_wsgi_application()
