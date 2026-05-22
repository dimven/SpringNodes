# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	else: return [obj1]

t1 = tolist(IN[0])
l1 = list(reversed(tolist(IN[1]) ) )
l2 = list(reversed(tolist(IN[2]) ) )

try: OUT = [l1.pop() if i else l2.pop() for i in t1]
except Exception as e: OUT = str(e)