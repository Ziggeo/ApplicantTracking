import os
import time
import tornado.options

os.environ['COOKIE_SECRET'] = "placeholder" # OVERWRITE
os.environ['DB_NAME'] = "apptrack" # OVERWRITE
os.environ['MONGODB_URL'] = "mongodb://localhost:27017/apptrack" # OVERWRITE
os.environ['ZIGGEO_TOKEN'] = "placeholder" # OVERWRITE
os.environ["ADMINS"] = "adminname:adminpassword"

os.environ['ACTIVE_THEME'] = "usv"
os.environ['BASE_URL'] = "localhost"
os.environ['PATH'] = "/app/bin:/app/vendor/nginx/sbin:/app/vendor/php/bin:/app/vendor/php/sbin:/usr/local/bin:/usr/bin:/bin"
os.environ['SITE_TITLE'] = "Applicant Tracking"  
os.environ['TZ'] = "US/Eastern"
os.environ['PROJECT_ROOT'] = os.path.abspath(os.path.join(os.path.dirname(__file__)))

try:
  import settings_local_environ
except:
  pass

  
time.tzset()

def get(key):
  return os.environ.get(key.upper())
