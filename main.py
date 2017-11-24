#! /usr/bin/env python
from tornado.options import options, define, parse_command_line
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
import sys


define("port", type=int, default=sys.argv[1])

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("Hello from tornado")

# Prevent tornado caching static files. Comment out on deploy.
class MyStaticFileHandler(tornado.web.StaticFileHandler):
    def set_extra_headers(self, path):
        # Disable cache
        self.set_header('Cache-Control', 'no-store, no-cache, must-revalidate, max-age=0')

def main():
	os.environ["DJANGO_SETTINGS_MODULE"] = "MacroMaster.settings" # path to your settings module
	settings = {
		"static_path": os.path.join(os.path.dirname(__file__), "static"),
	}
	parse_command_line()
	wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
	tornado_app = tornado.web.Application(
	[
		
		("/hello-tornado", HelloHandler),
		#("/favicon.ico", tornado.web.StaticFileHandler, {"path": "/home/ruiqili2/cs411-project/static/favicon.ico"}),
		(r"/static/(.*)", tornado.web.StaticFileHandler, {"path": os.path.join(os.environ['HOME'],"cs411-project/static")}),
		#(r"/", tornado.web.StaticFileHandler, {"path": "/home/ruiqili2/cs411-project/static/"}),

		(r"/(.*)", tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
		
	])
	server = tornado.httpserver.HTTPServer(tornado_app)
	server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
if __name__ == "__main__":
	main()
