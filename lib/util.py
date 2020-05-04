import tornado.web
import binascii
import os
import base64

class SessionHandler(tornado.web.RequestHandler):
  def get_current_user(self):
    session = self.get_secure_cookie("session")
    if session :
        return session
    session = binascii.hexlify(os.urandom(32))
    self.set_secure_cookie("session", session)
    return session


def require_basic_auth(handler_class):
    def wrap_execute(handler_execute):
        def require_basic_auth(handler, kwargs):
            if (not handler.get_current_user()):
                handler.set_status(401)
                handler.set_header('WWW-Authenticate', 'Basic realm=Restricted')
                handler._transforms = []
                handler.finish()
                return False
            return True
        def _execute(self, transforms, *args, **kwargs):
            if not require_basic_auth(self, kwargs):
                return False
            return handler_execute(self, transforms, *args)
        return _execute
    
    def get_current_user(self):
        scheme, _, token = self.request.headers.get('Authorization', '').partition(' ')
        if scheme.lower() == 'basic':
            user, _, pwd = base64.decodestring(token).partition(':')
            if self.basic_auth(user, pwd) :
                return user
        return None
 
    handler_class._execute = wrap_execute(handler_class._execute)
    handler_class.get_current_user = get_current_user
    return handler_class
