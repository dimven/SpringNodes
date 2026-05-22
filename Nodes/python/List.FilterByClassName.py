# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
from itertools import izip, imap, repeat

def tolist(obj1):
	if hasattr(obj1,"__iter__"): return obj1
	else: return [obj1]

OUT = []
elements = tolist(IN[0])
optNames = IN[1]
filter = set(imap(str.lower, imap(str, tolist(IN[2]) ) ) )

useOptNames = optNames is not None and len(elements) == len(tolist(optNames) )
if useOptNames:
	optNames = map(str.lower, imap(str, tolist(optNames) ) )
else:
	optNames = repeat("", len(elements) )

for e, n in izip(elements, optNames):
	if useOptNames:
		n1 = n
	else:
		n1 = object.GetType(e).ToString().lower() if e is not None else "null"
	OUT.append(any(f in n1 for f in filter) )