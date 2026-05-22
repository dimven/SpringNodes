#Copyright(c) 2016, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com

import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

curves = IN[0]
margin = IN[1]
original = curves[:]

def OrderCurves(cl0,cl1):
	def switch1(i, j, cl0 = cl0, cl1 = cl1):
		cl0[i],cl0[j] = cl0[j],cl0[i]
		cl1[i],cl1[j] = cl1[j],cl1[i]

	_ln = len(cl1)
	xr1 =  xrange(_ln)
	int_test = [[cl1[i].DoesIntersect(cl1[j])\
	for j in xr1 if j != i] for i in xr1]
	countT = map(sum, int_test)
	if 0 not in countT:
		if 1 in countT and countT[0] != 1 :
			switch1(0, countT.index(1) )
		for i in xrange(_ln - 1):
			k = i + 1
			if cl1[i].DoesIntersect(cl1[k]) : pass
			else :
				try:
					int_test = [cl1[i].DoesIntersect(cl1[j])\
					for j in xrange(k, _ln)]
					switch1(k, k + int_test.index(True) )
				except : pass
	return cl0, cl1

def ClosedCase(cl0,cl1):
	pts = [cl1[i-1].Intersect(cl1[i])[0] for i in xrange(len(cl1) )]
	return PolyCurve.ByPoints(pts,True).Curves()

def OpenCase(cl0,cl1):
	def FarPt(l1, p1):
		pts = (l1.StartPoint,l1.EndPoint)
		return max(pts, key = p1.DistanceTo)

	pts = [cl1[i].Intersect(cl1[i+1])[0] for i in xrange(len(cl1) -1)]
	pts.append(FarPt(cl0[-1],pts[-1]))
	pts.insert(0,FarPt(cl0[0],pts[0]))
	return PolyCurve.ByPoints(pts).Curves()

def joinCurves(cl0,th1):
	len1 = len(cl0)
	if len1 < 2 : return cl0, False
	else:
		cl1 = [c.ExtendStart(th1).ExtendEnd(th1) for c in cl0]
		cl0, cl1 = OrderCurves(cl0,cl1)
		_fn = ClosedCase if cl1[0].DoesIntersect(cl1[-1]) and len1 > 2 else OpenCase
		try : return _fn(cl0,cl1), True
		except : return cl0, False

def ReorderCurves(orig, new):
	reordered, new = [], list(new)
	app1, pop1, PaP = reordered.append, new.pop, Curve.PointAtParameter
	for i in xrange(len(orig) ):
		p1 = PaP(orig[i],0.5)
		p2 = [PaP(new[j],0.5) for j in xrange(len(new) )]
		ind1 = p2.index(min(p2, key = p1.DistanceTo) )
		app1(pop1(ind1) )
	return reordered

out1 = joinCurves(curves, margin)
OUT = out1[0], ReorderCurves(original,out1[0]), out1[1]