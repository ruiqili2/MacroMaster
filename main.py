#import os
#import tornado.httpserver
#import tornado.ioloop
#import tornado.wsgi
#from django.core.wsgi import get_wsgi_application
#
#def main():
#    os.environ['DJANGO_SETTINGS_MODULE'] = 'MacroMaster.settings' # path to your settings module
#    application = get_wsgi_application()
#    container = tornado.wsgi.WSGIContainer(application)
#    http_server = tornado.httpserver.HTTPServer(container)
#    http_server.listen(8888)
#    tornado.ioloop.IOLoop.instance().start()
#
#if __name__ == "__main__":
#    main()

from tornado.options import options, define, parse_command_line
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os

define('port', type=int, default=8080)

class HelloHandler(tornado.web.RequestHandler):
	def get(self):
		self.write('Hello from tornado')

def main():
	os.environ['DJANGO_SETTINGS_MODULE'] = 'MacroMaster.settings' # path to your settings module
	settings = {
		"static_path": os.path.join(os.path.dirname(__file__), "static"),
	}
	parse_command_line()
	wsgi_app = tornado.wsgi.WSGIContainer(
	get_wsgi_application())
	tornado_app = tornado.web.Application(
	[
		('/hello-tornado', HelloHandler),
		('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
		(r'/static/(.*)', tornado.web.StaticFileHandler, {'path': "/home/me/Downloads/javaAutoGraderBuilding/django-tornado-demo-master/testsite/static"}),
	])
	server = tornado.httpserver.HTTPServer(tornado_app)
	server.listen(options.port)
	tornado.ioloop.IOLoop.instance().start()
if __name__ == '__main__':
	main()
