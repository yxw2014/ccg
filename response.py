# -*- coding: utf-8 -*-

import sys,os,time
import json, struct
from  const import *
from config import config
from errors import err

class response:
    def __init__(self, data, uid):        
        if(isinstance(data, dict)!= False):           
            #self.error= data["error"]
            self.service= data["service"]
            self.method= data["method"]
            self.data= data["data"]
            self.data['error']= data["error"]
            self.uid= uid
            self.error= False
        else:
            self.error= True
        self.version= '2013111910'
        
    def dump(self):
        '''
        if self.error!= True:
            obj = {'version': self.version, "uid": self.uid, 'service':self.service, 'method':self.method, 'params': self.data} 
        else:
            obj = {'version': self.version, "uid": '', 'service':'main', 'method':'error', 'params': {'error': {"code":6, 'msg':err[6]}}} 
        '''
            
        if self.error!= True:
            obj = {"uid": self.uid, 'method':self.method, 'params': self.data} 
            self.format(obj['params'])
        else:
            obj = {"uid": '', 'method':'error', 'params': {'error': {"code":6, 'msg':err[6]}}}
             
        encodedjson = json.dumps(obj) 
        encodedjson= (encodedjson+ config['GAME']['msgsuffix'])
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson)
        return encodedjson
    
    
    def format(self, obj):
        self.__format(obj) 
        if isinstance(obj, dict)== True:
            for key, val in obj.items():
                if isinstance(val, dict)== True:
                    self.__format(obj[key])
                elif isinstance(val, list)== True:
                    for k, v in enumerate(obj[key]):
                        self.__format(obj[key][k])
                else:
                    pass
    
    def __format(self, obj):
        if isinstance(obj, dict)== True:
            for key, val in obj.items():  
                c= 0               
                if key== 'uniqid':
                    c= 1
                    obj[V_UNIQID]= val                    
                elif key== 'locaX':
                    c= 1
                    obj[V_INDEX]= val
                elif key== 'status':
                    c= 1
                    obj[V_STATUS]= val
                elif key== 'type':
                    c= 1
                    obj[V_TYPE]= val
                elif key== 'armor':
                    c= 1
                    obj[V_ARMOR]= val
                elif key== 'aTime':
                    c= 1
                    obj[V_ATTACK_TIME]= val
                elif key== 'sTime':
                    c= 1
                    obj[V_HERO_SKILL_TIME]= val  
                elif key== 'weapon':
                    c= 1
                    obj[V_WEAPON]= val 
                elif key== 'desktopOpp':
                    c= 1
                    obj[V_DESKTOP_OPP]= val
                elif key== 'desktopSelf':
                    c= 1
                    obj[V_DESKTOP_SELF]= val
                elif key== 'skillCardId':
                    c= 1
                    obj[V_SKILL_CARD_ID]= val
                elif key== 'crystal':
                    c= 1
                    obj[V_CRYSTAL]= val
                if c== 1:
                    del obj[key] 
        
if __name__ == '__main__':  
    c= response({})
    print c.dump()
    
    
    
    
    
    