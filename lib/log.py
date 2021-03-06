# -*- coding: utf-8 -*-  
import os, sys
import logging
import config
import time

_logFormat = "%(asctime)s %(levelname)s:%(message)s"
_dateFormat = "%Y-%m-%d %H:%M:%S"

_logger = None

log_path, level= None, None
warn,info,error,debug = None,None,None,None

def get_logger(log_path,level = logging.DEBUG):	
	logging.basicConfig(level = level,
			format = _logFormat,
			datefmt = _dateFormat,
			filename = log_path)
	logger = logging.getLogger()
	return logger

def init():
	global log_path, level, warn,info,error,debug
	log_dir_path = config.path_root + '/log/'
	log_path = config.path_root + '/log/app.log'
	tm= time.strftime('%Y%m%d',time.localtime(time.time()))
	log_path= log_path+ tm

	if not os.path.isdir(log_dir_path):
		os.makedirs(log_dir_path)
	level = config.log_level

	logger = get_logger(log_path,level)
	error = logger.error
	warn = logger.warning
	info = logger.info
	debug = logger.debug

init()