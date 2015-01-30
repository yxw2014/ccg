import test12

from tornado.options import options, define
define('port', type=int, default=9528, help="define the server port")
define('debug', type=bool, default=False, help="debug mode, True or False")

test12.aaa()

print 11