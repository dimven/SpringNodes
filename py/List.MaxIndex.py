# Copyright(c) 2019, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(x):
	if hasattr(x,'__iter__'): return x
	return [x]

data = tolist(IN[0])
OUT = max(enumerate(data), key=lambda x: x[1])