# -*- coding: utf-8 -*-

import os
import sys
import logging
import time,datetime

#reload(sys) 
#sys.setdefaultencoding('utf-8') 
#/usr/lib/python2.7/sitecustomize.py

sys.path.append('./')
sys.path.append('./lib')
sys.path.append('./config')
sys.path.append('./model')

from model import *
import log
from config import config
from errors import err
from lib.mongo import Mongo
import redis

from amf import base as amfbase
from ccg import base as webbase

from tornado.options import options, define

define('port', type=int, default=8800, help="define the server port")
define('debug', type=bool, default=False, help="debug mode, True or False")


if __name__ == "__main__":
    options.parse_command_line()

    #for mutiprocess
    logger=logging.getLogger()
    handler=logging.FileHandler(log.log_path+ "."+ str(options.port))
    #very important
    logger.removeHandler(logger.handlers[0])
    logger.addHandler(handler)
    logger.setLevel(log.level)
    logger.error = logger.error
    logger.warn = logger.warning
    logger.info = logger.info
    logger.debug = logger.debug    
    
    model= BaseModel.BaseModel
    model.log= logger
    
    mongo= Mongo.getInstance(config['MONGO_STAG']['host'], int(config['MONGO_STAG']['port']))
    mongodb= mongo[config['MONGO_STAG']['db']]
    model.mongodb= mongodb    
    
    pool = redis.ConnectionPool(host=config['REDIS_STAG']['host'], port= int(config['REDIS_STAG']['port']), \
                                                    db= int(config['REDIS_STAG']['db']), socket_timeout= 2)  
    redis = redis.Redis(connection_pool=pool)
    model.redis= redis

    amfbase.Base.logger= logger
    amfbase.Base.redis= redis
    amfbase.Base.mongodb= mongodb

    webbase.Base.logger= logger
    webbase.Base.redis= redis
    webbase.Base.mongodb= mongodb	

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ccg.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
    
    
    