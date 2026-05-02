import os
import sys
import django
from django.urls import reverse

sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanga_portal.settings')
django.setup()

try:
    url = reverse('admissions:verify_otp', kwargs={'email': 'muazuawe5050@gmail.com'})
    print(f"URL found: {url}")
except Exception as e:
    print(f"Error: {e}")
