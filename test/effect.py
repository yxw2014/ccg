data= {

    "triger": "myTurnEnd",
    
    "trigerCondition": {
        "object": None,
        "target": {
			        "range":"camp",
			        "field": "hands",
			        "role": "hero",
			        "job": "warrior",
			        "race": "kids",        
			            
			        "mathCondition": {
			            "type": "hpGT",
			            "value":3
			        },
			        
			        "pointer": {
			            "type": "randomX",
			            "value": 2
			        }    
			    },
        "condition": "die"
    }, 
       
    "object": None,
    
    "target": {
        "range":"camp",
        "field": "hands",
        "role": "hero",
        "job": "warrior",
        "race": "kids",        
            
        "mathCondition": {
            "type": "hpGT",
            "value":3
        },
        
        "pointer": {
            "type": "randomX",
            "value": 2
        }    
    },  
       
    "type": "chakra+",
    
    "value":{
        "type":"toN",
        "value":30   
    },
       
    "valueFrom":{
        "target": {
			        "range":"camp",
			        "field": "hands",
			        "role": "hero",
			        "job": "warrior",
			        "race": "kids",        
			            
			        "mathCondition": {
			            "type": "hpGT",
			            "value":3
			        },
			        
			        "pointer": {
			            "type": "randomX",
			            "value": 2
			        }    
			    },
        "type": "toN",
        "value": 1  
    },   
       
    "continuous": {
        "type": "thisTurnEnd",
        "value": 0
    }

}

print data

'''
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


output = dump(data, Dumper=Dumper, default_flow_style=True, indent= '    ')

print output


file_object = open('yaml.txt', 'w')
try:
     file_object.write(output)
finally:
     file_object.close()

file_object = open('yaml.txt')
try:
     all_the_text = file_object.read()
     print load(all_the_text)
finally:
     file_object.close()
'''
