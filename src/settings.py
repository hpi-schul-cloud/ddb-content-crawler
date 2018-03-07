import os

API_KEY = os.getenv('API_KEY', None)
SOURCE_LOCATION = os.getenv('JSON_LOCATION', 'https://api.deutsche-digitale-bibliothek.de/search?query=*')
# SOURCE_LOCATION = os.getenv('JSON_LOCATION', '../data/ddb.json')
TARGET_URL = os.getenv('TARGET_URL', 'http://localhost:4040/resources')
BASIC_AUTH_USER = os.getenv('BASIC_AUTH_USER', 'schulcloud-content-1')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'content-1')
