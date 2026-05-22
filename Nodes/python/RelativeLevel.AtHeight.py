# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

from itertools import izip

heights, elevs, names, belowOnly = IN
BIG_VAL = float('inf')

def evalHeight(e, belowOnly=belowOnly):
	if belowOnly:
		if e > z:
			return BIG_VAL
	return abs(z - e)

lvl_dict = dict(izip(map(int,elevs), names))
OUT = [lvl_dict[min(lvl_dict, key=evalHeight)] for z in heights]