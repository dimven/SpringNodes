# Copyright(c) 2017, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
from System.Threading import Thread, ThreadStart
from operator import itemgetter

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

def tolist(obj1):
	if hasattr(obj1,'__iter__'):
		return obj1
	else:
		return [obj1]

def chop1(l1, n):
	return [l1[x:x+n] for x in xrange(0, len(l1), n)]

def mesh2ps(topo, f_chop = chop1, itemgetter=itemgetter, 
			f_ps1 = PolySurface.ByJoinedSurfaces,
			f_sf1 = Surface.ByPerimeterPoints):
	
	NUMTHREADS = 4
	vp = topo.VertexPositions
	ptslist = [itemgetter(i.A, i.B, i.C)(vp) for i in topo.FaceIndices]
	len1 = len(ptslist) / NUMTHREADS + 1

	def ps_generator(ptslist, chop1=chop1,
					 f_ps1 = PolySurface.ByJoinedSurfaces,
					 f_sf1 = Surface.ByPerimeterPoints):
		
		sflist = map(f_sf1, ptslist)
		while len(sflist) > 10 :
			sflist = map(f_ps1, chop1(sflist, 10) )
		return sflist
	
	if len(ptslist) > 10 :
		ptslist = f_chop(ptslist, len1)
		
		class Worker(object):
			__slots__ = 'fn', 'args', 'result'
			def __init__(self, fn, args):
				self.fn = fn
				self.args = args
				self.result = None
			def __call__(self):
				self.result = self.fn(*self.args)
		
		workers, tasks = [], []
		for p in ptslist:
			w = Worker(ps_generator, (p,) )
			t = Thread(ThreadStart(w) )
			workers.append(w)
			tasks.append(t)
			t.Start()

		for t in tasks: t.Join()
		return f_ps1(i for w in workers for i in w.result)
	else:
		return  f_ps1(ps_generator(ptslist) )
		
meshes = tolist(IN[0])
OUT = map(mesh2ps, meshes)
if IN[1]:
	OUT = PolySurface.ByJoinedSurfaces(OUT)