#!/bin/env python

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.gen
import tornado.httpclient
import tornado.concurrent
import tornado.ioloop

import time,datetime

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

class SleepHandler(tornado.web.RequestHandler):

    def get(self):
        #yield tornado.gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + 10)
		while 1:
				pass
		self.write("when i sleep 5s"+ str(datetime.datetime.now()))


class JustNowHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("i hope just now see you"+ str(datetime.datetime.now()))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[
            (r"/sleep", SleepHandler), (r"/now", JustNowHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
