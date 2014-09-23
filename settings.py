import os
import time
import tornado.options

os.environ['COOKIE_SECRET'] = "placeholder" # OVERWRITE
os.environ['DB_NAME'] = "apptrack" # OVERWRITE
os.environ['MONGODB_URL'] = "mongodb://localhost:27017/apptrack" # OVERWRITE
os.environ['ZIGGEO_TOKEN'] = "placeholder" # OVERWRITE
os.environ["ADMINS"] = "adminname:adminpassword"
os.environ['FILE_PICKER_KEY'] = "placeholder" # OVERWRITE

os.environ['BASE_URL'] = "localhost"
os.environ['PATH'] = "/app/bin:/app/vendor/nginx/sbin:/app/vendor/php/bin:/app/vendor/php/sbin:/usr/local/bin:/usr/bin:/bin"
os.environ['TZ'] = "US/Eastern"
os.environ['PROJECT_ROOT'] = os.path.abspath(os.path.join(os.path.dirname(__file__)))

os.environ['SITE_TITLE'] = "Applicant Tracking"
os.environ['APPLY_TITLE'] = "Apply"   
os.environ['STRING_BOTTOM'] = "We support workplace diversity and does not discriminate in employment matters on the basis of race, color, religion, gender, national origin, age, military service eligibility, veteran status, sexual orientation, marital status, disability, or any other protected class."
os.environ['STRING_CONFIRMATION'] = "We will begin reviewing applications shortly, and we will be in touch regarding next steps."
os.environ["STRING_WELCOME"] = "Thanks for taking the time to apply for our position."
os.environ["STRING_INTRO"] = "In the first section (below), we're looking to see links that will help us get to know you. This could be your personal blog, Tumblr, Github profile or Twitter account - whatever represents you best. We expect your web presence to represent who you are, not who you think an employer wishes you were, so please don't waste time sanitizing your web presence before sending us there. We get it."

global_data = {
    "VIDEOS": [{
        "question": "Why are you interested in the position?",
        "limit": 90
    }, {
        "question": "What inspires you the most, and why?",
        "limit": 120
    }],
    "FIELDS": [{
        "label": "Your Name",
        "name": "name",
        "type": "text",
        "placeholder": "",
        "required": True
    }, {
        "label": "Email",
        "name": "email",
        "type": "text",
        "placeholder": "",
        "required": True
    }, {
        "label": "Location",
        "name": "location",
        "type": "text",
        "placeholder": "Where are you now?",
        "required": True
    }, {
        "label": "You, on the Web",
        "name": "web",
        "type": "textarea",
        "placeholder": "Any public social links that help us get to know you. (Please put each link on a new line.)",
        "required": True
    }, {
        "label": "Projects",
        "name": "projects",
        "type": "textarea",
        "placeholder": "Any links to projects you've built or worked on. (Please put each link on a new line.)",
        "required": False
    }, {
        "label": "CV",
        "name": "cv",
        "type": "file",
        "placeholder": "Your CV (PDF, DOC, TXT)",
        "required": False
    }]
}


try:
  import settings_local_environ
  if settings_local_environ.global_data :
      global_data = settings_local_environ.global_data
except:
  pass

  
time.tzset()

def get(key):
  return os.environ.get(key.upper())
