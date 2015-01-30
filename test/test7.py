import json


"""
cardHand1= '''[{'durability': 0, 'hp': 2, 'cost': 1, 'rarity': 1, 'id': 22, 'skill_id': 0, 'name': 'card22', 'flavor_text': '', 'atk': '5', 'element': 'air', 'race': '', 'type': 'minion', 'card_class': 'warrior'}, {'durability': 0, 'hp': 4, 'cost': 1, 'rarity': 1, 'id': 9, 'skill_id': 0, 'name': 'card9', 'flavor_text': '', 'atk': '0', 'element': 'air', 'race': '', 'type': 'minion', 'card_class': 'warrior'}, {'durability': 0, 'hp': 2, 'cost': 1, 'rarity': 1, 'id': 12, 'skill_id': 0, 'name': 'card12', 'flavor_text': '', 'atk': '3', 'element': 'air', 'race': '', 'type': 'minion', 'card_class': 'warrior'}]'''

cardHand1 = cardHand1.replace("'", "\""); 

#a=json.loads((cardHand1))
a=json.dumps((cardHand1))
a=json.loads((a))
print a[0]
"""