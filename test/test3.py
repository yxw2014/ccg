import tornado.ioloop
import tornado.web
from TorCast import client

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

application = tornado.web.Application([
    (r"/", MainHandler),
])

def on_message(chn, message):
    print message
    #when message recived, this function will be fired

if __name__ == "__main__":
    application.listen(8888)
    #sub = client("127.0.0.1",6379,1)
    sub= client.Subscriber("127.0.0.1", 6379, 5)
    sub.listen_on(["chn_1"], on_message)
    tornado.ioloop.IOLoop.instance().start()

