import asyncmongo
import tornado.ioloop
from tornado import gen
import time

def s():
	db.test.find()

@gen.engine
def test_query(i):
    '''A generator function of asyncmongo query operation.'''
    #response, error = yield gen.Task(db.test.find, {})
    yield gen.Task(tornado.ioloop.IOLoop.instance().add_timeout, time.time() + i)
    print i


    #tornado.ioloop.IOLoop.instance().stop()

if __name__ == "__main__":
    db = asyncmongo.Client(pool_id="test", host="127.0.0.1", port=27017,
                           dbname="test")
    test_query(5)
    test_query(1)
    tornado.ioloop.IOLoop.instance().start()
