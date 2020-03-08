# Copyright(c) 2020, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as DS

def tolist(x):
    if hasattr(x,'__iter__'): return x
    return [x]

surfaces = tolist(IN[0])

def dropSurfaceOpenings(srf):
	face = srf.Faces[0]
	extLoop = [lp for lp in srf.Faces[0].Loops if lp.IsExternal][0]
	return [ce.Edge.CurveGeometry for ce in extLoop.CoEdges]

OUT = map(dropSurfaceOpenings, surfaces)