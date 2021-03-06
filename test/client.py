from tornado.ioloop  import IOLoop 
import tornado.iostream
import socket
import struct
import json
from tornado import autoreload 
from pprint import pprint

def send_request():
    #encodedjson = '{"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "testMethod", "params":{"uuid": 451377}}'
    stream.read_until("##", on_read)
    """
    encodedjson= encodedjson+ '##'  
    encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
    stream.write(encodedjson)
    """
    
    #stream.read_bytes(int(headers[b"Content-Length"]), on_read)
count= 0
count2= 0
room_id= None
def on_read(data):  
    global  room_id, count, count2
    data= data.rstrip('##') 
    arr= json.loads(data)
    pprint(arr)  
    print "-" * 100
  
    if arr.get('method')!= None and arr.get('method')== 'signUpSucceeded':
        uuid= arr['uid']
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "searchRoom", "params":{"uuid": uuid, "heroId": 1}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)
        
    if arr.get('method')!= None and arr.get('method')== 'matchedSucceeded':
        uuid= arr['uid']
        room_id= roomId= arr['params']['roomInfo']['roomId']
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "matchedSucceededComplete", "params":{"uuid": uuid, "roomId": roomId}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)
    
    if arr.get('method')!= None and arr.get('method')== 'getFirstHC':
        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "confirmFirstHC", "params":{"uuid": uuid, "roomId": roomId}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)
       
       
         
    if arr.get('method')!= None and arr.get('method')== 'startBattel' and arr['params']['isFirst']== 1:
        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id
    
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "turnEnd", "params":{"uuid": uuid,  "roomId": roomId}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)
        
    if arr.get('method')!= None and arr.get('method')== 'turnStart' :
        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id

        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id
            
        if count< 2:            
            encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "turnEnd", "params":{"uuid": uuid,  "roomId": roomId}}
            encodedjson= json.dumps(encodedjson)
            encodedjson= encodedjson+ '##'  
            encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
            stream.write(encodedjson)
            count= count+ 1 
            
            ######################################################################################################
        else:
            id= arr['params']['cards']["_id"]        
            uniqid= arr['params']['cards']["uniqid"]
            obj= {}
            obj['_id']= id
            obj['uniqid']= uniqid
            obj['locaX']= 10086
            obj['locaY']= 0
            print "obj:", obj
            encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "putCardOnDesk", "params":{"uuid": uuid, "card": obj, "roomId": roomId}}
            encodedjson= json.dumps(encodedjson)
            encodedjson= encodedjson+ '##'  
            encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
            stream.write(encodedjson)
                         
  
    ''''''''' 
    if arr.get('method')!= None and arr.get('method')== 'startBattel':
        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id
        
        id= arr['params']['cards']["_id"]        
        uniqid= arr['params']['cards']["uniqid"]
        obj= {}
        obj['_id']= id
        obj['uniqid']= uniqid
        obj['locaX']= 10086
        obj['locaY']= 0
        print "obj:", obj
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "putCardOnDesk", "params":{"uuid": uuid, "card": obj, "roomId": roomId}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)
  

    if arr.get('method')!= None and arr.get('method')== 'getFirstHC':
        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id
        id= arr['params']['cards'][0]["_id"]
        print "id:", id
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "changeFirstHC", "params":{"uuid": uuid, "cards": [id], "roomId": roomId}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)       

    '''''''''   
            
    '''        
    if arr.get('method')!= None and arr.get('method')== 'desktopChange':
        uuid= arr['uid']
        #roomId= arr['params']['roomInfo']['roomId']
        roomId= room_id
        _id1= arr['params']['dSelf'][0]['uniqid']
        _id2= arr['params']['dOpp'][0]['uniqid']
        print '_id1, _id2',_id1,_id2, roomId
        encodedjson = {"uid":3022, "version": "2013.11.12.10.31.00", "service": "FightService", "method": "atkTarget", "params":{"uuid": uuid, "roomId": roomId,\
        "attacker":{'uniqid':_id1}, "target":{'uniqid':_id2}}}
        encodedjson= json.dumps(encodedjson)
        encodedjson= encodedjson+ '##'  
        encodedjson= struct.pack(str(len(encodedjson))+'s', encodedjson) 
        stream.write(encodedjson)
        
        count2= count2+ 1
    '''
    stream.read_until("##", on_read)
    #stream.close()
    #tornado.ioloop.IOLoop.instance().stop()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
stream = tornado.iostream.IOStream(s)
stream.connect(("127.0.0.1", 8801), send_request)
#stream.connect(("50.23.111.162", 8801), send_request)
loop= IOLoop.instance()
autoreload.start(loop)
loop.start()


