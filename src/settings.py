import os

DEBUG = os.getenv('DEBUG', False)
API_KEY = os.getenv('API_KEY')
if not API_KEY:
    raise EnvironmentError('There is no API_KEY set in the environment but is needed for getting the source feed')
SOURCE_LOCATION = os.getenv('JSON_LOCATION', 'https://api.deutsche-digitale-bibliothek.de/search?query=*')
# SOURCE_LOCATION = os.getenv('JSON_LOCATION', '../data/ddb.json')
TARGET_URL = os.getenv('TARGET_URL', 'http://localhost:4040/resources')
BASIC_AUTH_USER = os.getenv('BASIC_AUTH_USER', 'schulcloud-content-1')
BASIC_AUTH_PASSWORD = os.getenv('BASIC_AUTH_PASSWORD', 'content-1')

