# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

from System.IO import FileInfo

def tolist(x):
	if hasattr(x,'__iter__'): return x
	else : return [x]

paths = tolist(IN[0])
mb = 1048576.0
kb = 1024.0
def getSize(p, mb=mb, kb=kb, kbOnly = IN[1]):
	sb = FileInfo(p).Length
	if sb < mb or kbOnly:
		return '%.3f KB' % (sb / kb)
	else:
		return '%.3f MB' % (sb / mb)

OUT = map(getSize, paths)