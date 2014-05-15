import tornado.web
import app.basic
import settings
from lib import userdb

###########################
### EMAIL SETTINGS
### /auth/email/?
###########################
class EmailSettings(app.basic.BaseHandler):
  @tornado.web.authenticated
  def get(self):
    next_page = self.get_argument('next', '')
    subscribe_to = self.get_argument('subscribe_to', '')
    error = ''
    email = ''
    status = 'enter_email'

    # get the current user's email value
    user = userdb.get_user_by_screen_name(self.current_user)
    if user:
      email = user['email_address']

    self.render('user/email_subscribe.html', email=email, error=error, next_page=next_page, subscribe_to=subscribe_to, status=status)

  @tornado.web.authenticated
  def post(self):
    next_page = self.get_argument('next', '')
    next_page += "&finished=true"
    close_popup = self.get_argument('close_popup', '')
    email = self.get_argument('email', '')
    subscribe_to = self.get_argument('subscribe_to', '')
    error = ''
    status = ''
    slug = ''
    if close_popup != '':
      status = 'close_popup'

    # get the current user's email value
    user = userdb.get_user_by_screen_name(self.current_user)
    if user:
      # Clear the existing email address
      if email == '':
        if subscribe_to == '':
          user['email_address'] = ''
          self.set_secure_cookie('email_address', '')
          userdb.save_user(user)
          error = 'Your email address has been cleared.'
      else:
        # make sure someone else isn't already using this email
        existing = userdb.get_user_by_email(email)
        if existing and existing['user']['id_str'] != user['user']['id_str']:
          error = 'This email address is already in use.'
        else:
          # OK to save as user's email
          user['email_address'] = email
          userdb.save_user(user)
          self.set_secure_cookie('email_address', email)

    userdb.save_user(user)
    
    self.redirect("/user/%s/settings?msg=updated" % user['user']['screen_name'])

###########################
### LOG USER OUT OF ACCOUNT
### /auth/logout
###########################
class LogOut(app.basic.BaseHandler):
  def get(self):
    self.clear_all_cookies()
    self.redirect(self.get_argument('next', '/'))

##########################
### USER PROFILE
### /user/(.+)
##########################
class Profile(app.basic.BaseHandler):
  def get(self, screen_name, section="shares"):
    user = userdb.get_user_by_screen_name(screen_name)
    if not user:
      raise tornado.web.HTTPError(404)
    
    view = "profile"
    self.render('user/profile.html', user=user, screen_name=screen_name, section=section, msg=None, view=view)

###########################
### USER SETTINGS
### /user/settings/?
###########################
class UserSettings(app.basic.BaseHandler):
  
  @tornado.web.authenticated
  def get(self, username=None):
    if username is None and self.current_user:
      username = self.current_user
    if username != self.current_user:
      raise tornado.web.HTTPError(401)
    
    if self.request.path.find("/user/settings") >= 0:
      self.redirect('/user/%s/settings' % username)
      
    msg = self.get_argument("msg", None)
    user = userdb.get_user_by_screen_name(self.current_user)
    if self.current_user in settings.get('staff'):
      user = userdb.get_user_by_screen_name(username)
      
    if not user:
      raise tornado.web.HTTPError(404)
    
    #self.render('user/settings.html', user=user, msg=msg)
    self.render('user/profile.html', user=user, screen_name=self.current_user, section="settings", msg=msg)
