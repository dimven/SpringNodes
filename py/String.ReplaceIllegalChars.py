# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

from itertools import imap, repeat
import System
badChars = set(System.IO.Path.GetInvalidFileNameChars() )

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

def fixName(n, rep="", badChars=badChars):
	n1 = (c if c not in badChars else rep for c in iter(n) )
	return ''.join(n1)

names = tolist(IN[0])
replacement = str(IN[1])
other = tolist(IN[2])

badChars.update(other)
OUT = map(fixName, imap(str, names), repeat(replacement, len(names) ) )