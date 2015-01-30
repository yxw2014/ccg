effect= {
triger= "myTurnEnd"
trigerCondition= {
object= nil
target= nil
}
target= {
	range":"camp"
	field": "hands"
	role: "hero"
	job: "warrior"
	race: "kids"            
	mathCondition: {
			            type: "hpGT"
			            value:3
			        },
			        
	pointer: {
			           type: "randomX"
			            value: 2
			}  
}
