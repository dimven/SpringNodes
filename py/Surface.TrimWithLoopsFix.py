# Copyright(c) 2018, Dimitar Venkov
# @5devene, dimitar.ven@gmail.com
# www.badmonkeys.net

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import Point

surf, trims = IN
original = True
for t in trims:
	bb = t.BoundingBox
	a, b = bb.MinPoint, bb.MaxPoint
	c = Point.ByCoordinates((a.X + b.X)/2, (a.Y + b.Y)/2, (a.Z + b.Z)/2)
	temp = surf.Trim(t, c)[0]
	if original:
		original = False
	else:
		surf.Dispose()
	surf = temp
OUT = surf