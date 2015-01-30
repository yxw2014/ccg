import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import tornado.iostream
import socket

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", PubSubWebSocket),
        ]
        settings = dict()
        tornado.web.Application.__init__(self, handlers, **settings)

class PubSubWebSocket(tornado.websocket.WebSocketHandler):
    def open(self):
        print "WebSocket opened"

    def on_message(self, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        print message.strip()
        self.data = ""        
        self.stream = tornado.iostream.IOStream(s)
        self.stream.connect(("50.23.111.162", 6379))
        self.stream.write("SUBSCRIBE %s\r\n" % str(message).strip())
        self.stream.read_until("\r\n", self.process_redis_protocol)

    def process_redis_protocol(self, data):
        print repr(data)
        if data.startswith('*'):
            self.command = 0
            self.command_count = int(data[1:-2])
        elif data.startswith('$'):
            self.command += 1            
            self.stream.read_bytes(int(data[1:-2]) + 2, self.process_redis_protocol)
            return
        elif data.startswith(':'):
            print 'Subscribed'
        else:
            if self.command == self.command_count:
                self.write_message(repr(data))

        self.stream.read_until("\r\n", self.process_redis_protocol)
        return

    def on_close(self):
        print "WebSocket closed"

def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
