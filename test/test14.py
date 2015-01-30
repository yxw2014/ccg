import logging
a= [3,5,7,9]
b= [8,9, 15]
for k, key in enumerate(a): 
	if k== 1:
		a.pop(k)
print a
print a.count(10)
print a+= b
#print a.extend(b)
print a