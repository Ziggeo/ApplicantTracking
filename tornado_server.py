import os
import tornado.httpserver
import tornado.httpclient
import tornado.ioloop
import tornado.options
import tornado.web

import logging

import settings 

import templates
import lib.apply

class Application(tornado.web.Application):
  def __init__(self):

    app_settings = {
      "cookie_secret" : settings.get("COOKIE_SECRET"),
      "debug": False,
      "static_path" : os.path.join(os.path.dirname(__file__), "static"),
      "template_path" : os.path.join(os.path.dirname(__file__), "templates"),
    }

    handlers = [

      # apply stuff
      (r"/", lib.apply.Process),
      (r"", lib.apply.Process),
      (r"/apply", lib.apply.Process),
      (r"/apply/", lib.apply.Process),
      (r"/apply/admin", lib.apply.AdminList),
      (r"/apply/admin/api/tags/([^\/]+)", lib.apply.AdminApiTags),
      (r"/apply/admin/api/rate/([^\/]+)", lib.apply.AdminApiRate),
      (r"/apply/admin/api/comment/([^\/]+)", lib.apply.AdminApiComment),

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
