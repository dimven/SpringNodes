# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

walls = UnwrapElement(tolist(IN[0]))

OUT = [getattr(w, 'CurtainGrid', None) is not None for w in walls]