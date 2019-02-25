# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

OUT = []

keys = tolist(IN[0])
elements = tolist(IN[1])
searchVals = tolist(IN[2])

dict1 = dict(zip(keys,elements) )
OUT = [dict1.get(sv, IN[3]) for sv in searchVals]