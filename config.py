# -*- coding: utf-8 -*-  
import os
import sys
import ConfigParser
import logging

"""
init constant var
"""
path_root	=	''

log_level	=	None

mail_server=''
mail_from=''
mail_to=''

config= None


def __get_config():
	config_path = path_root + '/conf/app.py'
	#print config_path
	cf = ConfigParser.ConfigParser()
	cf.read(config_path)
	sections = {}
	for section in cf.sections():
		sections[section] = {}
		items = cf.items(section)
		for item in items:
			key = item[0]
			value = item[1]
			sections[section][key] = value
	return sections

def __init():
	global path_root
	global log_level
	global mail_server,mail_from,mail_to
	global config
	script_path = os.path.dirname(os.path.abspath(__file__))

	#path_root = script_path[0:-8]
	path_root = script_path

	config = __get_config()

	try:
		log_level = int(config['GLOBAL']['log_level'])
		
		if log_level == 1:
			log_level = logging.ERROR
		elif log_level == 2:
			log_level = logging.WARNING
		elif log_level == 3:
			log_level = logging.INFO
		elif log_level == 4:
			log_level =logging.DEBUG

		
		mail_server = config['MAIL']['smtp_server']
		mail_from = config['MAIL']['from']
		mail_to = config['MAIL']['to']

	except Exception,e:
		print 'config file error[%s],exit'%(e)
		sys.exit()

__init()
