# -*- coding: utf-8 -*-

import sys

err= {
	#common error
	0: '',
	1: 'paramters error',
	2: 'unkown service',
	3: 'unkown method',		
	4: 'parse_message, json.loads error',
	5: 'unkown',
	6: 'unkown error',
	
	#fight error
	14: 'search room error',
	15: 'creat room_id error',
	16: 'round error',	
	17: 'room error',
	18: 'matchedSucceededComplete error',
	19: 'matchedSucceededComplete repeated',
	20: 'startBattel, checked faild',	
	21: 'heroId error!',
	22: 'desktopChange, uniqid error',
	23: 'not enough crystal',
	24: 'It\'s not your turn',
	25: 'skill error',
	26: 'method getCrystalCard return null',
	27: 'Can\'t attack the opponent',
	28: 'You can only attack a taunt opponents',
	29: 'card type is not correct',
	30: 'game over',
	31: 'durability error',
	32: 'no weapon',
	33: 'This creature can\'t attack',
	34: 'You cannot use skill',
	35: 'This monster stunned',
	
	#user error
	101: '',



	
}