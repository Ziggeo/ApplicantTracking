from mongo import db

# For update_twitter
import tweepy
import settings
import urllib2

"""
{
  'user': { 
    'id_str':'', 
    'auth_type': '', 
    'username': '', 
    'fullname': '', 
    'screen_name': '', 
    'profile_image_url_https': '', 
    'profile_image_url': '', 
    'is_blacklisted': False 
    },
  'access_token': { 'secret': '', 'user_id': '', 'screen_name': '', 'key': '' },
  'email_address': '',
  'role': '',
"""

''' Returns all users '''
def get_all():
  return db.user_info.find()

def get_user_by_id_str(id_str):
  return db.user_info.find_one({'user.id_str': id_str})

def get_user_by_screen_name(screen_name):
  return db.user_info.find_one({'user.screen_name': screen_name})

def get_user_by_email(email_address):
  return db.user_info.find_one({'email_address':email_address})
  
def create_new_user(user, access_token):
  return db.user_info.update({'user.id_str': user['id_str']}, {'user':user, 'access_token':access_token, 'email_address':'', 'role':''}, upsert=True)

def save_user(user):
  return db.user_info.update({'user.id_str': user['user']['id_str']}, user)

def get_user_count():
  return db.user_info.count()

###########################
### SCRIPT FUNCTIONS
###########################
''' Updates twitter account of id id_str, or else updates all twitter accounts.
    Updating all accounts will probably cause API to puke from too many requests '''
def update_twitter(id_str=None, api=None):
  if not api:
    consumer_key = settings.get('twitter_consumer_key')
    consumer_secret = settings.get('twitter_consumer_secret')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
    api = tweepy.API(auth) 

  if id_str:
    users = [get_user_by_id_str(id_str)]
  else:
    users = get_all()

  for user in users:
    id_str = user['user']['id_str']
    twitter_user = api.get_user(id=id_str)
    if id_str != twitter_user.id_str:
      raise Exception

    user_data = {
      'auth_type': 'twitter',
      'id_str': twitter_user.id_str,
      'username': twitter_user.screen_name,
      'fullname': twitter_user.name,
      'screen_name': twitter_user.screen_name,
      'profile_image_url': twitter_user.profile_image_url,
      'profile_image_url_https': twitter_user.profile_image_url_https,
    }

    updated_user = {'access_token': user['access_token'], 'user': user_data}
    save_user(updated_user)
    print "++ Updated user @%s" % user['user']['username']

''' Only updates a user if their twitter profile image URL returns a 404 '''
def update_twitter_profile_images():
  consumer_key = settings.get('twitter_consumer_key')
  consumer_secret = settings.get('twitter_consumer_secret')
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret, secure=True)
  api = tweepy.API(auth) 

  for user in get_all():
    print "Checking user %s" % user['user']['screen_name']
    try:
      response= urllib2.urlopen(user['user']['profile_image_url_https'])
    except urllib2.HTTPError, e:
      if e.code == 404:
        update_twitter(id_str=user['user']['id_str'], api=api)

