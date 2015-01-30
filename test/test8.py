import os, sys, json


str= """[{u'skill_id': 0, u'special_swf': u'', u'rand': 0.665725248832065, u'name': u'Calming Preist of Solesna', u'Img': u'DefaultImage.png', u'class': u'Neutral', u'hp': 1,
u'version': u'Alpha', u'atk': 2, u'rarity': u'Basic', u'version_serial': 8, u'race2': u'', u'cost': 1, u'durabilitycount': 0, u'race': u'', u'element': u'NA', u'_id': 8, u'type': u'Creature', u'flavor_text': u''}, {u'skill_id': 0, u'special_swf': u'', u'rand':
 0.6210551782282493, u'name': u'Mospen, Queen of Succubus ', u'Img': u'MospenQueenOfSuccubus.png', u'class': u'Neutral', u'hp': 12, u'version': u'Alpha', u'atk': 4, u'rarity': u'Legendary', u'version_serial': 33, u'race2': u'', u'cost': 9, u'durabilitycount':
0, u'race': u'Archfiend', u'element': u'NA', u'_id': 33, u'type': u'Creature', u'flavor_text': u''}, {u'skill_id': 1, u'special_swf': u'', u'rand': 0.6369128971611271, u'name': u"Kelytia Heaven's Defender ", u'Img': u'KelytiaHeavensDefender.png', u'class': u'N
eutral', u'hp': 4, u'version': u'Alpha', u'atk': 5, u'rarity': u'Basic', u'version_serial': 27, u'race2': u'', u'cost': 5, u'durabilitycount': 0, u'race': u'', u'element': u'NA', u'_id': 27, u'type': u'Creature', u'flavor_text': u''}]"""

d= {u'skill_id': 1, u'special_swf': u'', u'rand': 0.6369128971611271, u'name': u"Kelytia Heaven's Defender ", u'Img': u'KelytiaHeavensDefender.png', u'class': u'N
eutral', u'hp': 4, u'version': u'Alpha', u'atk': 5, u'rarity': u'Basic', u'version_serial': 27, u'race2': u'', u'cost': 5, u'durabilitycount': 0, u'race': u'', u'element': u'NA', u'_id': 27, u'type': u'Creature', u'flavor_text': u''}

print json.dumps(d)

j= str.replace("u'", "'").replace("'", "\"")
print j
arr= json.loads(j)
print arr

print "\n"


str= """[{"skill_id": 0, "special_swf": "", "rand": 0.718432468951623, "name": "Yutmor the Earthshaker", "Img": "YutmorTheEarthshaker.png", "class": "Neutral", "hp": 4, "version": "Alpha", "atk": 4, "rarity": "Common", "version_serial": 63, "race2": "", "cost": 4, "durabilitycount": 0, "race": "Helioguardian", "element": "NA", "_id": 63, "type": "Creature", "flavor_text": ""}]"""
j= str.replace("u'", "'").replace("'", "\"")
print j
arr= json.loads(j)
print arr