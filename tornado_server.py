import os
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web

import logging

import settings 

import app.user
import app.twitter
import app.error
import templates
import app.apply

class Application(tornado.web.Application):
  def __init__(self):

    app_settings = {
      "cookie_secret" : "change_me",
      "login_url": "/auth/twitter",
      "debug": False,
      "static_path" : os.path.join(os.path.dirname(__file__), "static"),
      "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    }

    handlers = [

      # account stuff
      (r"/auth/email/?", app.user.EmailSettings),
      (r"/auth/logout/?", app.user.LogOut),
      (r"/user/(?P<username>[A-z-+0-9]+)/settings/?", app.user.UserSettings),
      (r"/user/settings?", app.user.UserSettings),
      (r"/user/(?P<screen_name>[A-z-+0-9]+)", app.user.Profile),
      (r"/user/(?P<screen_name>[A-z-+0-9]+)/(?P<section>[A-z]+)", app.user.Profile),

      # apply stuff
      (r"/", app.apply.Process),
      (r"", app.apply.Process),
      (r"/apply", app.apply.Process),
      (r"/apply/", app.apply.Process),
      (r"/apply/admin", app.apply.AdminList),
      (r"/apply/admin/view/([^\/]+)", app.apply.AdminView),
      (r"/apply/admin/api/rate/([^\/]+)", app.apply.AdminApiRate),

      # twitter stuff
      (r"/auth/twitter/?", app.twitter.Auth),
      (r"/twitter", app.twitter.Twitter),

     ]
     
    tornado.web.Application.__init__(self, handlers, **app_settings)


def main():
  tornado.options.define("port", default=8001, help="Listen on port", type=int)
  tornado.options.parse_command_line()
  logging.info("starting tornado_server on 0.0.0.0:%d" % tornado.options.options.port)
  http_server = tornado.httpserver.HTTPServer(request_callback=Application(), xheaders=True)
  http_server.listen(tornado.options.options.port)
  tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
  main()
