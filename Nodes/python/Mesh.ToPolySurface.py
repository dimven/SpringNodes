# Copyright(c) 2019, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
from System.Threading import Thread, ThreadStart

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import PolySurface, Surface

meshes, mergeAll, NUMTHREADS = IN
CHOPLIMIT = 10

def tolist(obj1):
	if hasattr(obj1,'__iter__'): return obj1
	return [obj1]

def chop(l1, n):
	return [l1[x:x+n] for x in xrange(0, len(l1), n)]

def ps_generator(ptslist,
				 f_ps1=PolySurface.ByJoinedSurfaces,
				 f_sf1=Surface.ByPerimeterPoints):
		
		sflist = map(f_sf1, ptslist)
		while len(sflist) > CHOPLIMIT:
			new_sflist = map(f_ps1, chop(sflist, CHOPLIMIT))
			for s in sflist: s.Dispose()
			sflist = new_sflist
		return sflist

def mesh2ps(topo):
	vp = topo.VertexPositions
	ptslist = [[vp[i.A], vp[i.B], vp[i.C]] for i in topo.FaceIndices]
	len1 = len(ptslist) / NUMTHREADS + 1

	if len(ptslist) > NUMTHREADS * 3 and NUMTHREADS > 1:
		ptslist = chop(ptslist, len1)
		
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
			w = Worker(ps_generator, (p,))
			t = Thread(ThreadStart(w))
			workers.append(w)
			tasks.append(t)
			t.Start()

		for t in tasks: t.Join()
		return PolySurface.ByJoinedSurfaces(i for w in workers for i in w.result)
	else:
		return  PolySurface.ByJoinedSurfaces(ps_generator(ptslist))

OUT = map(mesh2ps, tolist(meshes))
if mergeAll: OUT = PolySurface.ByJoinedSurfaces(OUT)