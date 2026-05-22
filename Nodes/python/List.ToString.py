import re
from itertools import izip_longest

import clr
clr.AddReference('DesignScriptBuiltin')
from DesignScript.Builtin import Dictionary as dsDict

from System import Int64

def replaceDict(x):
	if hasattr(x,'__iter__'): return map(replaceDict, x)
	if isinstance(x, dsDict): return dict(zip(x.Keys, replaceDict(x.Values)))
	if isinstance(x, Int64): return int(x)
	return x

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

rep = {"'" : "\"",
	   "[" : "[\n",
	   "]" : "\n]",
	   "None" : "null",
	   "True" : "true",
	   "False" : "false",
	   ", " : ",\n",
	   "{" : "{\n",
	   "}" : "\n}"
	  }

if not IN[1]:
	del rep["["]
	del rep["]"]
	del rep[", "]
	del rep["{"]
	del rep["}"]

rep = dict((re.escape(k), v) for k, v in rep.iteritems())
pattern = re.compile("|".join(rep.keys()))
s1 = str(replaceDict(tolist(IN[0])))

body, strings = re.split("'[^/']+'", s1), re.findall("'([^/']+)'", s1)
body = (pattern.sub(lambda m: rep[re.escape(m.group(0))], b) for b in body)
OUT = ''.join('%s"%s"' % (b, s) if s else b for b, s in izip_longest(body, strings))