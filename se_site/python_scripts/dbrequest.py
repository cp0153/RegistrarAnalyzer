import os
import sys
import json

# Import settings for django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "se_site.settings.dev")
import django
from django.core import serializers
from django.db.utils import IntegrityError

django.setup()
from registrar_analyzer.models import Courses

# Get first two DB entries
serialData = serializers.serialize("json", Courses.objects.all()[:2])
jsonArr = json.loads(serialData)
for item in jsonArr:
    print(">>> FIELDS")
    print(item['fields'])







#